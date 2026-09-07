const authService = require('../services/auth.service');
const { success } = require('../utils/apiResponse');
const AppError = require('../utils/AppError');

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MIN_PASSWORD_LENGTH = 6;

async function register(req, res, next) {
  try {
    const { name, email, password } = req.body;
    if (!name || !email || !password) throw new AppError('name, email, and password are required.', 400);
    if (!EMAIL_RE.test(email)) throw new AppError('Please provide a valid email address.', 400);
    if (password.length < MIN_PASSWORD_LENGTH) throw new AppError(`Password must be at least ${MIN_PASSWORD_LENGTH} characters.`, 400);

    const result = await authService.registerUser({ name, email, password });
    res.status(201).json(success(result));
  } catch (err) {
    next(err);
  }
}

async function login(req, res, next) {
  try {
    const { email, password } = req.body;
    if (!email || !password) throw new AppError('email and password are required.', 400);

    const result = await authService.loginUser({ email, password });
    res.status(200).json(success(result));
  } catch (err) {
    next(err);
  }
}

async function me(req, res, next) {
  try {
    const user = await authService.getMe(req.user.id);
    res.status(200).json(success({ user }));
  } catch (err) {
    next(err);
  }
}

module.exports = { register, login, me };
