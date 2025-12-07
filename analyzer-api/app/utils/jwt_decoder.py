# app/utils/jwt_decoder.py

from jose import jwt, JWTError

SECRET_KEY = "your-super-secret-key"  # Use env variable in production
ALGORITHM = "HS256"  # Or RS256 if using public/private keys


def extract_user_id_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return str(payload.get("user_id", "anonymous"))
    except JWTError:
        return "anonymous"
