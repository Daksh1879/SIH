const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { jwtSecret } = require('../config/env');
const userStore = require('../data/userStore');
const AppError = require('../utils/AppError');

const SALT_ROUNDS = 10;

function signToken(userId) {
  return jwt.sign({ userId }, jwtSecret, { expiresIn: '7d' });
}

function sanitizeUser(user) {
  const { passwordHash, ...safe } = user;
  return safe;
}

async function registerUser({ name, email, password }) {
  const existing = await userStore.findUserByEmail(email);
  if (existing) throw new AppError('An account with this email already exists.', 409);

  const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
  const user = await userStore.createUser({ name, email, passwordHash });
  const token = signToken(user.id);
  return { token, user: sanitizeUser(user) };
}

async function loginUser({ email, password }) {
  const user = await userStore.findUserByEmail(email);
  const GENERIC_ERROR = new AppError('Invalid email or password.', 401);

  if (!user) throw GENERIC_ERROR;

  const match = await bcrypt.compare(password, user.passwordHash);
  if (!match) throw GENERIC_ERROR;

  const token = signToken(user.id);
  return { token, user: sanitizeUser(user) };
}

async function getMe(userId) {
  const user = await userStore.findUserById(userId);
  if (!user) throw new AppError('User not found.', 404);
  return sanitizeUser(user);
}

module.exports = { registerUser, loginUser, getMe };
