from src.api.smart_editor.smart_dto import SmartEditorParamsDTO


class SmartEditorLinkGenerator:
    _result_url = None

    def __init__(self, param_dto: SmartEditorParamsDTO):
        self.params = param_dto

    @property
    def result_url(self):
        return self.result_url

    @result_url.setter
    def result_url(self, url):
        self._result_url = url
