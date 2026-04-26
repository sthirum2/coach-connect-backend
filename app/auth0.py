import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from httpx import AsyncClient

token_auth_scheme = HTTPBearer()

async def get_jwks():
    domain = os.getenv("AUTH0_DOMAIN")
    async with AsyncClient() as client:
        response = await client.get(f"https://{domain}/.well-known/jwks.json")
        return response.json()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token = credentials.credentials
    domain = os.getenv("AUTH0_DOMAIN")
    audience = os.getenv("AUTH0_AUDIENCE")
    algorithms = os.getenv("AUTH0_ALGORITHMS", "RS256").split(",")

    try:
        jwks = await get_jwks()
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])
        payload = jwt.decode(
            token,
            key,
            algorithms=algorithms,
            audience=audience,
            issuer=f"https://{domain}/"
        )
        return payload
    except (JWTError, StopIteration):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
