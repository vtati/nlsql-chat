#!/bin/bash
# Vercel build script for frontend
echo "Building React app..."
npm ci
npm run build
echo "Build completed!"