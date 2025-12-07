import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from interface.email import EmailInterface
from logger import log
from core.config import data_source as ds
from exceptions import custom_exception as ce


class EmailService:
    MAX_RETRIES = 3
    INITIAL_DELAY = 2

    def __init__(self, from_address=None, priority=3, ms_mail_priority='Normal'):
        self.smtp_server = ds.SMTP_HOST
        self.smtp_port = ds.SMTP_PORT
        self.from_address = from_address or ds.SENDER_EMAIL
        self.priority = priority
        self.ms_mail_priority = ms_mail_priority

    def send_email_with_template(self, to_emails: str, data: dict, template_handler: EmailInterface):
        recipients = [email.strip() for email in to_emails.split(',') if email.strip()]

        context = template_handler.prepare_context(data)
        subject = template_handler.get_subject(context)

        template_dir = os.path.dirname(template_handler.get_template_name())
        template_file = os.path.basename(template_handler.get_template_name())

        html_body = Environment(loader=FileSystemLoader(template_dir)) \
            .get_template(template_file) \
            .render(context=context)

        msg = self._build_email_message(recipients, subject, html_body)

        log.log_info('Preparing email for sending')

        self._send_with_retries(recipients, msg)

    def _build_email_message(self, to_emails: list, subject: str, html_body: str) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg["From"] = self.from_address
        msg["To"] = ', '.join(to_emails)
        msg["Subject"] = subject
        msg["X-Priority"] = str(self.priority)
        msg["X-MSMail-Priority"] = str(self.ms_mail_priority)
        msg.attach(MIMEText(html_body, "html"))
        return msg

    def _send_with_retries(self, to_emails: list, msg: MIMEMultipart):
        delay = self.INITIAL_DELAY

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.sendmail(self.from_address, to_emails, msg.as_string())
                    log.log_info(f"Email sent successfully to {', '.join(to_emails)}")
                    return  # success, exit
            except Exception as err:
                error_type = type(err)

                if error_type in (
                        smtplib.SMTPConnectError,
                        smtplib.SMTPServerDisconnected,
                        ConnectionRefusedError
                ):
                    log.log_error(f"SMTP connection error on attempt {attempt}: {err}")
                    if attempt == self.MAX_RETRIES:
                        raise ce.SMTPConnectionException(str(err))
                    time.sleep(delay)
                    delay *= 2  # exponential backoff
                    continue

                exception_mapping = {
                    smtplib.SMTPAuthenticationError: ce.SMTPAuthenticationException,
                    smtplib.SMTPRecipientsRefused: ce.SMTPRecipientException,
                    smtplib.SMTPSenderRefused: ce.SMTPSenderException,
                    smtplib.SMTPDataError: ce.SMTPDataException,
                }

                exception_class = exception_mapping.get(error_type)

                if exception_class:
                    raise exception_class(str(err))

                log.log_error("Unexpected error during email sending", exception=err)
                raise
