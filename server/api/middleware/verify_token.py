from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException
import jwt

SECRET_KEY = 'secret-key'
ALGORITHM = "HS256"


class TokenAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude certain paths from token verification
        if request.url.path in ["/sign-up", "/sign-in"]:
            return await call_next(request)

        # Token extraction and verification as shown earlier
        token = request.headers.get('Authorization')
        if token is None:
            return JSONResponse(
                status_code=401, content={"detail": "Authorization header missing"})

        token = token.replace("Bearer ", "")

        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={
                                "detail": "Token has expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={
                                "detail": "Invalid token"})

        response = await call_next(request)
        return response
