const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const config = require('./config/env');
const { success } = require('./utils/apiResponse');
const { notFound, errorHandler } = require('./middleware/error.middleware');

const authRoutes = require('./routes/auth.routes');
const verifyRoutes = require('./routes/verify.routes');
const dashboardRoutes = require('./routes/dashboard.routes');

const app = express();

// Security headers
app.use(helmet());

// CORS — allowed origins for local development
const ALLOWED_ORIGINS = [
  config.frontendUrl,
  'http://localhost:3000',
  'http://127.0.0.1:5500',
  'http://127.0.0.1:3000',
  null, // file:// protocol sends Origin: null
];
app.use(cors({
  origin: (origin, cb) => {
    if (!origin || ALLOWED_ORIGINS.includes(origin)) return cb(null, true);
    cb(new Error(`CORS: origin ${origin} not allowed`));
  },
  credentials: true,
}));

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// General rate limiter
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 200,
  standardHeaders: true,
  legacyHeaders: false,
  message: { success: false, error: { message: 'Too many requests. Please try again later.' } },
});

// Stricter limiter for upload/OCR route
const uploadLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 30,
  standardHeaders: true,
  legacyHeaders: false,
  message: { success: false, error: { message: 'Upload limit reached. Please wait before uploading again.' } },
});

app.use('/api', generalLimiter);
app.use('/api/verify/upload', uploadLimiter);

// Health check
app.get('/api/health', (req, res) => {
  res.status(200).json(success({ message: 'LabelSetu API is running' }));
});

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/verify', verifyRoutes);
app.use('/api/dashboard', dashboardRoutes);

// Error handlers — must be last
app.use(notFound);
app.use(errorHandler);

module.exports = app;