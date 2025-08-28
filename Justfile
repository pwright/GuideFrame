# Cross-distro automation for GuideFrame
# Usage: install https://github.com/casey/just ; run `just --list`

set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

# Detect package manager
pm := `command -v dnf >/dev/null && echo dnf || (command -v apt-get >/dev/null && echo apt-get || (command -v pacman >/dev/null && echo pacman || echo unknown))`

# Default Python
py := `command -v python3 || command -v python`

# Virtualenv dir
venv := ".venv"

# Print environment for debugging
env-info:
    @echo "pm={{pm}}"
    @echo "py={{py}}"
    @echo "venv={{venv}}"

# System dependencies (Fedora/Ubuntu/Arch)
setup:
    if [ "{{pm}}" = "dnf" ]; then \
      sudo dnf install -y ffmpeg xorg-x11-server-Xvfb chromium chromedriver python3; \
    elif [ "{{pm}}" = "apt-get" ]; then \
      sudo apt-get update; \
      sudo apt-get install -y ffmpeg xvfb chromium-driver chromium-browser python3-venv; \
    elif [ "{{pm}}" = "pacman" ]; then \
      sudo pacman -Syu --noconfirm ffmpeg xorg-server-xvfb chromium chromedriver python-virtualenv; \
    else \
      echo "Unsupported package manager. Install ffmpeg, Xvfb, Chromium, and chromedriver manually." >&2; \
    fi

# Create venv and install python deps
install-deps:
    {{py}} -m venv {{venv}}
    . {{venv}}/bin/activate && python -m pip install -U pip
    . {{venv}}/bin/activate && python -m pip install -r requirements.txt

# Start Xvfb for headless capture (Fedora/Wayland-safe)
start-xvfb:
    pgrep -x Xvfb >/dev/null && echo "Xvfb already running" || (Xvfb :99 -screen 0 1920x1080x24 2>/dev/null & sleep 1)
    echo ":99" > .display
    echo "DISPLAY=:99"

stop-xvfb:
    pkill -x Xvfb || true
    rm -f .display

# Run a demo or your script in linux mode using Xvfb  
# Example: just run guideframe_demos/tutors_demo/guideframe_tutors_demo.py
run file="guideframe/github_automation_tests.py":
    . {{venv}}/bin/activate
    export DISPLAY=$(cat .display 2>/dev/null || echo ":99")
    export GUIDEFRAME_BROWSER="${GUIDEFRAME_BROWSER:-$(command -v chromium || command -v google-chrome-stable || command -v google-chrome || echo "")}"
    export GUIDEFRAME_CHROMEDRIVER="${GUIDEFRAME_CHROMEDRIVER:-$(command -v chromedriver || echo "")}"
    export GUIDEFRAME_FFMPEG_CODEC="${GUIDEFRAME_FFMPEG_CODEC:-mpeg4}"
    if [ -z "${GUIDEFRAME_BROWSER:-}" ] || [ -z "${GUIDEFRAME_CHROMEDRIVER:-}" ]; then \
      echo "Browser or chromedriver not found. See README for options." >&2; \
    fi
    MODULE_NAME=$(echo "{{file}}" | sed 's/\.py$//' | tr '/' '.'); \
    echo "Running: python -m $MODULE_NAME linux"; \
    python -m $MODULE_NAME linux

# Linting placeholder (extend as needed)
lint:
    echo "No linter configured. Add ruff/flake8 if desired."

# Format placeholder (extend as needed)
fmt:
    echo "No formatter configured. Add black/isort if desired."

# One-shot all-in
bootstrap file="guideframe/github_automation_tests.py":
    just setup
    just install-deps
    just start-xvfb
    just run {{file}}
