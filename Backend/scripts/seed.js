'use strict';

/**
 * Seed script — compliance rules for Food, Cosmetics, and General categories.
 *
 * Idempotent: uses updateOne with upsert so running it multiple times
 * does not create duplicates or overwrite other categories.
 *
 * Usage:
 *   npm run seed
 */

require('dotenv').config();

const mongoose = require('mongoose');
const ComplianceRule = require('../models/ComplianceRule');

const RULES = [
  {
    category: 'food',
    requiredFields: [
      { key: 'mrp', label: 'MRP', description: 'Maximum Retail Price', required: true },
      { key: 'net_quantity', label: 'Net quantity', description: 'Net weight or volume of the product', required: true },
      { key: 'consumer_care_contact', label: 'Consumer care contact', description: 'Consumer helpline number or email', required: true },
    ],
  },
  {
    category: 'cosmetics',
    requiredFields: [
      { key: 'manufacturer_name', label: 'Manufacturer name & address', description: 'Full name and address of the manufacturer', required: true },
      { key: 'mrp', label: 'MRP', description: 'Maximum Retail Price', required: true },
      { key: 'net_quantity', label: 'Net quantity', description: 'Net weight or volume of the product', required: true },
      { key: 'country_of_origin', label: 'Country of origin', description: 'Country where the product was manufactured', required: true },
      { key: 'consumer_care_contact', label: 'Consumer care contact', description: 'Consumer helpline number or email', required: true },
      { key: 'manufacturing_date', label: 'Manufacturing date', description: 'Date of manufacture or expiry', required: true },
    ],
  },
  {
    category: 'general',
    requiredFields: [
      { key: 'manufacturer_name', label: 'Manufacturer name & address', description: 'Full name and address of the manufacturer', required: true },
      { key: 'mrp', label: 'MRP', description: 'Maximum Retail Price', required: true },
      { key: 'net_quantity', label: 'Net quantity', description: 'Net weight or volume of the product', required: true },
      { key: 'country_of_origin', label: 'Country of origin', description: 'Country where the product was manufactured', required: true },
      { key: 'consumer_care_contact', label: 'Consumer care contact', description: 'Consumer helpline number or email', required: true },
      { key: 'manufacturing_date', label: 'Manufacturing date', description: 'Date of manufacture or expiry', required: true },
      { key: 'generic_name', label: 'Generic name', description: 'Common/generic name of the product', required: true },
    ],
  },
];

async function seed() {
  const uri = process.env.MONGO_URI;
  if (!uri) {
    console.error('[seed] FATAL: MONGO_URI is not set. Create a .env file first.');
    process.exit(1);
  }

  try {
    await mongoose.connect(uri);
    console.log('[seed] Connected to MongoDB.');

    for (const rule of RULES) {
      const result = await ComplianceRule.updateOne(
        { category: rule.category },
        { $set: { requiredFields: rule.requiredFields } },
        { upsert: true }
      );
      const action = result.upsertedCount > 0 ? 'inserted' : 'updated';
      console.log(`[seed] ${action}: ${rule.category} (${rule.requiredFields.length} fields)`);
    }

    console.log('[seed] Done. Compliance rules are up to date.');
  } catch (err) {
    console.error('[seed] Error:', err.message);
    process.exit(1);
  } finally {
    await mongoose.disconnect();
    console.log('[seed] Disconnected.');
  }
}

seed();
