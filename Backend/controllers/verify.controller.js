const verificationService = require('../services/verification.service');
const { success } = require('../utils/apiResponse');
const AppError = require('../utils/AppError');

async function uploadAndVerify(req, res, next) {
  try {
    if (!req.file) throw new AppError('No image file provided. Use field name "image".', 400);

    const { category } = req.body;
    if (!category) throw new AppError('category is required (food, cosmetics, or general).', 400);

    const result = await verificationService.runVerification({
      file: req.file,
      category: category.toLowerCase().trim(),
      userId: req.user.id,
    });

    res.status(200).json(success(result));
  } catch (err) {
    next(err);
  }
}

module.exports = { uploadAndVerify };
