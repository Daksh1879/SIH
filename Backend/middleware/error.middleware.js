const { nodeEnv } = require('../config/env');
const { error: errorResponse } = require('../utils/apiResponse');

function notFound(req, res, next) {
  res.status(404).json(errorResponse(`Route not found: ${req.method} ${req.originalUrl}`));
}

function errorHandler(err, req, res, next) {
  let statusCode = err.statusCode || 500;
  let message = err.message || 'Something went wrong.';

  // Multer file-size error
  if (err.code === 'LIMIT_FILE_SIZE') {
    statusCode = 400;
    message = 'File too large. Maximum allowed size is 5MB.';
  }

  // Multer unexpected field
  if (err.code === 'LIMIT_UNEXPECTED_FILE') {
    statusCode = 400;
    message = 'Unexpected file field. Use the field name "image".';
  }

  // Malformed JSON body
  if (err.type === 'entity.parse.failed') {
    statusCode = 400;
    message = 'Invalid JSON in request body.';
  }

  // In production, hide internal error details
  if (statusCode === 500 && nodeEnv !== 'development') {
    message = 'An unexpected error occurred.';
  }

  if (nodeEnv === 'development' && statusCode === 500) {
    console.error('[ERROR]', err);
  }

  res.status(statusCode).json(errorResponse(message));
}

module.exports = { notFound, errorHandler };
