'use strict';

const dns = require('dns');
dns.setServers(['8.8.8.8', '8.8.4.4']);

const mongoose = require('mongoose');
const config = require('./env');


async function connectDB() {
  try {
    await mongoose.connect(config.mongoUri);
    console.log('[LabelSetu] MongoDB connected successfully.');
  } catch (err) {
    console.error('[LabelSetu] MongoDB connection failed:', err.message);
    process.exit(1);
  }
}

module.exports = { connectDB };
