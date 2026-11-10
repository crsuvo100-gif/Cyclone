"""Phase 4: Deployment Scripts module.

Provides deployment scripts for various environments.
"""

import os


def generate_production_deploy_script() -> str:
    """Generate a production deployment script."""
    return """#!/usr/bin/env bash
# Production Deployment Script for MOON/CYCLONE
# Usage: ./deploy-prod.sh <version>
set -euo pipefail

VERSION="${1:-$(date +%Y%m%d%H%M%S)}"
IMAGE="moon-cyclone:${VERSION}"

echo "Starting production deployment v${VERSION}..."

# Build
echo "Building Docker image..."
docker build -t "${IMAGE}" .

# Push
echo "Pushing image..."
docker push "${IMAGE}"

# Deploy
echo "Deploying to production..."
kubectl set image deployment/moon-cyclone moon-cyclone="${IMAGE}"
kubectl rollout status deployment/moon-cyclone

echo "Production deployment v${VERSION} completed successfully!"
"""


def generate_staging_deploy_script() -> str:
    """Generate a staging deployment script."""
    return """#!/usr/bin/env bash
# Staging Deployment Script for MOON/CYCLONE
# Usage: ./deploy-staging.sh
set -euo pipefail

echo "Starting staging deployment..."

# Run tests
echo "Running tests..."
pytest tests/ -v --tb=short

# Build
echo "Building staging image..."
docker build -t "moon-cyclone:staging" .

# Deploy
echo "Deploying to staging..."
docker-compose up -d --build

echo "Staging deployment completed!"
"""


def generate_dev_deploy_script() -> str:
    """Generate a dev deployment script."""
    return """#!/usr/bin/env bash
# Development Deployment Script for MOON/CYCLONE
# Usage: ./deploy-dev.sh
set -euo pipefail

echo "Starting development deployment..."

# Install dependencies
echo "Installing dependencies..."
npm install
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start server
echo "Starting server on port 8765..."
npm run dev

echo "Development deployment completed!"
"""


if __name__ == "__main__":
    scripts_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "scripts"
    )
    os.makedirs(scripts_dir, exist_ok=True)

    with open(os.path.join(scripts_dir, "deploy-prod.sh"), "w") as f:
        f.write(generate_production_deploy_script())
    with open(os.path.join(scripts_dir, "deploy-staging.sh"), "w") as f:
        f.write(generate_staging_deploy_script())
    with open(os.path.join(scripts_dir, "deploy-dev.sh"), "w") as f:
        f.write(generate_dev_deploy_script())

    print("Created deployment scripts in", scripts_dir)
