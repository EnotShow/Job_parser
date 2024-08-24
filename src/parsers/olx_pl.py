import asyncio
import time
from typing import Any

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.api.applications.application_dto import ApplicationCreateDTO
from src.api.smart_editor.smart_dto import SmartEditorParamsDTO
from src.parsers.link_generators import DynamicLinkGenerator


class OlxParser:
    base_url = 'https://www.olx.pl'

    async def parse_offers(self, url: str, owner_id: int):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        jobs = soup.div.find_all(class_='jobs-ad-card')
        result = []
        for i in jobs:
            try:
                title, url = i.get_text(separator='\n'), self.base_url + i.a['href']
                description = await self._parse_details(url)
                job = ApplicationCreateDTO(
                    title=title,
                    url=url,
                    description=description,
                    owner_id=owner_id
                )
                result.append(job)
            except AttributeError:
                pass
        return result

    async def _parse_details(self, url: str):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        description = soup.find(class_='css-14ie0im').get_text()
        return description


class OlxDynamicLinkGenerator(DynamicLinkGenerator):
    base_url = "https://www.olx.pl/praca/"
    _filter = "?search%5Border%5D=created_at:desc"

    def generate_link(self) -> Any | None:
        try:
            self.driver.get(self.base_url)

            # Accept cookies if the banner is present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
            )
            self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

            # Fill in the location
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "location-input"))
            )
            location_input = self.driver.find_element(By.ID, "location-input")
            location_input.send_keys("Warszawa")

            # Wait for location suggestion and select the first suggestion
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='suggestion-list']"))
            )
            first_suggestion = self.driver.find_element(By.CSS_SELECTOR, "li[data-testid='suggestion-item']")
            first_suggestion.click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='search-submit']"))
            )

            # Fill in the search query
            search_input = self.driver.find_element(By.CSS_SELECTOR, "input[data-testid='search-input']")
            search_input.send_keys("Linux")

            # Save the current link before search
            current_link = self.driver.current_url

            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='search-submit']")
            submit_button.click()

            # Wait for the URL to change after the search is submitted
            WebDriverWait(self.driver, 10).until(
                EC.url_changes(current_link)
            )

            return self.driver.current_url + self._filter

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
