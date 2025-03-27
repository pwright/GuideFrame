---
title: Tutors Demo
layout: default
nav_order: 3
parent: Demos
permalink: /tutors-demo/
---

# Code Walkthrough

The below video serves as a demonstration of GuideFrame via the open-source education platform, Tutors. The script used to create this can be seen below in addition to its companion markdown.

<div style="padding-bottom:56.25%; position:relative; display:block; width: 100%">
  <iframe width="100%" height="100%"
    src="https://www.youtube.com/embed/Hq5pKuotsac?si=nryPLkZiRFdQFv0j"
    frameborder="0" allowfullscreen="" style="position:absolute; top:0; left: 0">
  </iframe>
</div>

## Tutors Demo Script
```python

from guideframe.selenium import * # Moved all selenium functions to external file
from guideframe.assembly import assemble  # Importing the assemble_clips function from assembly.py
from guideframe.utils import guide_step, get_env_settings  # Importing the guide_step and get_env_settings functions from guideframe_utils.py


# Function to run the main walkthrough section
def guideframe_script():
    try:
        '''
        Setup - Setup driver and Open Tutors.dev and set window size etc
        '''
        env_settings = get_env_settings()  # Getting the environment settings
        driver_location = env_settings["driver_location"]  # Getting the driver location from the settings
        driver = driver_setup(driver_location) # Initializing driver as the return value from the setup function in selenium script
        set_window_size(driver)
        open_url(driver, "https://tutors.dev")

        '''
        Step 1 - Open Tutors
        '''
        guide_step(
            1, 
            lambda: None,
            )
        
        '''
        Step 2 - setting dark mode
        '''
        guide_step(
            2,
            lambda: click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block"),
            lambda: sleep_for(0.5),
            lambda: click_element(driver, "label[data-testid='segment-item']"),
            lambda: sleep_for(0.5),
            lambda: click_element(driver, "span.ml-2.hidden.text-sm.font-bold.md\\:block"),
            )

        '''
        Step 3 - navigating to the docs page
        '''
        guide_step(
            3,
            lambda: hover_and_click(driver, "/course/tutors-reference-manual"),
            )

        '''
        Step 4 - Docs page intro
        '''
        guide_step(
            4,
            lambda: None
            )

        '''
        Step 5 - Hovering over the first card
        '''
        guide_step(
            5,
            lambda: hover_over_element(driver, "/note/tutors-reference-manual/unit-0-getting-started/note-01-getting-started"),
            order="action-before-vo"
            )

        '''
        Step 6 - Hovering over the second card
        '''
        guide_step(
            6,
            lambda: hover_over_element(driver, "/course/tutors-starter-course"),
            order="action-before-vo"
            )

        '''
        Step 7 - Hovering over the third card
        '''
        guide_step(
            7,
            lambda: hover_over_element(driver, "/course/layout-reference-course"),
            order="action-before-vo"
            )

        '''
        Step 8 - Hovering over the fourth card
        '''
        guide_step(
            8,
            lambda: scroll_to_element(driver, "/course/reference-course"),
            lambda: hover_over_element(driver, "/course/reference-course"),
            order="action-before-vo"
            )

        '''
        Step 9 - Click the search button
        '''
        guide_step(
            9,
            lambda: click_element_by_xpath(driver, '/html/body/div[1]/div[1]/header/header/section/div[3]/div[1]/div[3]/button/div/span[2]'),
            )
        
        '''
        Step 10 - Search for a term
        '''
        guide_step(
            10,
            lambda: type_into_field(driver, "search", "card"),
            )
        
        '''
        Step 11 - Open the search result in a new tab
        '''
        guide_step(
            11,
            lambda: open_link_in_new_tab(driver, "https://tutors.dev/note/tutors-reference-manual/unit-1-fundamentals/note-02-cards")
        )
        
        '''
        Step 12 - End demo
        '''
        guide_step(
            12,
            lambda: None
        )
        

    finally:
        print("Script complete -> moving to assembly")
        driver.quit()


# Main function to run the test and assemble the clips
if __name__ == "__main__":
    guideframe_script()
    assemble(12)
```

## Tutors Demo Markdown

```markdown
## Step 1 
This brief GuideFrame demo begins by opening tutors.dev. This is achieved by using the open u r l function prior to step 1.

## Step 2
We can demonstrate the ability to pass multiple actions to GuideFrame by activating dark mode. This involves 3 calls to the click element function. We'll also call the sleep function for 0.5 seconds between each action.

## Step 3
Now let's use the hover and click function to move to the tutors reference manual.

## Step 4
We can pass None to lambda in order to hang on a page. This is useful for when you wish to simply add voiceover to a static page. Let's use the hover over element function a few times here. We'll also pass the order argument. This ensures that the action begins before the voiceover.

## Step 5
We'll start with the getting started card.

## Step 6
Now let's move on to the simple starter card.

## Step 7
Let's continue to the alternative starter card. Before using the scroll to element function to move to the reference course.

## Step 8
In this case, we use this function to access an element that may not be in the display window.

## Step 9
Let's use the click element by xpath function. We'll use it to access the search bar at the top of the screen.

## Step 10
With the search bar open, let's use the type into field function to type in card.

## Step 11
Let's open the link in the first result in a new tab. We can do this by using the open link in new tab function.

## Step 12
And that concludes this GuideFrame demonstration.
```
