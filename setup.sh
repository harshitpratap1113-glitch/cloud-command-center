#!/usr/bin/env bash
# Setup script executed automatically when GitHub Codespace boots up

echo "⚡ Initializing Cloud Command Center..."

# 1. Install python dependencies
pip install --upgrade pip requests uvicorn fastapi pytest huggingface_hub

# 2. Configure Git Identity
git config --global user.name "Harshit Pratap"
git config --global user.email "harshitpratap1113@gmail.com"

# 3. Create workspace folders
mkdir -p projects deliveries

echo "✅ Environment configured!"
echo "🚀 To launch the 24/7 background prompt synthesizer, run:"
echo "   python cloud_architect_daemon.py"
