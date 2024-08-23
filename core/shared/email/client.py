from email.message import EmailMessage
from smtplib import SMTP_SSL, SMTPException

from src.config.email.smtp_config import config_smtp

from .email_dto import EmailDTO
from .exceptions import SendEmailError
from .jinja import env


class EmailClient:
    """Класс для обработки почтовых сообщений"""

    def __init__(
        self,
        smtp_port: int = config_smtp.SMTP_PORT,
        smtp_host: str = config_smtp.SMTP_HOST,
        smtp_password: str = config_smtp.SMTP_PASSWORD,
        mail_from: str = config_smtp.MAIL_FROM,
    ) -> None:
        self.port = smtp_port
        self.host = smtp_host
        self.password = smtp_password
        self.mail_from = mail_from

    def send_email(self, dto: EmailDTO) -> None:
        message = self._templatize(dto.template_path, dto.recipient, dto.email_subject, dto.context)
        try:
            with SMTP_SSL(self.host, self.port) as smtp:
                smtp.login(self.mail_from, self.password)
                smtp.send_message(message)
        except SMTPException:
            raise SendEmailError("Error when sending a email")

    def _templatize(self, template_path: str, recipient_email: str, subject: str, data: dict[str, str]) -> EmailMessage:
        template = env.get_template(template_path)
        context = template.render(**data)
        return self._get_email_template(recipient_email, subject, context)

    def _get_email_template(self, recipient_email: str, subject: str, body: str) -> EmailMessage:
        email = EmailMessage()
        email["Subject"] = subject
        email["From"] = self.mail_from
        email["To"] = recipient_email

        email.set_content(body, subtype="html")
        return email
