
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException
import jwt

SECRET_KEY = 'secret-key'
ALGORITHM = "HS256"


class TokenAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude certain paths from token verification
        if request.url.path in ["/register", "/login"]:
            return await call_next(request)

        # Token extraction and verification as shown earlier
        token = request.headers.get('Authorization')
        if token is None:
            raise HTTPException(
                status_code=401, detail="Authorization header missing")

        token = token.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # request.state.user = payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        response = await call_next(request)
        return response
