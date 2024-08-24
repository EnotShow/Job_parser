from fake_useragent import UserAgent
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from src.api.smart_editor.smart_dto import SmartEditorParamsDTO
from src.api.smart_editor.smart_editor_generator import SmartEditorLinkGenerator


class DynamicLinkGenerator(SmartEditorLinkGenerator):

    def __init__(self, param_dto: SmartEditorParamsDTO):
        super().__init__(param_dto)
        ua = UserAgent(os="Windows", browsers=["Chrome"])

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua.random})

    def __del__(self):
        self.driver.quit()
