import secrets
from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .config import settings

security = HTTPBasic()
limiter = Limiter(key_func=get_remote_address)


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """Validate HTTP Basic auth credentials."""
    is_valid = secrets.compare_digest(credentials.username, settings.basic_user) and secrets.compare_digest(
        credentials.password, settings.basic_pass
    )
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Basic"})
    return credentials.username


def init_rate_limiter(app: FastAPI) -> None:
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
