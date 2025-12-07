
class CustomException(Exception):
    """Base class for custom exceptions."""
    def __init__(self, detail: str):
        self.detail = detail


class ConfigurationMissingException(CustomException):
    """Exception raised for configuration"""
    def __init__(self, config_name: str):
        super().__init__(detail=f"Configuration '{config_name}' is missing.")


class AuthenticationFailedException(CustomException):
    """Exception raised for Authentication failures"""
    def __init__(self, reason: str):
        super().__init__(detail=f"Authentication failed: {reason}.")


class CapchaValidationFailedException(CustomException):
    """Exception raised for errors during CAPTCHA validation."""
    def __init__(self, detail: str = "An error occurred during CAPTCHA validation."):
        super().__init__(detail=detail)


class CapchaSolvingFailedException(CustomException):
    """Exception raised when CAPTCHA solving fails."""
    def __init__(self, detail: str = "CAPTCHA solving failed."):
        super().__init__(detail=detail)


# DB related Exception

class DatabaseConnectionException(CustomException):
    def __init__(self, detail: str = "Failed to connect to the database."):
        super().__init__(detail=detail)


class DatabaseQueryException(CustomException):
    def __init__(self, detail: str = "Database query failed."):
        super().__init__(detail=detail)


class RecordNotFoundException(CustomException):
    def __init__(self, record_id: str):
        super().__init__(detail=f"Record with ID '{record_id}' not found.")


class DuplicateRecordException(CustomException):
    def __init__(self, detail: str = "Duplicate record found."):
        super().__init__(detail=detail)


class TransactionException(CustomException):
    def __init__(self, detail: str = "Database transaction failed."):
        super().__init__(detail=detail)


class DataValidationException(CustomException):
    def __init__(self, detail: str = "Data validation failed."):
        super().__init__(detail=detail)


# RabbitMq related Exception


class RabbitMQConnectionException(CustomException):
    def __init__(self, detail: str = "Failed to connect to RabbitMQ."):
        super().__init__(detail=detail)


class RabbitMQPublishException(CustomException):
    def __init__(self, detail: str = "Failed to publish message to RabbitMQ."):
        super().__init__(detail=detail)


class RabbitMQConsumeException(CustomException):
    def __init__(self, detail: str = "Failed to consume message from RabbitMQ."):
        super().__init__(detail=detail)


class MessageProcessingException(CustomException):
    def __init__(self, detail: str = "Error processing the message."):
        super().__init__(detail=detail)


class QueueNotFoundException(CustomException):
    def __init__(self, queue_name: str):
        super().__init__(detail=f"Queue '{queue_name}' not found.")


class MessageAcknowledgmentException(CustomException):
    def __init__(self, detail: str = "Failed to acknowledge the message."):
        super().__init__(detail=detail)


class SMTPConnectionException(Exception):
    def __init__(self, message: str = "Failed to connect to the SMTP server."):
        super().__init__(message)


class SMTPAuthenticationException(Exception):
    def __init__(self, message: str = "SMTP authentication failed."):
        super().__init__(message)


class SMTPRecipientException(Exception):
    def __init__(self, message: str = "SMTP recipients were refused."):
        super().__init__(message)


class SMTPSenderException(Exception):
    def __init__(self, message: str = "SMTP sender was refused."):
        super().__init__(message)


class SMTPDataException(Exception):
    def __init__(self, message: str = "SMTP server refused the email data."):
        super().__init__(message)


class InvalidArgumentsException(Exception):
    """Exception raised for invalid or missing arguments."""
    def __init__(self, message="Invalid or missing arguments provided."):
        self.message = message
        super().__init__(self.message)
