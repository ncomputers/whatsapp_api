const morgan = require('morgan');

const logger = morgan('combined');

function log(...args) {
  console.log(new Date().toISOString(), ...args);
}

module.exports = {
  logger,
  log
};
