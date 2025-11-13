const db = require('../config/database');
const bcrypt = require('bcryptjs');
const { generateToken, generateRefreshToken } = require('../middleware/auth');
const { v4: uuidv4 } = require('uuid');

exports.register = async (req, res, next) => {
  try {
    const { username, email, apple_id, google_id, device_id } = req.body;

    // Validation
    if (!username || username.length < 3 || username.length > 20) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'INVALID_USERNAME',
          message: 'Username must be 3-20 characters'
        }
      });
    }

    // Check if username exists
    const existingUser = await db.query(
      'SELECT id FROM users WHERE username = $1',
      [username]
    );

    if (existingUser.rows.length > 0) {
      return res.status(409).json({
        success: false,
        error: {
          code: 'USERNAME_TAKEN',
          message: 'Username already taken'
        }
      });
    }

    // Create user
    const userId = uuidv4();
    const playerId = uuidv4();

    await db.query('BEGIN');

    await db.query(
      `INSERT INTO users (id, username, email, apple_id, google_id)
       VALUES ($1, $2, $3, $4, $5)`,
      [userId, username, email, apple_id, google_id]
    );

    // Create player with starting resources
    await db.query(
      `INSERT INTO players (id, user_id, display_name, gold, wood, stone, food, water, gems)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
      [playerId, userId, username, 100, 50, 50, 30, 20, 50]
    );

    await db.query('COMMIT');

    const token = generateToken({ user_id: userId, player_id: playerId });
    const refresh_token = generateRefreshToken({ user_id: userId });

    res.status(201).json({
      success: true,
      data: {
        user_id: userId,
        player_id: playerId,
        username,
        token,
        refresh_token
      }
    });
  } catch (error) {
    await db.query('ROLLBACK');
    next(error);
  }
};

exports.login = async (req, res, next) => {
  try {
    const { apple_id, google_id, device_id } = req.body;

    let query, params;

    if (apple_id) {
      query = 'SELECT id, username FROM users WHERE apple_id = $1';
      params = [apple_id];
    } else if (google_id) {
      query = 'SELECT id, username FROM users WHERE google_id = $1';
      params = [google_id];
    } else {
      return res.status(400).json({
        success: false,
        error: {
          code: 'INVALID_REQUEST',
          message: 'apple_id or google_id required'
        }
      });
    }

    const result = await db.query(query, params);

    if (result.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: {
          code: 'USER_NOT_FOUND',
          message: 'User not found. Please register first.'
        }
      });
    }

    const user = result.rows[0];

    // Get player ID
    const playerResult = await db.query(
      'SELECT id FROM players WHERE user_id = $1',
      [user.id]
    );

    const player_id = playerResult.rows[0]?.id;

    // Update last login
    await db.query(
      'UPDATE users SET last_login = NOW() WHERE id = $1',
      [user.id]
    );

    const token = generateToken({ user_id: user.id, player_id });
    const refresh_token = generateRefreshToken({ user_id: user.id });

    res.json({
      success: true,
      data: {
        user_id: user.id,
        player_id,
        username: user.username,
        token,
        refresh_token
      }
    });
  } catch (error) {
    next(error);
  }
};

exports.refresh = async (req, res, next) => {
  try {
    const { refresh_token } = req.body;

    if (!refresh_token) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'INVALID_REQUEST',
          message: 'refresh_token required'
        }
      });
    }

    // Verify refresh token
    const jwt = require('jsonwebtoken');
    const decoded = jwt.verify(
      refresh_token,
      process.env.JWT_REFRESH_SECRET || process.env.JWT_SECRET
    );

    // Get player ID
    const result = await db.query(
      'SELECT id FROM players WHERE user_id = $1',
      [decoded.user_id]
    );

    const player_id = result.rows[0]?.id;

    const token = generateToken({ user_id: decoded.user_id, player_id });
    const new_refresh_token = generateRefreshToken({ user_id: decoded.user_id });

    res.json({
      success: true,
      data: {
        token,
        refresh_token: new_refresh_token
      }
    });
  } catch (error) {
    return res.status(403).json({
      success: false,
      error: {
        code: 'INVALID_REFRESH_TOKEN',
        message: 'Invalid or expired refresh token'
      }
    });
  }
};
