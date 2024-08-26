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

    generator = OlxDynamicLinkGenerator()

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

class OlxDynamicLinkGenerator(DynamicLinkGenerator):
    base_url = "https://www.olx.pl/praca/"
    _filter = "?search%5Border%5D=created_at:desc"

    async def generate_link(self, params_dto: SmartEditorParamsDTO) -> str | None:
        try:
            # Navigate to the base URL
            await self.page.goto(self.base_url)

            # Accept cookies if the banner is present
            try:
                accept_button = await self.page.wait_for_selector("#onetrust-accept-btn-handler", timeout=10000)
                await accept_button.click()
            except PlaywrightTimeoutError:
                print("No cookie banner appeared")

            # Fill in the location
            location_input = await self.page.wait_for_selector("#location-input", timeout=10000)
            await location_input.fill(params_dto.location)

            # Wait for location suggestion and select the first suggestion
            first_suggestion = await self.page.wait_for_selector("li[data-testid='suggestion-item']", timeout=10000)

            # Wait for navigation to start and complete after clicking the suggestion
            async with self.page.expect_navigation(wait_until="load"):
                await first_suggestion.click()

            # Fill in the search query
            search_input = await self.page.wait_for_selector("input[data-testid='search-input']", timeout=10000)
            await search_input.fill(params_dto.kwords)

            # Save the current link before search
            current_link = self.page.url

            # Submit the search
            submit_button = await self.page.wait_for_selector("button[data-testid='search-submit']", timeout=10000)

            # Wait for navigation to start and complete after submitting the search
            async with self.page.expect_navigation(wait_until="load"):
                await submit_button.click()

            # Wait for the URL to change after the search is submitted
            await self.page.wait_for_url(lambda url: url != current_link, timeout=10000)

            # Return the final URL with the filter applied
            return self.page.url + self._filter

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
