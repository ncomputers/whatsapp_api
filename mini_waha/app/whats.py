from __future__ import annotations
import asyncio
from pathlib import Path
from typing import List
from playwright.async_api import async_playwright, Page, BrowserContext

from .config import settings
from .models import Chat, Message
from .logger import logger


class WhatsAppWebController:
    """Minimal controller around WhatsApp Web using Playwright."""

    def __init__(self) -> None:
        self._playwright = None
        self.browser: BrowserContext | None = None
        self.page: Page | None = None

    async def start(self) -> None:
        self._playwright = await async_playwright().start()
        self.browser = await self._playwright.chromium.launch_persistent_context(
            settings.user_data_dir, headless=settings.headless
        )
        self.page = await self.browser.new_page()
        await self.page.goto("https://web.whatsapp.com/")
        await self.page.wait_for_load_state("networkidle")
        logger.info("WhatsApp Web started")

    async def stop(self) -> None:
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def is_ready(self) -> bool:
        if not self.page:
            return False
        return bool(await self.page.query_selector("div[role='grid']"))

    async def get_qr_png(self) -> bytes:
        if not self.page:
            return b""
        canvas = await self.page.query_selector("canvas")
        if canvas:
            return await canvas.screenshot()
        return await self.page.screenshot()

    async def send_text(self, chat_id: str, text: str) -> str:
        if not self.page:
            raise RuntimeError("Controller not started")
        phone = chat_id.split("@")[0]
        await self.page.goto(f"https://web.whatsapp.com/send?phone={phone}")
        await self.page.wait_for_selector("div[contenteditable='true']")
        box = await self.page.query_selector("div[contenteditable='true']")
        await box.fill(text)
        await box.press("Enter")
        return "local-msg-id"

    async def send_image(self, chat_id: str, path: str, caption: str | None = None) -> str:
        if not self.page:
            raise RuntimeError("Controller not started")
        phone = chat_id.split("@")[0]
        await self.page.goto(f"https://web.whatsapp.com/send?phone={phone}")
        await self.page.wait_for_selector("div[contenteditable='true']")
        await self.page.set_input_files("input[type=file]", path)
        if caption:
            box = await self.page.query_selector("div[contenteditable='true']")
            await box.fill(caption)
        await self.page.keyboard.press("Enter")
        return "local-msg-id"

    async def get_chats(self, query: str | None = None, limit: int = 20) -> List[Chat]:
        return []

    async def get_messages(self, chat_id: str, limit: int = 50) -> List[Message]:
        return []
