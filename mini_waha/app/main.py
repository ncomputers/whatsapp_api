from fastapi import FastAPI

from .api import router
from .auth import init_rate_limiter
from .whats import WhatsAppWebController
from .store import init_db
from .logger import logger

app = FastAPI()
controller = WhatsAppWebController()


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
    await controller.start()
    app.state.controller = controller
    init_rate_limiter(app)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await controller.stop()


app.include_router(router)
