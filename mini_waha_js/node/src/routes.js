const express = require('express');
const basicAuth = require('express-basic-auth');
const helmet = require('helmet');
const cors = require('cors');
const multer = require('multer');
const fs = require('fs');
const os = require('os');
const wa = require('./wa');
const { BASIC_USER, BASIC_PASS, WEBHOOK_URL } = require('./config');
const { sendMessageEvent } = require('./webhook');
const { logger } = require('./logger');

function createApp() {
  const app = express();
  const upload = multer({ dest: os.tmpdir() });

  app.use(helmet());
  app.use(cors());
  app.use(express.json());
  app.use(logger);

  app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
  });

  app.get('/qr', async (req, res) => {
    if (wa.getState() !== 'qr') return res.sendStatus(204);
    const png = await wa.getQrPng();
    res.type('png').send(png);
  });

  app.use(basicAuth({ users: { [BASIC_USER]: BASIC_PASS }, challenge: true }));

  app.get('/status', (req, res) => {
    res.json({ state: wa.getState() });
  });

  app.post('/sendText', async (req, res) => {
    const { chatId, text } = req.body || {};
    if (!chatId || !text) return res.status(400).json({ error: 'chatId and text required' });
    try {
      const messageId = await wa.sendText(chatId, text);
      res.json({ ok: true, messageId });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/sendImage', upload.single('media'), async (req, res) => {
    const { chatId, caption } = req.body || {};
    if (!chatId || !req.file) {
      if (req.file) fs.unlink(req.file.path, () => {});
      return res.status(400).json({ error: 'chatId and media required' });
    }
    try {
      const messageId = await wa.sendImage(chatId, req.file.path, caption);
      res.json({ ok: true, messageId });
    } catch (err) {
      res.status(500).json({ error: err.message });
    } finally {
      fs.unlink(req.file.path, () => {});
    }
  });

  app.get('/chats', async (req, res) => {
    const { query = '', limit = 20 } = req.query;
    try {
      const chats = await wa.getChats(query, parseInt(limit, 10));
      res.json(chats);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  app.get('/messages/:chatId', async (req, res) => {
    const { chatId } = req.params;
    const { limit = 50 } = req.query;
    try {
      const msgs = await wa.getMessages(chatId, parseInt(limit, 10));
      res.json(msgs);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/webhook/test', async (req, res) => {
    if (!WEBHOOK_URL) return res.status(400).json({ error: 'WEBHOOK_URL not set' });
    await sendMessageEvent({
      id: { _serialized: 'test' },
      from: 'test@c.us',
      fromMe: false,
      body: 'test',
      timestamp: Math.floor(Date.now() / 1000)
    });
    res.json({ ok: true });
  });

  return app;
}

module.exports = createApp;
