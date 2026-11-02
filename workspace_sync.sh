#!/usr/bin/env bash
# Clone all SaaS platforms into projects/ folder inside GitHub Codespaces

mkdir -p projects
cd projects

echo "[*] Syncing all SaaS projects..."

repos=(
  "https://github.com/harshitpratap1113-glitch/voxai-platform.git"
  "https://github.com/harshitpratap1113-glitch/tokenshield.git"
  "https://github.com/harshitpratap1113-glitch/bizflow-platform.git"
  "https://github.com/harshitpratap1113-glitch/freelancing-portfolio.git"
)

for r in "${repos[@]}"; do
  repo_name=$(basename -s .git "$r")
  if [ ! -d "$repo_name" ]; then
    echo "Cloning $repo_name..."
    git clone "$r"
  else
    echo "Updating $repo_name..."
    git -C "$repo_name" pull
  fi
done

echo "✅ All SaaS projects synced into /projects!"
