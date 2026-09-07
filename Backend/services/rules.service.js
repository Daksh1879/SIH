const RULES = {
  food: ['MRP', 'Net quantity', 'Consumer care contact'],
  cosmetics: [
    'Manufacturer name & address',
    'MRP',
    'Net quantity',
    'Country of origin',
    'Consumer care contact',
    'Manufacturing date',
  ],
  general: [
    'Manufacturer name & address',
    'MRP',
    'Net quantity',
    'Country of origin',
    'Consumer care contact',
    'Manufacturing date',
    'Generic name',
  ],
};

const VALID_CATEGORIES = Object.keys(RULES);

function getRequiredFields(category) {
  return RULES[category] || [];
}

function compareFields(category, extractedFields) {
  const required = getRequiredFields(category);
  const found = Object.keys(extractedFields).filter(
    (key) => extractedFields[key] && required.includes(key)
  );
  const missing = required.filter((field) => !found.includes(field));
  const status = missing.length === 0 ? 'pass' : 'fail';
  return { foundFields: found, missingFields: missing, status };
}

module.exports = { getRequiredFields, compareFields, VALID_CATEGORIES };
