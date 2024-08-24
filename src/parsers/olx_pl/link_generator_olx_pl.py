from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.api.smart_editor.smart_dto import SmartEditorParamsDTO
from src.parsers.helpers.link_generators import DynamicLinkGenerator


class OlxDynamicLinkGenerator(DynamicLinkGenerator):
    base_url = "https://www.olx.pl/praca/"
    _filter = "?search%5Border%5D=created_at:desc"  # start from new filter

    def generate_link(self, params_dto: SmartEditorParamsDTO) -> Any | None:
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
            location_input.send_keys(params_dto.location)

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
            search_input.send_keys(params_dto.kwords)

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
