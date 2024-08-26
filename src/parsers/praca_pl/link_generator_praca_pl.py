from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from src.api.smart_editor.smart_dto import SmartEditorParamsDTO
from src.parsers.helpers.link_generators import DynamicLinkGenerator

"""
Example of usage:

async def main():
    param_dto = SmartEditorParamsDTO(
        kwords="python developer",
        location="Warszawa",
        salary="1000-2000",
        services=[ServiceEnum.OLX_PL],
        owner_id=1,
        links_limit=25,
    )

    generator = PracaDynamicLinkGenerator()

    try:
        await generator.init_browser()
        result = await generator.generator_execute(param_dto)
        print(result)
        param_dto.kwords = "java developer"
        result = await generator.generator_execute(param_dto)
        print(result)
        param_dto.kwords = "javascript developer"
        result = await generator.generator_execute(param_dto)
        print(result)
        param_dto.kwords = "kotlin developer"
        result = await generator.generator_execute(param_dto)
        print(result)
        param_dto.kwords = "Django developer"
        result = await generator.generator_execute(param_dto)
        print(result)
    finally:
        await generator.close_browser()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Exception in main: {e}")
"""


class PracaDynamicLinkGenerator(DynamicLinkGenerator):
    base_url = "https://www.praca.pl/"

    async def generate_link(self, params_dto: SmartEditorParamsDTO) -> str | None:
        try:
            await self.page.goto(self.base_url)

            # Accept cookies
            try:
                # Wait for and click the "Accept all" cookies button
                accept_all_button = await self.page.wait_for_selector('button:has-text("Akceptuj wszystkie")',
                                                                      timeout=10000)
                await accept_all_button.click()
            except PlaywrightTimeoutError:
                print("No cookie banner appeared or failed to locate the accept button")

            # Fill in the location field
            location_input = await self.page.wait_for_selector('input.test__search-place', timeout=10000)
            await location_input.fill(params_dto.location)

            # Fill in the keyword field
            keyword_input = await self.page.wait_for_selector('input.test__search-phrase', timeout=10000)
            await keyword_input.fill(params_dto.kwords)

            # Click the search button
            search_button = await self.page.wait_for_selector('button.css-32vdb2', timeout=10000)
            await search_button.click()

            # Wait for network request to complete
            await self.page.wait_for_load_state("networkidle")

            return self.page.url

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
