require('dotenv').config();

const requiredVars = ['JWT_SECRET'];
for (const v of requiredVars) {
  if (!process.env[v]) {
    console.error(`FATAL: Missing required environment variable: ${v}`);
    process.exit(1);
  }
}

module.exports = {
  port: parseInt(process.env.PORT, 10) || 5000,
  jwtSecret: process.env.JWT_SECRET,
  frontendUrl: process.env.FRONTEND_URL || 'http://localhost:3000',
  nodeEnv: process.env.NODE_ENV || 'development',
};
