import requests
from functools import wraps
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)


def validate_azure_token(token):
    """
    Validate Azure AD token using Microsoft Graph API.

    Args:
        token (str): The Bearer token to validate

    Returns:
        tuple: (bool, dict) - (is_valid, user_info)
        If token is invalid, user_info will contain error message
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

        if response.status_code != 200:
            logger.error(f"Token validation failed: {response.status_code} - {response.text}")
            return False, {"error": "Invalid token", "details": response.text}

        user_info = response.json()
        return True, user_info

    except Exception as e:
        logger.error(f"Error validating token: {str(e)}")
        return False, {"error": "Token validation failed", "details": str(e)}


def verify_token(token):
    """
    Simple wrapper around validate_azure_token that returns only the boolean result.
    Used by WebSocket authentication.
    """
    is_valid, _ = validate_azure_token(token)
    return is_valid


def require_auth(f):
    """
    Decorator for routes that require authentication.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid authorization header"}), 401

        token = auth_header.split(' ')[1]
        is_valid, user_info = validate_azure_token(token)

        if not is_valid:
            return jsonify(user_info), 401

        # Add user info to request context
        request.user_info = user_info
        return f(*args, **kwargs)

    return decorated