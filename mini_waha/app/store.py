from __future__ import annotations
import json
from pathlib import Path
from typing import List
import aiosqlite

from .models import Message

DB_PATH = Path("mini_waha.db")

CREATE_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS messages(
        id TEXT PRIMARY KEY,
        chat_id TEXT,
        from_me INTEGER,
        text TEXT,
        media INTEGER,
        ts INTEGER
    )
    """,
    """CREATE TABLE IF NOT EXISTS last_seen(chat_id TEXT PRIMARY KEY, last_msg_id TEXT)""",
    """CREATE TABLE IF NOT EXISTS webhook_queue(id TEXT PRIMARY KEY, payload TEXT, retries INTEGER, next_attempt_ts INTEGER)""",
]


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        for stmt in CREATE_STATEMENTS:
            await db.execute(stmt)
        await db.commit()


async def save_message(msg: Message) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO messages(id, chat_id, from_me, text, media, ts) VALUES(?,?,?,?,?,?)",
            (msg.id, msg.chatId, int(msg.fromMe), msg.text, int(msg.media), msg.ts),
        )
        await db.commit()


async def fetch_messages(chat_id: str, limit: int = 50) -> List[Message]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, chat_id, from_me, text, media, ts FROM messages WHERE chat_id=? ORDER BY ts DESC LIMIT ?",
            (chat_id, limit),
        )
        rows = await cursor.fetchall()
    return [
        Message(id=r[0], chatId=r[1], fromMe=bool(r[2]), text=r[3], media=bool(r[4]), ts=r[5])
        for r in rows
    ]
