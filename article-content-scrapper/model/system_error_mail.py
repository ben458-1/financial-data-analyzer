from typing import Optional

from pydantic import BaseModel, Field

from interface.email import EmailInterface
from datetime import datetime, timezone
from core.config import data_source as ds
import os


class SystemErrorEMailTemplate(EmailInterface):
    def get_subject(self, context: dict) -> str:
        return "🚨 Spokesperson Alert – System Failure Detected"

    def get_template_name(self) -> str:
        return os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            f"mail_templates{os.sep}system_error_email_template.html")

    def prepare_context(self, raw_data: dict) -> dict:
        return raw_data


def current_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class SysErrorModel(BaseModel):
    type: str
    component: Optional[str] = ''
    message: str
    time: str = Field(default_factory=current_utc_iso)
    environment: Optional[str] = ds.STAGE
    stack_trace: str
    year: int = Field(default_factory=lambda: datetime.now().year)
