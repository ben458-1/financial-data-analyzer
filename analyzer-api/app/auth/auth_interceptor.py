# auth.py
from fastapi import Request, HTTPException
from functools import wraps
import re
import requests
import logging
import msal
import os
from app.core.config import data_source

from app.db.orm_models import APIKey  # make sure this works with your ORM

logger = logging.getLogger(__name__)

AZURE_TENANT_ID = data_source.AZURE_TENANT_ID
AZURE_CLIENT_ID = data_source.AZURE_CLIENT_ID
AZURE_CLIENT_SECRET = data_source.AZURE_CLIENT_SECRET


def get_authority():
    return f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"


def require_auth(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        request: Request = kwargs.get("request")
        if not request:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
        if not request:
            raise RuntimeError("Request object not found")

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing authorization header")

        try:
            if auth_header.startswith('ApiKey '):
                api_key = auth_header.split(' ')[1]
                key_obj = APIKey.get_active_key(api_key)

                if not key_obj:
                    raise HTTPException(status_code=401, detail="Invalid or expired API key")

                current_path = request.url.path.lstrip('/')
                for pattern in key_obj.allowed_endpoints:
                    regex_pattern = pattern.replace('*', '.*').replace('/', '\\/')
                    if re.match(f"^{regex_pattern}$", current_path):
                        key_obj.update_last_used()
                        return await f(*args, **kwargs)

                raise HTTPException(status_code=403, detail="Endpoint not allowed for this API key")

            elif auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                app = msal.ConfidentialClientApplication(
                    AZURE_CLIENT_ID,
                    authority=get_authority(),
                    client_credential=AZURE_CLIENT_SECRET
                )

                headers = {"Authorization": f"Bearer {token}"}
                response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

                if response.status_code != 200:
                    raise HTTPException(status_code=401, detail="Invalid token")

                request.state.user_info = response.json()

            else:
                raise HTTPException(status_code=401, detail="Unsupported authorization scheme")

        except Exception as e:
            logger.exception("Auth failed")
            raise HTTPException(status_code=401, detail=str(e))

        return f(*args, **kwargs)

    return decorated


def auth_required(validate_azure_token):
    def decorator(f):
        @wraps(f)
        async def decorated(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            if not request:
                raise RuntimeError("Request object not found")

            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

            token = auth_header.split(" ")[1]
            is_valid, user_info = validate_azure_token(token)

            if not is_valid:
                raise HTTPException(status_code=401, detail=user_info)

            request.state.user_info = user_info
            return await f(*args, **kwargs)

        return decorated

    return decorator
