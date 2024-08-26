from fake_useragent import UserAgent
from playwright.async_api import async_playwright

from src.api.smart_editor.smart_dto import SmartEditorParamsDTO
from src.api.smart_editor.smart_editor_generator import SmartEditorLinkGenerator


class DynamicLinkGenerator(SmartEditorLinkGenerator):
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def init_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context(user_agent=self._get_user_agent())
        self.page = await self.context.new_page()

        # Configure the page to mimic a real user
        await self.page.evaluate("""
            () => {
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            }
        """)

    def _get_user_agent(self):
        user_agent = UserAgent(os="Windows", browsers=["Chrome"])
        return user_agent.random

    async def close_browser(self):
        if self.browser:
            await self.browser.close()

    async def generator_execute(self, param_dto: SmartEditorParamsDTO):
        if not self.browser:
            await self.init_browser()
        try:
            return await self.generate_link(param_dto)
        except Exception as e:
            print(e)

    async def generate_link(self, params_dto: SmartEditorParamsDTO):
        pass
