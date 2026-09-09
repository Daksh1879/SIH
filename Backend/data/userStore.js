'use strict';

// Mongoose-backed replacement for the in-memory userStore.
// Preserves the exact function names, signatures, and return shapes
// that auth.service.js depends on.

const User = require('../models/User');

/**
 * Find a user by email.
 * Returns the full document including passwordHash (needed by loginUser
 * in auth.service.js for bcrypt.compare).
 * The .select('+passwordHash') explicitly opts-in to the field that is
 * excluded by default in the schema.
 */
async function findUserByEmail(email) {
  const user = await User.findOne({ email: email.toLowerCase().trim() })
    .select('+passwordHash')
    .lean({ virtuals: true });
  return user || null;
}

/**
 * Find a user by their string id (JWT payload `userId`).
 * Does NOT include passwordHash — used only for /me and token validation.
 */
async function findUserById(id) {
  if (!id || id.length !== 24) return null; // quick guard for invalid ObjectId strings
  const user = await User.findById(id).lean({ virtuals: true });
  return user || null;
}

/**
 * Create a new user.
 * `passwordHash` has already been produced by bcrypt in auth.service.js —
 * do NOT hash again here.
 * Returns the plain object with `id` string matching the in-memory shape.
 */
async function createUser({ name, email, passwordHash }) {
  const user = await User.create({ name, email, passwordHash });
  // .toObject() applies the schema transform: adds `id`, removes `_id`/`__v`/`passwordHash`
  return user.toObject();
}

module.exports = { findUserByEmail, findUserById, createUser };
