'use strict';

// Database-backed compliance rules service.
// Rules are now fetched from MongoDB (ComplianceRule collection)
// so categories and required fields can be updated without code changes.
//
// Field keys in the DB are machine-readable (e.g. 'mrp').
// Field labels in the DB are display strings (e.g. 'MRP').
// The OCR service returns a `fields` object keyed by label strings
// (e.g. { 'MRP': 'Rs. 149', 'Net quantity': '250g' }).
// compareFields matches on label, matching the original rules.service contract.

const ComplianceRule = require('../models/ComplianceRule');
const AppError = require('../utils/AppError');

/**
 * Returns an array of label strings for a given category, e.g.
 * ['MRP', 'Net quantity', 'Consumer care contact']
 * Throws a controlled 400 if the category is not found in the DB.
 */
async function getRequiredFields(category) {
  const rule = await ComplianceRule.findOne({ category: category.toLowerCase() }).lean();
  if (!rule) {
    throw new AppError(
      `Compliance rules not found for category "${category}". Please run the seed script.`,
      400
    );
  }
  return rule.requiredFields.map((f) => f.label);
}

/**
 * Returns sorted list of valid category names from the DB.
 * Used by verification.service to validate user-supplied category.
 */
async function getValidCategories() {
  const rules = await ComplianceRule.find({}, 'category').lean();
  return rules.map((r) => r.category);
}

/**
 * Compare extracted fields against category rules.
 * `extractedFields` is an object: { labelString: value|null, ... }
 * Returns { foundFields, missingFields, status } — lowercase status preserved.
 */
async function compareFields(category, extractedFields) {
  const required = await getRequiredFields(category);
  const found = Object.keys(extractedFields).filter(
    (key) => extractedFields[key] && required.includes(key)
  );
  const missing = required.filter((field) => !found.includes(field));
  const status = missing.length === 0 ? 'pass' : 'fail';
  return { foundFields: found, missingFields: missing, status };
}

module.exports = { getRequiredFields, compareFields, getValidCategories };
