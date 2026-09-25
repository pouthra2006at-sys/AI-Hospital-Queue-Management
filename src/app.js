const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const authRoutes = require('./routes/authRoutes');
const blogRoutes = require('./routes/blogRoutes');
const aiRoutes = require('./routes/aiRoutes');
const errorMiddleware = require('./middleware/errorMiddleware');

const app = express();

app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

app.use('/api/auth', authRoutes);
app.use('/api/blogs', blogRoutes);
app.use('/api/ai', aiRoutes);

app.use(errorMiddleware);

app.get('/', (req, res) => {
  res.json({ message: 'AI BlogNest API is running' });
});

module.exports = app;
