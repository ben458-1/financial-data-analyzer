from fastapi import APIRouter, Request
from app.auth.auth_interceptor import require_auth

app = APIRouter(prefix="/app/v1", tags=["app:v1.0.0"])


@app.get("/auth/user/userinfo")
@require_auth
def get_user(request: Request):
    return request.state.user_info
