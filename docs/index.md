---
title: Overview
layout: home
nav_order: 1
---

# GuideFrame

GuideFrame is a tool to allow software developers to produce detailed walkthrough videos of their projects using python code. It comes in the form of a python package which leverages numerous open source technologies. 

At a high level, it allows the user to codify their video material, ensuring ease of reproduction. It aims to circumvent some of the presumed skills required of an engineer to produce engaging video content.
Its intended use is as a GitHub action. In this guise, GuideFrame can exist in a CI/CD pipeline where code changes can prompt a fresh render of a walkthrough video. 

It allows users to define a script in plain markdown which will be consumed by GuideFrame's audio functions. This will in turn be applied to an interaction-based script which will carry out actions in a web UI and record the process. GuideFrame assembles all of these elements in order to render a complete video with recorded video interactions and matching voiceover.

The current iteration of GuideFrame is in Beta and is being submitted as a final project for the HDip in Computer Science in SETU.
