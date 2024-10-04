import time

import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.settings import settings

JWT_ALGORITHM = "HS256"

class JWTTokenPayload(BaseModel):
    iss: str
    sub: str
    exp: int
    iat: int


class JWTToken(BaseModel):
    payload: JWTTokenPayload
    access_token: str


def create_jwt_token(user_id: str) -> JWTToken:
    iat = int(time.time())
    exp = iat + settings.security.ACCESS_TOKEN_LIFETIME

    token_payload = JWTTokenPayload(
        iss=settings.security.JWT_ISSUER,
        sub=user_id,
        exp=exp,
        iat=iat,
    )

    access_token = jwt.encode(
        token_payload.model_dump(),
        key=settings.security.JWT_SECRET_KEY.get_secret_value(),
        algorithm=JWT_ALGORITHM,
    )

    return JWTToken(payload=token_payload, access_token=access_token)


def verify_jwt_token(token: str) -> JWTTokenPayload:
    try:
        raw_payload = jwt.decode(
            token,
            settings.security.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[JWT_ALGORITHM],
            options={"verify_signature": True},
            issuer=settings.security.JWT_ISSUER,
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalid: {e}",
        )

    return JWTTokenPayload(**raw_payload)
