const { PORT, BIND } = require('./config');
const createApp = require('./routes');
const wa = require('./wa');
const { log } = require('./logger');
const { sendMessageEvent } = require('./webhook');

const clientEvents = {
  onMessage: async (msg) => {
    await sendMessageEvent(msg);
  }
};

async function start() {
  await wa.init(clientEvents);
  const app = createApp();
  const server = app.listen(PORT, BIND, () => {
    log(`Listening on http://${BIND}:${PORT}`);
  });

  const shutdown = () => {
    log('Shutting down');
    server.close(() => process.exit(0));
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

start();
