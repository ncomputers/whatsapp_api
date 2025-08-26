const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode');
const qrcodeTerminal = require('qrcode-terminal');
const { AUTH_DIR } = require('./config');
const { log } = require('./logger');

let client;
let latestQr = null;
let state = 'connecting';

async function init(events) {
  client = new Client({
    authStrategy: new LocalAuth({ dataPath: AUTH_DIR }),
    puppeteer: {
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
  });

  client.on('qr', (qr) => {
    latestQr = qr;
    state = 'qr';
    qrcodeTerminal.generate(qr, { small: true });
    events?.onQr?.(qr);
  });

  client.on('ready', () => {
    state = 'ready';
    log('WhatsApp ready');
    events?.onReady?.();
  });

  client.on('message', (msg) => {
    events?.onMessage?.(msg);
  });

  client.on('disconnected', (reason) => {
    log('WhatsApp disconnected', reason);
    state = 'connecting';
    client.initialize();
  });

  await client.initialize();
}

function getState() {
  return state;
}

async function getQrPng() {
  if (!latestQr) return null;
  return await qrcode.toBuffer(latestQr);
}

async function sendText(chatId, text) {
  const msg = await client.sendMessage(chatId, text);
  return msg.id._serialized;
}

async function sendImage(chatId, filePath, caption) {
  const media = await MessageMedia.fromFilePath(filePath);
  const msg = await client.sendMessage(chatId, media, { caption });
  return msg.id._serialized;
}

async function getChats(query = '', limit = 20) {
  const chats = await client.getChats();
  return chats
    .filter((c) => !query || c.name.toLowerCase().includes(query.toLowerCase()))
    .slice(0, limit)
    .map((c) => ({ chatId: c.id._serialized, name: c.name }));
}

async function getMessages(chatId, limit = 50) {
  const chat = await client.getChatById(chatId);
  const msgs = await chat.fetchMessages({ limit });
  return msgs.map((m) => ({
    id: m.id._serialized,
    chatId: chatId,
    fromMe: m.fromMe,
    text: m.body,
    ts: m.timestamp
  }));
}

module.exports = {
  init,
  getState,
  getQrPng,
  sendText,
  sendImage,
  getChats,
  getMessages
};
