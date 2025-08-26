const axios = require('axios');
const { WEBHOOK_URL } = require('./config');
const { log } = require('./logger');

async function sendMessageEvent(msg) {
  if (!WEBHOOK_URL) return;
  const payload = {
    type: 'message',
    data: {
      id: msg.id._serialized,
      chatId: msg.from,
      fromMe: msg.fromMe,
      text: msg.body,
      ts: msg.timestamp
    }
  };
  try {
    await axios.post(WEBHOOK_URL, payload);
  } catch (err) {
    try {
      await axios.post(WEBHOOK_URL, payload);
    } catch (err2) {
      log('Webhook error', err2.message);
    }
  }
}

module.exports = {
  sendMessageEvent
};
