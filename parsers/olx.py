import requests
from bs4 import BeautifulSoup

from src.api.dtos.application_dto import ApplicationCreateDTO


class OlxParser:
    base_url = 'https://www.olx.pl'

    async def parse_offers(self, url: str):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        jobs = soup.div.find_all(class_='jobs-ad-card css-1qmjf8h')
        result = []
        for i in jobs:
            title, url = i.get_text(separator='\n'), self.base_url + i.a['href']
            description, application_link = await self._parse_details(url)
            job = ApplicationCreateDTO(
                title=title,
                url=url,
                description=description,
                application_link=application_link
            )
            result.append(job)
        return result

    async def _parse_details(self, url: str):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        description = soup.find(class_='css-14ie0im').get_text()
        application_link = soup.find(class_='css-ezafkw')['href']
        if application_link.startswith('/'):
            application_link = self.base_url + application_link
        return description, application_link
