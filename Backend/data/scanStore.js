'use strict';

// Mongoose-backed replacement for the in-memory scanStore.
// Preserves the exact function names and signatures that
// verification.service.js and dashboard.service.js depend on.

const Scan = require('../models/Scan');

/**
 * Create a scan record.
 * Input matches what verification.service.js passes:
 *   { userId, category, imagePath, extractedText, foundFields, missingFields, status }
 */
async function createScan(scan) {
  const record = await Scan.create(scan);
  return record.toObject();
}

/**
 * Find one scan by its string id.
 * Returns the plain object or null.
 * Ownership check is performed by dashboard.service.js (scan.userId !== userId).
 */
async function findScanById(id) {
  if (!id || id.length !== 24) return null;
  const scan = await Scan.findById(id).lean({ virtuals: true });
  return scan || null;
}

/**
 * Find all scans for a user, newest first.
 */
async function findScansByUserId(userId) {
  const scans = await Scan.find({ userId })
    .sort({ createdAt: -1 })
    .lean({ virtuals: true });
  return scans;
}

module.exports = { createScan, findScanById, findScansByUserId };
