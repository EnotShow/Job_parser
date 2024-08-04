class BaseClient:
    @staticmethod
    def _add_pagination(url: str, limit: int, page: int):
        params = []

        if limit:
            params.append(f"limit={limit}")
        if page:
            params.append(f"page={page}")

        if params:
            separator = "&" if "?" in url else "?"
            result_string = separator + "&".join(params)
            return url + result_string
        else:
            return url
