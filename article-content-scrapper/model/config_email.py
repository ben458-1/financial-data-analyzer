from interface.email import EmailInterface
import datetime
import os


class ConfigErrorEmailTemplate(EmailInterface):
    def get_subject(self, context: dict) -> str:
        return f"🚨 Spokesperson Alert: Missing {context.get('newspaper_name')} Configuration"

    def get_template_name(self) -> str:
        return os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            f"mail_templates{os.sep}config_error_template.html")

    def prepare_context(self, raw_data: dict) -> dict:
        raw_data["year"] = datetime.datetime.now().year
        return raw_data
