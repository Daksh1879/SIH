'use strict';

const mongoose = require('mongoose');

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Name is required.'],
      trim: true,
      minlength: [2, 'Name must be at least 2 characters.'],
      maxlength: [100, 'Name must be at most 100 characters.'],
    },
    email: {
      type: String,
      required: [true, 'Email is required.'],
      unique: true,
      trim: true,
      lowercase: true,
      match: [/^[^\s@]+@[^\s@]+\.[^\s@]+$/, 'Please provide a valid email address.'],
    },
    // Named passwordHash to match the existing auth.service.js boundary —
    // hashing is done in auth.service before createUser is called.
    // Do NOT add a pre-save hash hook here; that would double-hash.
    passwordHash: {
      type: String,
      required: [true, 'Password hash is required.'],
      select: false, // excluded from ordinary queries by default
    },
  },
  {
    timestamps: { createdAt: 'createdAt', updatedAt: false },
  }
);

// Virtual `id` string to match the in-memory store's contract.
// auth.service calls signToken(user.id) and sanitizeUser spreads user,
// so `id` must be a plain string on the returned object.
userSchema.set('toObject', {
  virtuals: true,
  transform(doc, ret) {
    ret.id = ret._id.toString();
    delete ret._id;
    delete ret.__v;
    // passwordHash is already excluded by `select: false`;
    // remove it here too in case it was deliberately selected for login.
    delete ret.passwordHash;
    return ret;
  },
});

// findUserByEmail in userStore explicitly needs the hash for bcrypt.compare.
// It will use .select('+passwordHash') when required.
const User = mongoose.model('User', userSchema);

module.exports = User;
