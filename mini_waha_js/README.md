# Mini WAHA JS

Lean WhatsApp HTTP API using [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js).

## Prerequisites
- Node.js 18+
- Python 3.10+

## Setup
```bash
cd mini_waha_js
cp node/.env.example node/.env # edit BASIC_USER/BASIC_PASS
```

## Run
- Linux/macOS: `./start.sh`
- Windows: `start.bat`

First run installs dependencies automatically. Scan the QR at [http://localhost:8000/qr](http://localhost:8000/qr).

## Sample requests
```bash
curl http://localhost:8000/health
curl -u admin:admin -X POST http://localhost:8000/sendText \
  -H "Content-Type: application/json" \
  -d '{"chatId":"<phone>@c.us","text":"Hello"}'
```

> Personal use only. WhatsApp may restrict accounts for automation abuse.
