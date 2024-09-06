from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.config.email.email_config import config_email

# print(src_path)
# print(config_email.TEMPLATE_ROOT)
env = Environment(
    loader=FileSystemLoader("app/src/api/auth/templates/"),
    autoescape=select_autoescape(config_email.AVAILABLE_TYPES.split()),
)

# print(env.loader.searchpath)
