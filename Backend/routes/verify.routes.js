const { Router } = require('express');
const { uploadAndVerify } = require('../controllers/verify.controller');
const { protect } = require('../middleware/auth.middleware');
const { upload } = require('../middleware/upload.middleware');

const router = Router();

router.post('/upload', protect, upload.single('image'), uploadAndVerify);

module.exports = router;
