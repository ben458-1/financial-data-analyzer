import os
import smtplib  # Import smtplib for SMTP connections
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging.handlers import SMTPHandler
from jinja2 import Environment, FileSystemLoader


class SMTPLOGHandler(SMTPHandler):
    def __init__(self, *args, template_name='log_template.html', **kwargs):
        super().__init__(*args, **kwargs)
        self.error_line = None
        self.template_name = template_name
        self.env = Environment(loader=FileSystemLoader(f'{os.path.dirname(__file__)}'))
        self.subject = 'Error Alert: Please Review Spokesperson Application Issue'

    def emit(self, record) -> None:
        # Load the template
        template = self.env.get_template(self.template_name)
        self.error_line = record.lineno
        error_stack_len = len(record.exc_info)
        if error_stack_len > 0:
            tb = record.exc_info[error_stack_len - 1]
            if tb is not None:
                while tb.tb_next is not None:
                    tb = tb.tb_next
                self.error_line = tb.tb_lineno
        # Prepare the email data
        err = {
            'subject': self.subject,
            'stacktrace': record.exc_text,
            'message': record.message,
            'levelname': record.levelname,
            'name': record.name,
            'pathname': record.pathname,
            'lineno': self.error_line,
            'exc_info': record.exc_info if record.exc_info else None,
            'newspaper_id': getattr(record, 'newspaper_id', 'N/A'),
            'article_id': getattr(record, 'article_id', 'N/A'),
            'newspaper_name': getattr(record, 'newspaper_name', 'oops'),
            'newspaper_url': getattr(record, 'newspaper_url', 'https://www.google.com/'),
            'article_url': getattr(record, 'article_url', 'https://www.google.com/'),
            'time': record.asctime
        }

        # Render the email content
        body = template.render(err=err)

        # Send the email
        self.send_email(body)

    def formatMessage(self):
        """Format the message for the email."""
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = ', '.join(self.toaddrs)
        msg['Subject'] = self.subject

        # Set email priority to high
        msg['X-Priority'] = '1'  # 1 = High priority
        msg['X-MSMail-Priority'] = 'High'
        return msg

    def send_email(self, body):
        # Create the email message
        msg = self.formatMessage()
        msg.attach(MIMEText(body, 'html'))  # Attach the rendered body
        # Create an SMTP connection and send the email
        try:
            with smtplib.SMTP(self.mailhost, self.mailport) as server:
                server.sendmail(self.fromaddr, self.toaddrs, msg.as_string())
        except Exception as e:
            # Handle any exceptions that occur during sending
            print(f"Failed to send email: {e}")
            raise e
