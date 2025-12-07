from fastapi import Request, FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.utils.jwt_decoder import extract_user_id_from_token


def get_custom_key_func():
    def key_func(request: Request):
        auth_header = request.headers.get("Authorization")
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user: {user_id}"

        api_key = request.headers.get('X-API-Key')
        if api_key:
            return f"apikey:{api_key}"

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            user_id = extract_user_id_from_token(token)
            return f"user:{user_id}"

        return get_remote_address(request)

    return key_func


class RateLimiterService:
    def __init__(self):
        self.limiter = Limiter(key_func=get_custom_key_func())

    def init_app(self, app: FastAPI):
        app.state.limiter = self.limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        app.add_middleware(SlowAPIMiddleware)

    def limit(self, limit_str: str):
        return self.limiter.limit(limit_str)
