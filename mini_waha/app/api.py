from fastapi import APIRouter, Depends, Request, UploadFile, File, Form
from fastapi.responses import Response, StreamingResponse

from .auth import basic_auth, limiter
from .config import settings
from .models import SendTextRequest, Chat, Message, WebhookEvent
from .whats import WhatsAppWebController
from .store import fetch_messages
from .webhooks import deliver

router = APIRouter(prefix="/api")


def get_controller(request: Request) -> WhatsAppWebController:
    return request.app.state.controller


@router.get("/health")
@limiter.limit(settings.rate_limit)
async def health(request: Request, controller: WhatsAppWebController = Depends(get_controller)) -> dict:
    ready = await controller.is_ready()
    return {"status": "ok", "ready": ready}


@router.get("/status")
@limiter.limit(settings.rate_limit)
async def status(request: Request, controller: WhatsAppWebController = Depends(get_controller)) -> dict:
    ready = await controller.is_ready()
    state = "ready" if ready else "qr"
    return {"state": state, "headless": settings.headless}


@router.get("/qr")
@limiter.limit(settings.rate_limit)
async def qr(request: Request, controller: WhatsAppWebController = Depends(get_controller)) -> Response:
    if await controller.is_ready():
        return Response(status_code=204)
    png = await controller.get_qr_png()
    return StreamingResponse(iter([png]), media_type="image/png")


@router.post("/sendText")
@limiter.limit(settings.rate_limit)
async def send_text(
    request: Request,
    payload: SendTextRequest,
    user: str = Depends(basic_auth),
    controller: WhatsAppWebController = Depends(get_controller),
) -> dict:
    msg_id = await controller.send_text(payload.chatId, payload.text)
    return {"ok": True, "messageId": msg_id}


@router.post("/sendImage")
@limiter.limit(settings.rate_limit)
async def send_image(
    request: Request,
    chatId: str = Form(...),
    caption: str | None = Form(None),
    file: UploadFile = File(...),
    user: str = Depends(basic_auth),
    controller: WhatsAppWebController = Depends(get_controller),
) -> dict:
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    msg_id = await controller.send_image(chatId, path, caption)
    return {"ok": True, "messageId": msg_id}


@router.get("/chats")
@limiter.limit(settings.rate_limit)
async def chats(
    request: Request,
    query: str | None = None,
    limit: int = 20,
    user: str = Depends(basic_auth),
    controller: WhatsAppWebController = Depends(get_controller),
) -> list[Chat]:
    return await controller.get_chats(query=query, limit=limit)


@router.get("/messages/{chat_id}")
@limiter.limit(settings.rate_limit)
async def messages(
    request: Request,
    chat_id: str,
    limit: int = 50,
    user: str = Depends(basic_auth),
) -> list[Message]:
    msgs = await fetch_messages(chat_id, limit)
    return msgs


@router.post("/webhook/test")
@limiter.limit(settings.rate_limit)
async def webhook_test(request: Request, user: str = Depends(basic_auth)) -> dict:
    event = WebhookEvent(type="message", data=Message(id="test", chatId="0", fromMe=False, text="test", media=False, ts=0))
    await deliver(event)
    return {"sent": True}
