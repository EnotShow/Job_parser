from src.parsers.olx_pl.job_parser_olx_pl import OlxParser
from src.parsers.praca_pl.job_parser_praca_pl import PracaParser
from src.parsers.pracuj_pl.job_parser_pracuj_pl import PracujParser


async def get_parser(url: str):
    if url.startswith(OlxParser.base_url):
        return OlxParser()
    elif url.startswith(PracujParser.base_url):
        return PracujParser()
    elif url.startswith(PracaParser.base_url):
        return PracaParser

