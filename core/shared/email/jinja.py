import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.config.email.email_config import config_email


env = Environment(
    loader=FileSystemLoader(os.path.join(os.getcwd(), config_email.TEMPLATE_ROOT)),
    autoescape=select_autoescape(config_email.AVAILABLE_TYPES.split()),
)
