---
title: Getting Started
layout: default
nav_order: 3
permalink: /getting-started/
---

### Getting Started

Prerequisites:
* You have installed GuideFrame as per the instructions in the [installation](https://chipspeak.github.io/GuideFrame/installation/) section of these docs.
* You have cloned or forked the GuideFrame template repository located [here](https://github.com/chipspeak/GuideFrame-Template).


### GuideFrame Script
The [GuideFrame Script Example](https://chipspeak.github.io/guideframe-py-example/) script serves as a template to get you started. It uses the magento test website as an example but the same functions can be used to interact with hrefs and elements from any website. 

Each `guide_step()` function takes a `step_number` (corresponding to the step in the accompanying markdown), function(s) called with `lambda` and an `order` argument. To illustrate this further, lets use an example from the demo.

```python
    '''
    Step 8 - Hover over the "Yoga Straps" product
    '''
    guide_step(
        8,
        lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html")
        order="action-before-vo"
        )
```

Within the above example, '8' is passed as the step argument. This always corresponds to the step within the matching markdown file. This text is in turn passed to the audio logic to create the voiceover and match it to the appropriate video step.

`lambda` allows you to pass a function from the selenium-sdk. A wide range of functions are available within this SDK and are detailed [here](https://chipspeak.github.io/selenium/).

Finally, each `guide_step` features a default argument for `order`. The default is "action-after-vo" but in the above example we've used the other option to place our voiceover after the interaction. This allows you to experiment with the video's pacing as you see fit.

### GuideFrame Markdown
The [GuideFrame Markdown Example](https://chipspeak.github.io/guideframe-md-example/) should serve to highlight the simplicity of this portion of GuideFrame. A user need only create a `## Step n` heading and place the text for that step underneath. If this format is adhered to, it will be detected appropriately by GuideFrame and used to create the voiceover.

### GuideFrame Workflow
The [GuideFrame Workflow Example](https://chipspeak.github.io/guideframe-action-example/) is triggered on push events and works to run the GuideFrame script on a GitHub runner before uploading the result as an artefact. The logic of the
workflow should be apparent. It once again serves as a simple starting point but it is advised to avoid manipulating the `Run Main Script With Display started` job in order to avoid compromising the render.