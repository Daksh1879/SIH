const dashboardService = require('../services/dashboard.service');
const { success } = require('../utils/apiResponse');

async function history(req, res, next) {
  try {
    const scans = await dashboardService.getHistory(req.user.id);
    res.status(200).json(success({ scans }));
  } catch (err) {
    next(err);
  }
}

async function scanById(req, res, next) {
  try {
    const scan = await dashboardService.getScanById(req.params.id, req.user.id);
    res.status(200).json(success({ scan }));
  } catch (err) {
    next(err);
  }
}

module.exports = { history, scanById };
