import asyncio

import requests
from bs4 import BeautifulSoup

from src.dtos.application_dto import ApplicationCreateDTO


class PracujParser:
    base_url = 'https://www.pracuj.pl'

    async def parse_offers(self, url: str):
        result = []
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        offers_section = soup.find('div', {'data-test-id': 'section-offers'})
        if offers_section:
            jobs = offers_section.div.find_all(class_='tiles_c1m5bwec')
            for i in jobs:
                description, application_link = await self._parse_details(i.a['href'])
                job = ApplicationCreateDTO(
                    title=i.get_text(separator='\n'),
                    url=i.a['href'],
                    description=description,
                    application_link=application_link
                )
                result.append(job)
        return result

    async def _parse_details(self, url: str):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        responsibilities = soup.find('div', {'data-test': 'section-responsibilities'}).get_text(separator="\n")
        requirements = soup.find('div', {'data-test': 'section-requirements'}).get_text(separator="\n")
        offered = soup.find('div', {'data-test': 'section-offered'}).get_text(separator="\n")
        description = responsibilities + "\n" + requirements + "\n" + offered
        application_link = soup.find("a", {"data-test": "anchor-apply"})['href']
        return description, application_link
