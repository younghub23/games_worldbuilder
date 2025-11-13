const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');
const playerController = require('../controllers/playerController');

// All routes require authentication
router.use(authenticateToken);

/**
 * @route   GET /api/v1/player/profile
 * @desc    Get player profile
 * @access  Private
 */
router.get('/profile', playerController.getProfile);

/**
 * @route   PUT /api/v1/player/profile
 * @desc    Update player profile
 * @access  Private
 */
router.put('/profile', playerController.updateProfile);

/**
 * @route   GET /api/v1/player/resources
 * @desc    Get player resources
 * @access  Private
 */
router.get('/resources', playerController.getResources);

module.exports = router;
