#!/bin/bash

set -euo pipefail

# Source the vars.sh script
source vars.sh


# Function to increment version
increment_version() {
    local version=$1
    local part=$2
    IFS='.' read -ra ver <<< "$version"
    case $part in
        major) ((ver[0]++)); ver[1]=0; ver[2]=0 ;;
        minor) ((ver[1]++)); ver[2]=0 ;;
        patch) ((ver[2]++)) ;;
    esac
    echo "${ver[0]}.${ver[1]}.${ver[2]}"
}

# Get current version from pyproject.toml
current_version=$(grep "^version" pyproject.toml | sed -E 's/version = "(.*)"/\1/')

# Prompt for version increment type
echo "Current version: $current_version"
echo "Select version increment type:"
echo "1) Major"
echo "2) Minor"
echo "3) Patch"
echo "4) No increment"
read -p "Enter your choice (1-4): " choice

case $choice in
    1) new_version=$(increment_version "$current_version" major) ;;
    2) new_version=$(increment_version "$current_version" minor) ;;
    3) new_version=$(increment_version "$current_version" patch) ;;
    4) new_version=$current_version ;;
    *) echo "Invalid choice. Exiting."; exit 1 ;;
esac

if [ "$new_version" != "$current_version" ]; then
    # Update version in pyproject.toml
    sed -i.bak "s/^version = .*/version = \"$new_version\"/" pyproject.toml && rm pyproject.toml.bak
    
    # Update version in __init__.py
    sed -i.bak "s/__version__ = .*/__version__ = \"$new_version\"/" src/duohub/__init__.py && rm src/duohub/__init__.py.bak
    
    # Commit version changes
    git add pyproject.toml src/duohub/__init__.py
    git commit -m "chore: bump version to $new_version"
fi

# Ensure we're on the main branch and up-to-date
git checkout main
git pull origin main

poetry build

# Create and push Git tag
git tag "v$new_version"
git push origin "v$new_version"

# Push changes to GitHub
git push origin main

# Publish to PyPI using the token format
poetry config pypi-token.pypi $PYPI_TOKEN
poetry publish --username __token__ --password $PYPI_TOKEN

echo "Release $new_version completed successfully!"

# Prompt for release title and description
read -p "Enter the release title: " release_title
echo "Enter the release description (press Ctrl+D when finished):"
release_description=$(cat)

# Create a GitHub release with the provided title and description
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/duohub-ai/duohub-py/releases \
  -d "{
    \"tag_name\": \"v$new_version\",
    \"target_commitish\": \"main\",
    \"name\": \"$release_title\",
    \"body\": \"$release_description\",
    \"draft\": false,
    \"prerelease\": false
  }"

echo "GitHub release created for v$new_version with title: $release_title"
