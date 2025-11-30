#!/usr/bin/env bash
# Wrapper to activate the gesture venv and run the script (zsh/bash)
set -e
cd "$(dirname "$0")"
if [ -f "hand_gesture_env/bin/activate" ]; then
  # shellcheck disable=SC1091
  source hand_gesture_env/bin/activate
  python index.py
else
  echo "Virtualenv not found at ./hand_gesture_env"
  echo "Create it with: python3 -m venv hand_gesture_env"
  echo "Then install deps: source hand_gesture_env/bin/activate && pip install -r requirements.txt"
  exit 1
fi
