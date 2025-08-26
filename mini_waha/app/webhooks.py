from __future__ import annotations
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings
from .models import WebhookEvent
from .logger import logger


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def deliver(event: WebhookEvent) -> None:
    if not settings.webhook_url:
        return
    async with httpx.AsyncClient() as client:
        try:
            await client.post(settings.webhook_url, json=event.model_dump())
            logger.info("Webhook delivered", extra={"type": event.type})
        except Exception as exc:  # pragma: no cover
            logger.error(f"Webhook delivery failed: {exc}")
            raise
