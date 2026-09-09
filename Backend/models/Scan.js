'use strict';

const mongoose = require('mongoose');

const scanSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: [true, 'userId is required.'],
      index: true,
    },
    category: {
      type: String,
      required: [true, 'category is required.'],
      trim: true,
    },
    // imagePath matches the field name used by verification.service.js
    // (file.path from Multer) and returned in scan responses.
    imagePath: {
      type: String,
      required: [true, 'imagePath is required.'],
    },
    extractedText: {
      type: String,
      default: '',
    },
    // status is lowercase 'pass' / 'fail' — confirmed in dashboard.html and results.html
    status: {
      type: String,
      enum: ['pass', 'fail'],
      required: [true, 'status is required.'],
    },
    foundFields: {
      type: [String],
      default: [],
    },
    missingFields: {
      type: [String],
      default: [],
    },
  },
  {
    timestamps: { createdAt: 'createdAt', updatedAt: false },
  }
);

// Compound index: efficient for getHistory (userId + sort by newest first)
scanSchema.index({ userId: 1, createdAt: -1 });

scanSchema.set('toObject', {
  virtuals: true,
  transform(doc, ret) {
    ret.id = ret._id.toString();
    // Keep userId as string so dashboard.service string comparison works
    if (ret.userId) ret.userId = ret.userId.toString();
    delete ret._id;
    delete ret.__v;
    return ret;
  },
});

const Scan = mongoose.model('Scan', scanSchema);

module.exports = Scan;
