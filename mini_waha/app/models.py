from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class SessionStatus(BaseModel):
    state: str
    ts: int


class SendTextRequest(BaseModel):
    chatId: str
    text: str


class SendMediaRequest(BaseModel):
    chatId: str
    caption: Optional[str] = None


class Chat(BaseModel):
    chatId: str
    name: str
    unread: int = 0


class Message(BaseModel):
    id: str
    chatId: str
    fromMe: bool
    text: Optional[str] = None
    media: bool = False
    ts: int


class WebhookEvent(BaseModel):
    type: str
    data: Message
