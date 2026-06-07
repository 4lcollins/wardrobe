#!/bin/bash
 
# deploy.sh — copies all non-gitignored, non-hidden files to iCloud Drive
 
ICLOUD_PATH="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Wardrobe"
 
# Create destination if it doesn't exist
mkdir -p "$ICLOUD_PATH"
 
rsync -av \
  --include='.env' \
  --exclude='.*' \
  --filter=':- .gitignore' \
  --delete \
  ./ "$ICLOUD_PATH/"
 
echo "✓ Deployed to $ICLOUD_PATH"
 