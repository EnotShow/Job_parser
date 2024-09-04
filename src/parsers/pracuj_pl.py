import requests
from bs4 import BeautifulSoup

from src.api.applications.application_dto import ApplicationCreateDTO


class PracujParser:
    base_url = 'https://www.pracuj.pl'

    async def parse_offers(self, url: str, owner_id: int):
        result = []
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        offers_section = soup.find('div', {'data-test': 'section-offers'})
        if offers_section:
            jobs = offers_section.find_all(class_='tiles_b1j1pbod')
            for i in jobs:
                description = await self._parse_details(i.a['href'])
                job = ApplicationCreateDTO(
                    title=i.get_text(separator='\n'),
                    url=i.a['href'],
                    description=description,
                    owner_id=owner_id
                )
                result.append(job)
        return result if result else r.text

    async def _parse_details(self, url: str):
        def extract_section_text(soup, section_name):
            section = soup.find('section', {'data-test': section_name})
            return section.get_text(separator="\n") if section else ""

        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        responsibilities = extract_section_text(soup, 'section-responsibilities')
        requirements = extract_section_text(soup, 'section-requirements')
        offered = extract_section_text(soup, 'section-offered')

        description = f"{responsibilities}\n{requirements}\n{offered}"
        return description
