# Mini WAHA

Minimal self-hosted API for controlling WhatsApp Web using Python & Playwright.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
python -m app
```

Visit `/qr` to pair your device. After it shows *ready* you can send messages.

Example:

```bash
curl -u admin:admin -X POST http://localhost:8000/api/sendText \
  -H "Content-Type: application/json" \
  -d '{"chatId":"<phone>@c.us","text":"Hello!"}'
```

## Notes

- Store data in local SQLite database `mini_waha.db`.
- Basic auth credentials configured via environment variables.
- Rate limiting uses in-memory SlowAPI.
- Logging written to `logs/app.log`.

Use responsibly; heavy automation may violate WhatsApp terms.
