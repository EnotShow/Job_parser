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
                job = ApplicationCreateDTO(title=i.get_text(separator='\n'), url=i.a['href'])
                result.append(job)
        return result
