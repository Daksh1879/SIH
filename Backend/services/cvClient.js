'use strict';

const fs = require('fs/promises');
const path = require('path');

const OCR_SERVICE_URL =
  process.env.OCR_SERVICE_URL || 'http://127.0.0.1:8000';

async function extractRegions(file) {
  if (!file || !file.path) {
    throw new Error('An uploaded image file is required.');
  }

  const imageBytes = await fs.readFile(file.path);

  const form = new FormData();
  form.append(
    'file',
    new Blob([imageBytes], {
      type: file.mimetype || 'application/octet-stream',
    }),
    path.basename(file.path)
  );

  const response = await fetch(`${OCR_SERVICE_URL}/ocr`, {
    method: 'POST',
    body: form,
  });

  let payload;

  try {
    payload = await response.json();
  } catch {
    throw new Error(
      `OCR service returned invalid JSON with status ${response.status}.`
    );
  }

  if (!response.ok) {
    throw new Error(
      payload.detail || `OCR service failed with status ${response.status}.`
    );
  }

  return payload;
}

module.exports = {
  extractRegions,
};
