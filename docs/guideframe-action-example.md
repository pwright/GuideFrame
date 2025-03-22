---
title: GuideFrame Workflow Example
layout: default
nav_order: 3
parent: Samples
permalink: /guideframe-action-example/
---

# GuideFrame Workflow Example

```yaml
name: GuideFrame Video Render
# Trigger the workflow on push
on: [push]
# All jobs in the workflow
jobs:
  magento-test:
    runs-on: ubuntu-latest
    # steps to run
    steps:
    # Checkout the code
    - name: Checkout code
      uses: actions/checkout@v2
    # Set up the environment required by GuideFrame
    - name: Set up environment
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          ffmpeg \
          xvfb \
          chromium-driver \
          chromium-browser
          pip install guideframe
    # Run the main script (starting the virtual display first)
    - name: Run Main Script with Display started
      run: |
        # Start Xvfb
        export DISPLAY=:99
        nohup Xvfb :99 -screen 0 1920x1080x24 &
        
        # Run the Python script
        python3 guideframe_demo.py github
    # Upload the screen recording as an artifact
    - name: Upload screen recording as artifact
      uses: actions/upload-artifact@v4
      with:
        name: guideframe-demo
        path: ./guideframe_demo*.mp4
```