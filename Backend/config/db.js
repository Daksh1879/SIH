'use strict';

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
