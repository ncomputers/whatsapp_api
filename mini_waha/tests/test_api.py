import os
import sys
import pytest
from httpx import AsyncClient, ASGITransport

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.main import app
from app.auth import init_rate_limiter

init_rate_limiter(app)


class DummyController:
    async def is_ready(self):
        return True

    async def get_qr_png(self):
        return b"123"

    async def send_text(self, chat_id: str, text: str):
        return "msg"

    async def send_image(self, chat_id: str, path: str, caption: str | None = None):
        return "msg"

    async def get_chats(self, query=None, limit=20):
        return []

    async def get_messages(self, chat_id: str, limit: int = 50):
        return []


@pytest.fixture(autouse=True)
def override_controller():
    app.router.on_startup.clear()
    app.router.on_shutdown.clear()
    app.state.controller = DummyController()
    yield


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["ready"] is True


@pytest.mark.asyncio
async def test_status_and_qr():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/api/status")
        assert resp.status_code == 200
        resp = await ac.get("/api/qr")
        assert resp.status_code == 204


@pytest.mark.asyncio
async def test_send_text():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/sendText",
            json={"chatId": "123@c.us", "text": "hi"},
            auth=("admin", "admin"),
        )
        assert resp.status_code == 200
        assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_rate_limit():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for _ in range(35):
            await ac.get("/api/health")
        resp = await ac.get("/api/health")
        assert resp.status_code == 429
