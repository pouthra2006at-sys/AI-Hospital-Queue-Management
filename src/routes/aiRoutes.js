const express = require('express');
const { body } = require('express-validator');
const { generateBlog, summarizeBlog } = require('../controllers/aiController');
const authMiddleware = require('../middleware/authMiddleware');

const router = express.Router();

router.post(
  '/generate-blog',
  authMiddleware,
  [
    body('topic').notEmpty().withMessage('Topic is required'),
    body('category').optional().notEmpty().withMessage('Category cannot be empty'),
  ],
  generateBlog
);

router.post(
  '/summarize',
  [body('content').notEmpty().withMessage('Content is required')],
  summarizeBlog
);

module.exports = router;
