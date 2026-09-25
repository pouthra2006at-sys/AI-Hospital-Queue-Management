const express = require('express');
const { body } = require('express-validator');
const {
  createBlog,
  getAllBlogs,
  getBlogById,
  updateBlog,
  deleteBlog,
} = require('../controllers/blogController');
const authMiddleware = require('../middleware/authMiddleware');

const router = express.Router();

router.post(
  '/',
  authMiddleware,
  [
    body('title').notEmpty().withMessage('Title is required'),
    body('content').notEmpty().withMessage('Content is required'),
    body('category').notEmpty().withMessage('Category is required'),
  ],
  createBlog
);

router.get('/', getAllBlogs);
router.get('/:id', getBlogById);

router.put(
  '/:id',
  authMiddleware,
  [
    body('title').optional().notEmpty().withMessage('Title cannot be empty'),
    body('content').optional().notEmpty().withMessage('Content cannot be empty'),
    body('category').optional().notEmpty().withMessage('Category cannot be empty'),
  ],
  updateBlog
);

router.delete('/:id', authMiddleware, deleteBlog);

module.exports = router;
