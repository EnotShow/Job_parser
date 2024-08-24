from src.parsers.enums import ServiceEnum
from src.parsers.olx_pl.link_generator_olx_pl import OlxDynamicLinkGenerator


async def get_link_generator(service: ServiceEnum):
    if service == ServiceEnum.OLX_PL:
        return OlxDynamicLinkGenerator
    elif service == ServiceEnum.PRACUJ_PL:
        pass
    elif service == ServiceEnum.PRACA_PL:
        pass
