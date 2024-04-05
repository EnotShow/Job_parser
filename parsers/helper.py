import functools

from pyvirtualdisplay import Display

from parsers.olx import OlxParser
from parsers.pracuj import PracujParser


async def display(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        disp = Display(visible=0, size=(800, 600))
        disp.start()
        await func(*args, **kwargs)
        disp.stop()

    return wrapper


async def get_parser(url: str):
    if url.startswith(OlxParser.base_url):
        return OlxParser()
    elif url.startswith(PracujParser.base_url):
        return PracujParser()
