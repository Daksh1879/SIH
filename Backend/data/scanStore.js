// DB TEAM: replace these internals with Mongoose calls.
// Keep these exact function names and signatures.

const { randomUUID } = require('crypto');

const scans = [];

async function createScan(scan) {
  const record = { id: randomUUID(), ...scan, createdAt: new Date() };
  scans.push(record);
  return record;
}

async function findScanById(id) {
  return scans.find((s) => s.id === id) || null;
}

async function findScansByUserId(userId) {
  return scans
    .filter((s) => s.userId === userId)
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
}

module.exports = { createScan, findScanById, findScansByUserId };
