// server/index.js
// Main entry point for the Express API server

// Load environment variables from a .env file if present
require('dotenv').config();

const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const tasksRouter = require('./routes/tasks.js');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Mount the tasks router under /api/tasks
app.use('/api/tasks', tasksRouter);

// Connect to MongoDB
const mongoUri = process.env.MONGODB_URI;
if (!mongoUri) {
  console.error('❌ MONGODB_URI environment variable not set.');
  process.exit(1);
}

mongoose
  .connect(mongoUri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => {
    console.log('✅ Connected to MongoDB');
    // Start the server after a successful DB connection
    const port = process.env.PORT || 5000;
    app.listen(port, () => {
      console.log(`🚀 Server is running at http://localhost:${port}`);
    });
  })
  .catch((err) => {
    console.error('❌ Failed to connect to MongoDB:', err);
    process.exit(1);
  });
