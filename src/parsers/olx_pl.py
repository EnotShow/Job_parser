import asyncio

import requests
from bs4 import BeautifulSoup

from src.api.applications.application_dto import ApplicationCreateDTO


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


async def main():
    parser = OlxParser()
    print(await parser.parse_offers('https://www.olx.pl/praca/q-linux/?search%5Border%5D=created_at:desc', 1))


if __name__ == '__main__':
    asyncio.run(main())
