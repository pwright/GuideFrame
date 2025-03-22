---
title: Installation
layout: default
nav_order: 2
permalink: /installation/
---

# How to Install GuideFrame

The following section will walk a user through the installation/setup of GuideFrame. This guide is written from 2 perspectives: 

1. A user who simply wishes to run GuideFrame on their GitHub repository.
2. A user who also wishes to run GuideFrame locally.

## GitHub Installation

GuideFrame is intended for use as part of a GitHub CI/CD pipeline. This involves featuring a GuideFrame script within your repository along with an appropriate GitHub action triggering it. 

In the interest of illustrating this, a template repository has been created and can be found [here](
https://github.com/chipspeak/GuideFrame-Template).

## Local Installation
GuideFrame is packaged and available on pypi. It can be installed using:

```pip install guideframe```

Once installed, you will need to install the non-python dependencies. A setup script is packaged with GuideFrame for this. You can simply copy it from the GuideFrame repo and run it locally or you can run the following:

```bash $(python -c "import guideframe, os; print(os.path.join(os.path.dirname(guideframe.__file__), 'setup_env.sh'))")```

Alternatively, depending on you operating system, you can run the following to install the package and dependencies in one:

```bash
  sudo apt-get update
  sudo apt-get install -y \
    ffmpeg \
    xvfb \
    chromium-driver \
    chromium-browser
    pip install guideframe
```

You will then need to create a GuideFrame script. See the repository link above for a template. Once this script has been created, you can run it using:

```bash python <guideframe_script_name> <system_argument>```

Note: GuideFrame currently supports ```macos``` as its system argument. You can also pass: ```github``` to run on an ubuntu system but this has not been tested outside of virtual machines.