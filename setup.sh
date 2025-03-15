#!/bin/bash

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd ../frontend
npm install

echo "Setup complete!"
echo "To start the backend server: cd backend && python manage.py runserver"
echo "To start the frontend server: cd frontend && npm run dev" 