'use strict';

const app = require('./app');
const config = require('./config/env');
const { connectDB } = require('./config/db');

async function start() {
  await connectDB();
  app.listen(config.port, () => {
    console.log(`[LabelSetu] Server running on port ${config.port} (${config.nodeEnv})`);
  });
}

start();
