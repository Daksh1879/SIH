const app = require('./app');
const config = require('./config/env');

app.listen(config.port, () => {
  console.log(`[LabelSetu] Server running on port ${config.port} (${config.nodeEnv})`);
});
