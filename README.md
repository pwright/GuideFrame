# GuideFrame

GuideFrame is a tool which allows software developers to produce detailed walkthrough videos of their projects using python code. It can be run locally, provided you have the required packages installed, or can be used as a GitHub action.

It uses a selection of open-source software to record a users screen, perform scripted UI interactions and generate a matching voiceover based on a user-defined markdown file.

## Installation

GuideFrame is currently available on PyPi. It can be installed using:`pip install guideframe`.
While GuideFrame can be run locally, given the variance in development environment, using it as part of a GitHub action is the recommended approach.

More detailed installation instructions can be found on the official docs page [here](https://chipspeak.github.io/GuideFrame/installation/).

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




