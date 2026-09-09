'use strict';

const mongoose = require('mongoose');

const requiredFieldSchema = new mongoose.Schema(
  {
    key: {
      type: String,
      required: [true, 'Field key is required.'],
      trim: true,
    },
    label: {
      type: String,
      required: [true, 'Field label is required.'],
      trim: true,
    },
    description: {
      type: String,
      default: '',
      trim: true,
    },
    required: {
      type: Boolean,
      default: true,
    },
  },
  { _id: false }
);

const complianceRuleSchema = new mongoose.Schema(
  {
    // category stored lowercase so lookup is case-insensitive by convention
    category: {
      type: String,
      required: [true, 'category is required.'],
      unique: true,
      trim: true,
      lowercase: true,
    },
    requiredFields: {
      type: [requiredFieldSchema],
      default: [],
    },
  },
  { timestamps: true }
);

const ComplianceRule = mongoose.model('ComplianceRule', complianceRuleSchema);

module.exports = ComplianceRule;
