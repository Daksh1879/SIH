'use strict';

const ocrService = require('./ocr.service');
const rulesService = require('./rules.service');
const scanStore = require('../data/scanStore');
const AppError = require('../utils/AppError');

async function runVerification({ file, category, userId }) {
  // Validate category against DB rules (replaces VALID_CATEGORIES array)
  const validCategories = await rulesService.getValidCategories();
  if (!validCategories.includes(category)) {
    throw new AppError(
      `Invalid category "${category}". Must be one of: ${validCategories.join(', ')}`,
      400
    );
  }

  const { extractedText, fields } = await ocrService.extractFields(file, category);
  // compareFields is now async (fetches rules from DB)
  const { foundFields, missingFields, status } = await rulesService.compareFields(category, fields);

  const scan = await scanStore.createScan({
    userId,
    category,
    imagePath: file.path,
    extractedText,
    foundFields,
    missingFields,
    status,
  });

  return {
    scanId: scan.id,
    category: scan.category,
    status: scan.status,
    foundFields: scan.foundFields,
    missingFields: scan.missingFields,
    extractedText: scan.extractedText,
    createdAt: scan.createdAt,
  };
}

module.exports = { runVerification };
