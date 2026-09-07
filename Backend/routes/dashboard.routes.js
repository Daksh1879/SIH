const { Router } = require('express');
const { history, scanById } = require('../controllers/dashboard.controller');
const { protect } = require('../middleware/auth.middleware');

const router = Router();

router.get('/history', protect, history);
router.get('/scan/:id', protect, scanById);

module.exports = router;
