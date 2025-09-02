#!/bin/bash

echo "🚀 Avvio Meta-Prompt Generator Web App..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❗ Docker non è installato. Per favore installa Docker prima:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check for docker-compose or docker compose (newer versions use 'docker compose')
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❗ Docker Compose non trovato. Per favore installa Docker Compose:"
    echo "   - Ubuntu/Debian: sudo apt-get install docker-compose-plugin"
    echo "   - macOS: brew install docker-compose"
    echo "   - Oppure installa Docker Desktop che include Compose"
    exit 1
fi

echo "✅ Docker trovato. Avvio dell'applicazione..."

# Build and start the container
$COMPOSE_CMD up --build

echo ""
echo "🎉 La web app è stata fermata!"