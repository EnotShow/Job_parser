import requests
from bs4 import BeautifulSoup

from src.api.applications.application_dto import ApplicationCreateDTO


class PracaParser:
    base_url = 'https://www.praca.pl/'

    async def parse_offers(self, url: str, owner_id: int):
        result = []
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")

        offers_section = soup.find('div', {'class': 'app-content__body app-content__body--default'})

        if offers_section:
            jobs = offers_section.find_all(class_='listing__item')

            for i in jobs:
                raw_title = i.get_text(separator=' ').strip()
                title = ' '.join(raw_title.split())

                job_url = i.a['href']

                # Construct the full job URL if it's a relative path
                if not job_url.startswith('http'):
                    job_url = self.base_url + job_url

                job = ApplicationCreateDTO(
                    title=title,
                    url=job_url,
                    description="No description provided for this resource",
                    owner_id=owner_id
                )

                result.append(job)

        return result if result else r.text
