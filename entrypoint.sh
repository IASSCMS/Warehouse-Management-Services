#!/bin/sh

echo "⚙️ Applying migrations..."
python manage.py migrate

echo "📦 PORT from .env is: $PORT"

PORT=${PORT:-8000}
echo "🚀 Starting Django server on port $PORT..."
python manage.py runserver 0.0.0.0:$PORT
