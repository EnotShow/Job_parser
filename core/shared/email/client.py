from email.message import EmailMessage
from smtplib import SMTP_SSL, SMTPException

from core.config.email.smtp_config import config_smtp
from src.api.email.email_dto import EmailDTO
from .exceptions import SendEmailError


class EmailClient:
    """Email sender."""

    def __init__(self) -> None:
        self.port: int = config_smtp.SMTP_PORT
        self.host: str = config_smtp.SMTP_HOST
        self.password: str = config_smtp.SMTP_PASSWORD
        self.mail_from: str = config_smtp.MAIL_FROM

    def send_email(self, dto: EmailDTO) -> None:
        message = self._templatize(dto)
        try:
            with SMTP_SSL(self.host, self.port) as smtp:
                smtp.login(user=self.mail_from, password=self.password)
                smtp.send_message(message)
        except SMTPException:
            raise SendEmailError("Error when sending a email")

    def _templatize(self, dto: EmailDTO) -> EmailMessage:
        message = EmailMessage()
        message["Subject"] = dto.subject
        message["From"] = self.mail_from
        message["To"] = dto.recipient_email
        context = dto.template.render(**dto.data)
        message.set_content(context, subtype="html")

        return message


dto = EmailDTO(
    template_path="account_activation.html",
    email_subject="Account activation",
    recipient="danil.taimulin@yandex.ru",
    context={"email": "123123213", "code": "123123123"},
)

client = EmailClient()

client.send_email(dto)
