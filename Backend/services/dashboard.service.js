const scanStore = require('../data/scanStore');
const AppError = require('../utils/AppError');

async function getHistory(userId) {
  const scans = await scanStore.findScansByUserId(userId);
  return scans;
}

async function getScanById(scanId, userId) {
  const scan = await scanStore.findScanById(scanId);
  // Treat not-found and wrong-owner identically to avoid confirming another user's scan
  if (!scan || scan.userId !== userId) throw new AppError('Scan not found.', 404);
  return scan;
}

module.exports = { getHistory, getScanById };
