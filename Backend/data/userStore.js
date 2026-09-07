// DB TEAM: replace these internals with Mongoose calls.
// Keep these exact function names and signatures.
// Each function is async to match the future DB interface.

const { randomUUID } = require('crypto');

const users = [];

async function findUserByEmail(email) {
  return users.find((u) => u.email === email) || null;
}

async function findUserById(id) {
  return users.find((u) => u.id === id) || null;
}

async function createUser({ name, email, passwordHash }) {
  const user = { id: randomUUID(), name, email, passwordHash, createdAt: new Date() };
  users.push(user);
  return user;
}

module.exports = { findUserByEmail, findUserById, createUser };
