import asyncio

import requests
from bs4 import BeautifulSoup

from src.dtos.application_dto import ApplicationDTO, ApplicationCreateDTO


class OlxParser:
    base_url = 'https://www.olx.pl'

    async def parse_offers(self, url: str):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        jobs = soup.div.find_all(class_='jobs-ad-card css-1qmjf8h')
        result = []
        for i in jobs:
            job = ApplicationCreateDTO(title=i.get_text(separator='\n'), url=self.base_url + i.a['href'])
            result.append(job)
        return result


if __name__ == '__main__':
    p = OlxParser()
    asyncio.run(p.parse_offers('https://www.olx.pl/praca/gastronomia/'))
