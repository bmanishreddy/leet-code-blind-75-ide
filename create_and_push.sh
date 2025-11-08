#!/bin/bash
# Script to create GitHub repository and push code

REPO_NAME="leet-code-blind-75-ide"
REPO_OWNER="bmanishreddy"
REPO_DESC="LeetCode Blind 75 IDE with AI-powered hints, code execution, test runner, and progress tracking"

echo "🚀 Creating GitHub repository: $REPO_OWNER/$REPO_NAME"
echo ""

# Check if GitHub CLI is authenticated
if ! gh auth status &>/dev/null; then
    echo "❌ GitHub CLI not authenticated. Please run: gh auth login"
    exit 1
fi

# Get current authenticated user
CURRENT_USER=$(gh api user --jq .login)
echo "📋 Currently authenticated as: $CURRENT_USER"

if [ "$CURRENT_USER" != "$REPO_OWNER" ]; then
    echo ""
    echo "⚠️  Warning: You're authenticated as '$CURRENT_USER' but want to create repo for '$REPO_OWNER'"
    echo ""
    echo "Please choose one of the following options:"
    echo "1. Switch GitHub CLI authentication:"
    echo "   gh auth login"
    echo "   (Then select $REPO_OWNER account)"
    echo ""
    echo "2. Create repository manually:"
    echo "   - Go to: https://github.com/new"
    echo "   - Repository name: $REPO_NAME"
    echo "   - Make it public"
    echo "   - Don't initialize with README"
    echo "   - Then run: git push -u origin main"
    echo ""
    exit 1
fi

# Create repository
echo "📦 Creating repository..."
gh repo create "$REPO_NAME" \
    --public \
    --description "$REPO_DESC" \
    --source=. \
    --remote=origin \
    --push

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully created and pushed to: https://github.com/$REPO_OWNER/$REPO_NAME"
else
    echo ""
    echo "❌ Failed to create repository. Please check your permissions."
fi

