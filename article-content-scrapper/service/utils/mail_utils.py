from service.email_service import EmailService
from core.config import data_source as ds
from model import config_email as ce
from model import system_error_mail as sem
from logger import log


def config_missing_alert(context):
    initiate_email_service = EmailService()
    initiate_email_service.send_email_with_template(ds.UPDATE_RECIPIENT_EMAILS, context, ce.ConfigErrorEmailTemplate())


def system_error_alert(context):
    initiate_email_service = EmailService()
    initiate_email_service.send_email_with_template(ds.DEV_RECIPIENT_EMAILS, context, sem.SystemErrorEMailTemplate())
