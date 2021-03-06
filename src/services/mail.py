import smtplib
from email.message import EmailMessage
from typing import Any

from core.config import SENDER_MAIL, SENDER_PASSWORD, TEMPLATE_DIR
from jinja2 import Environment, FileSystemLoader


class MailService:
    def __init__(self):

        self.env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        self.template = self.env.get_template("email.html")

    def send_email(self, email: str, link: str, operation: str, data: Any) -> None:

        self.message = EmailMessage()
        self.message["To"] = email
        self.message["Subject"] = f"Novardis бронирование"

        output = self.template.render(
            **{
                "link": link,
                "operation": operation,
                "data": data,
            }
        )

        self.message.add_alternative(output, subtype="html")

        self._send(email)

    def _send(self, to: str) -> None:
        mailserver = smtplib.SMTP("smtp.office365.com", 587)
        mailserver.starttls()
        mailserver.login(SENDER_MAIL, SENDER_PASSWORD)

        mailserver.sendmail(SENDER_MAIL, to, self.message.as_string())
        mailserver.quit()
