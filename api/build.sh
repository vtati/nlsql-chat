#!/bin/bash

# Render build script for Natural Language to SQL API

echo "🚀 Starting Render build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r config/requirements.txt

# Create data directory for SQLite
echo "📁 Creating data directory..."
mkdir -p data

# Set up database
echo "🗄️ Setting up database..."
python scripts/setup_database.py

# Verify installation
echo "✅ Verifying installation..."
python -c "from src.main import app; print('✅ FastAPI app loads successfully')"

echo "🎉 Build completed successfully!"