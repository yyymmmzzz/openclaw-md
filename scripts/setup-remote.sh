#!/bin/bash
# Setup script for GitHub/GitLab remote repository
# Usage: ./scripts/setup-remote.sh <github|gitlab> <repo-url> <token>

set -e

PLATFORM=${1:-}
REPO_URL=${2:-}
TOKEN=${3:-}

if [ -z "$PLATFORM" ] || [ -z "$REPO_URL" ]; then
    echo "Usage: $0 <github|gitlab> <repo-url> [token]"
    echo ""
    echo "Examples:"
    echo "  $0 github https://github.com/username/openclaw-backup.git ghp_xxxxxx"
    echo "  $0 gitlab https://gitlab.com/username/openclaw-backup.git glpat-xxxxxx"
    echo ""
    echo "To create a GitHub token:"
    echo "  1. Go to https://github.com/settings/tokens"
    echo "  2. Click 'Generate new token (classic)'"
    echo "  3. Select 'repo' scope"
    echo "  4. Copy the token and use it here"
    echo ""
    echo "To create a GitLab token:"
    echo "  1. Go to https://gitlab.com/-/profile/personal_access_tokens"
    echo "  2. Click 'Add new token'"
    echo "  3. Select 'api' and 'write_repository' scopes"
    echo "  4. Copy the token and use it here"
    exit 1
fi

# Parse repository URL and add token if provided
if [ -n "$TOKEN" ]; then
    if [[ "$REPO_URL" == https://github.com/* ]]; then
        REPO_URL_WITH_TOKEN="https://${TOKEN}@github.com/${REPO_URL#https://github.com/}"
    elif [[ "$REPO_URL" == https://gitlab.com/* ]]; then
        REPO_URL_WITH_TOKEN="https://oauth2:${TOKEN}@${REPO_URL#https://}"
    else
        echo "Warning: Unknown platform, using URL as-is"
        REPO_URL_WITH_TOKEN="$REPO_URL"
    fi
else
    REPO_URL_WITH_TOKEN="$REPO_URL"
fi

cd /workspace/projects/workspace

# Add remote
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL_WITH_TOKEN"

# Save remote URL to environment file for backup script
mkdir -p /workspace/projects/workspace/.env
echo "export REMOTE_URL=\"$REPO_URL_WITH_TOKEN\"" > /workspace/projects/workspace/.env/backup.env
echo "export BRANCH=\"main\"" >> /workspace/projects/workspace/.env/backup.env

echo "✅ Remote repository configured successfully!"
echo ""
echo "Repository: $REPO_URL"
echo ""
echo "To test the backup, run:"
echo "  source .env/backup.env && ./scripts/backup.sh"
