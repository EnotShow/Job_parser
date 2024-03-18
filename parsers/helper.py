from parsers.olx import OlxParser
from parsers.pracuj import PracujParser


async def get_parser(url: str):
    if url.startswith(OlxParser.base_url):
        return OlxParser()
    elif url.startswith(PracujParser.base_url):
        return PracujParser()
