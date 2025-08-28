# GuideFrame

GuideFrame is a tool which allows software developers to produce detailed walkthrough videos of their projects using python code. It can be run locally, provided you have the required packages installed, or can be used as a GitHub action.

It uses a selection of open-source software to record a users screen, perform scripted UI interactions and generate a matching voiceover based on a user-defined markdown file. To see GuideFrame in action you can visit the [Demos section of the GuideFrame Site](https://chipspeak.github.io/GuideFrame/demos/).

## Installation

GuideFrame can be installed in several ways depending on your use case:

### Quick Start with PyPI (Recommended for Users)

```bash
pip install guideframe
```

**Note:** You'll also need to install system dependencies (see below) for GuideFrame to work properly.

### Development Installation

For contributors or advanced users who want to modify GuideFrame:

```bash
# Clone the repository
git clone https://github.com/chipspeak/GuideFrame.git
cd GuideFrame

# Install with pip in editable mode
pip install -e .
```

### Automated Setup (Linux)

For the easiest setup on Linux systems, use the included Justfile automation:

```bash
# Install Just first: https://github.com/casey/just
# Then run automated setup
just setup        # Install system dependencies
just install-deps # Create virtual environment and install Python dependencies
```

### System Dependencies

GuideFrame requires several system packages to function:

**For Fedora/RHEL/CentOS:**
```bash
sudo dnf install -y ffmpeg xorg-x11-server-Xvfb chromium chromedriver python3-venv
```

**For Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg xvfb chromium-driver chromium-browser python3-venv
```

**For Arch Linux:**
```bash
sudo pacman -Syu --noconfirm ffmpeg xorg-server-xvfb chromium chromedriver python-virtualenv
```

### GitHub Actions (Recommended for CI/CD)

GuideFrame works excellently as a GitHub Action. Use the [GuideFrame Template Repository](https://github.com/chipspeak/GuideFrame-Template) to get started quickly without dealing with local dependencies.

### Verification

To verify your installation works:

```bash
# Start virtual display (Linux only)
just start-xvfb  # or manually: Xvfb :99 -screen 0 1920x1080x24 &

# Run a demo
just run guideframe_demos/tutors_demo/guideframe_tutors_demo.py
```

For more detailed installation instructions, visit the [official documentation](https://chipspeak.github.io/GuideFrame/installation/).

## Getting Started

If you simply want to get started, a template repository exists to enable users to dive in without the need to navigate local dependencies, python environments etc. Simply clone or fork the repository listed below to have access to a correctly configured template. You can then modify the GuideFrame script and markdown as needed for your purpose. Then you need only enable the GitHub action to begin your first render.

[GuideFrame Template Repository](https://github.com/chipspeak/GuideFrame-Template)

## Samples

If you wish to view the syntax of GuideFrame through the lense of examples, see the below links.

**Tutors Demo** - A brief GuideFrame walkthrough using [tutors.dev](tutors.dev)
* [GuideFrame Tutors Demo script](https://github.com/chipspeak/GuideFrame/blob/main/guideframe_demos/tutors_demo/guideframe_tutors_demo.py)
* [GuideFrame Tutors Demo markdown](https://github.com/chipspeak/GuideFrame/blob/main/guideframe_demos/tutors_demo/guideframe_tutors_demo.md)
* [GuideFrame Tutors Demo video](https://www.youtube.com/watch?v=Hq5pKuotsac)

**Magento Demo** - A GuideFrame selenium function demo using the [Magento test site](https://magento.softwaretestingboard.com/)
* [GuideFrame Magento Demo script](https://github.com/chipspeak/GuideFrame/blob/main/selenium_demos/selenium_function_demo.py)
* [GuideFrame Magento Demo markdown](https://github.com/chipspeak/GuideFrame/blob/main/selenium_demos/selenium_function_demo.md)
* [GuideFrame Magento Demo video](https://www.youtube.com/watch?v=O9Mt2SXts-0)

**GuideFrame Code Walkthrough** - An elaborate GuideFrame walkthrough where it works through its own code.
* [GuideFrame Code Walkthrough script](https://github.com/chipspeak/GuideFrame/blob/main/guideframe_demos/guideframe_code_demo/guideframe_code_demo.py)
* [GuideFrame Code Walkthrough markdown](https://github.com/chipspeak/GuideFrame/blob/main/guideframe_demos/guideframe_code_demo/guideframe_code_demo.md)
* [GuideFrame Code Walkthrough video](https://www.youtube.com/watch?v=EZVsS7ulclA)

## Additional Links
* [GuideFrame On PyPi](https://pypi.org/project/guideframe/)
* [GuideFrame Official Docs](https://chipspeak.github.io/GuideFrame/)

## Technologies Used
* [`ffmpeg`](https://www.ffmpeg.org/) - used to capture the virtual displays and combine clips.
* [`gTTS`](https://pypi.org/project/gTTS/) - used to generate the voiceover audio.
* [`xvfb`](https://linux.die.net/man/1/xvfb) - used to provide a virtual display server.
* [`mutagen`](https://mutagen.readthedocs.io/en/latest/index.html) - used to parse MP3 length.
* [`chromium`](https://www.chromium.org/Home/) - to provide a browser for interactions.
* [`selenium`](https://pypi.org/project/selenium/) - the python package for interacting with the browser.

## How To Contribute
GuideFrame is an open-source project and contributions are greatly encouraged. Open an issue thread or fork the repo and open a pull request if you've got suggestions, fixes etc. 

## Environment Configuration

### Optional Environment Variables

You can customize GuideFrame's behavior with these environment variables:

```bash
# Override browser and driver paths if needed
export GUIDEFRAME_BROWSER=/usr/bin/chromium
export GUIDEFRAME_CHROMEDRIVER=/usr/bin/chromedriver

# Override FFmpeg codec (default is libx264)
export GUIDEFRAME_FFMPEG_CODEC=libxvid
```

### Notes
- Screen capture uses `Xvfb :99` with `x11grab`, which works on both Wayland and X11 systems
- `requirements.txt` contains only Python dependencies; system packages must be installed separately via your distribution's package manager
