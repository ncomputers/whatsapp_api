const path = require('path');
const dotenv = require('dotenv');

dotenv.config({ path: path.join(__dirname, '..', '.env') });

const PORT = process.env.PORT || 8000;
const BIND = process.env.BIND || '0.0.0.0';
const BASIC_USER = process.env.BASIC_USER || 'admin';
const BASIC_PASS = process.env.BASIC_PASS || 'admin';
const WEBHOOK_URL = process.env.WEBHOOK_URL || '';

const AUTH_DIR = '.wwebjs_auth';

module.exports = {
  PORT,
  BIND,
  BASIC_USER,
  BASIC_PASS,
  WEBHOOK_URL,
  AUTH_DIR
};
