import uvicorn
from .config import settings


def main() -> None:
    uvicorn.run("app.main:app", host=settings.bind, port=settings.port)


if __name__ == "__main__":
    main()
