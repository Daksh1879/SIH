const ocrService = require('./ocr.service');
const rulesService = require('./rules.service');
const scanStore = require('../data/scanStore');
const AppError = require('../utils/AppError');

async function runVerification({ file, category, userId }) {
  if (!rulesService.VALID_CATEGORIES.includes(category)) {
    throw new AppError(`Invalid category. Must be one of: ${rulesService.VALID_CATEGORIES.join(', ')}`, 400);
  }

  const { extractedText, fields } = await ocrService.extractFields(file, category);
  const { foundFields, missingFields, status } = rulesService.compareFields(category, fields);

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
