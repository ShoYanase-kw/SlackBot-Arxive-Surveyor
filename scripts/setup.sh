#!/bin/sh

echo "Write scripts for building docker image..."

# docker-compose.yml作成
echo -e "services:\n  bot:\n    container_name: $1\n    build: \n      context: .\n      dockerfile: etc/docker/Dockerfile\n    volumes:\n      - .:/app\n    tty: true\n    env_file: etc/.env" > docker-compose.yml
# scripts/build.sh作成
echo -e "docker builder prune -y\ndocker compose up --build" > scripts/build.sh
# scripts/up.sh作成
echo -e "docker compose down --remove-orphans\ndocker compose up" > scripts/up.sh

bash scripts/build.sh