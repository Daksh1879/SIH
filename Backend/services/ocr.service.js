// OCR TEAM: replace only this function's implementation.
// Input:  file object from Multer ({ path, mimetype, ... }), category string
// Output: { extractedText: string, fields: object }
// The fields object keys must match the rule names in rules.service.js exactly.
// Example output when OCR is implemented:
// {
//   extractedText: "MRP Rs. 149 Net Wt 250g ...",
//   fields: { "MRP": "Rs. 149", "Net quantity": "250g", ... }
// }

async function extractFields(file, category) {
  // Placeholder: OCR not implemented yet.
  // Returns empty fields so rules.service correctly marks all as missing.
  return {
    extractedText: '',
    fields: {},
  };
}

module.exports = { extractFields };
