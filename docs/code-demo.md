---
title: Code Demo
layout: default
nav_order: 1
parent: Demos
permalink: /code-demo/
---

# Code Walkthrough

The below video serves as a demonstration of GuideFrame's use in a code walkthrough of its own repository. The script used to create this can be seen below in addition to its companion markdown.

<div style="padding-bottom:56.25%; position:relative; display:block; width: 100%">
  <iframe width="100%" height="100%"
    src="https://www.youtube.com/embed/EZVsS7ulclA?si=e6vvEdKAOXTbeTLe"
    frameborder="0" allowfullscreen="" style="position:absolute; top:0; left: 0">
  </iframe>
</div>

## GuideFrame Code Walkthrough Script
```python

from guideframe.selenium import * # Moved all selenium functions to external file
from guideframe.assembly import assemble  # Importing the assemble_clips function from assembly.py
from guideframe.utils import guide_step, get_env_settings  # Importing the guide_step and get_env_settings functions from guideframe_utils.py

# Function to run the full script
def guideframe_script():
    try:
        '''
        Setup - Setup driver, Open GuideFrame repo and set window size etc
        '''
        env_settings = get_env_settings()  # Getting the environment settings
        driver_location = env_settings["driver_location"]  # Getting the driver location from the settings
        driver = driver_setup(driver_location) # Initializing driver as the return value from the setup function in selenium script
        set_window_size(driver)
        open_url(driver, "https://github.com/chipspeak/GuideFrame")

#-------------------Overview-------------------#

        '''
        Step 1 - Open GitHub Page
        '''
        guide_step(
            1, 
            lambda: None
            )
        
        '''
        Step 2 - open tutors test file
        '''
        guide_step(
            2,
            lambda: open_url(driver, "https://github.com/chipspeak/GuideFrame/tree/main/selenium_demos"),
            lambda: open_url(driver, "https://github.com/chipspeak/GuideFrame/blob/main/selenium_demos/selenium_function_demo.py"),
            order="action-before-vo"
            )

        '''
        Step 3 - Open markdown file in new tab
        '''
        guide_step(
            3,
            lambda: open_link_in_new_tab(driver, "https://github.com/chipspeak/GuideFrame/blob/main/selenium_demos/selenium_function_demo.md"),
            lambda: click_element_by_xpath(driver, '//*[@id="repos-sticky-header"]/div[1]/div[2]/div[1]/ul/li[2]/button/span/div'),
            order="action-before-vo"
            )

        '''
        Step 4 - Switch back to main script, move to environment setup
        '''
        guide_step(
            4,
            lambda: switch_to_tab(driver, 0),
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/selenium_demos/selenium_function_demo.py#L6-L13"),
            order="action-before-vo"
            )
        
        '''
        Step 5 - Move to step 1 and 2 highlight step syntax
        '''
        guide_step(
            5,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/selenium_demos/selenium_function_demo.py#L16-L31"),
            order="action-before-vo"
            )
        
        '''
        Step 6 - Explain multiple actions
        '''
        guide_step(
            6,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/selenium_demos/selenium_function_demo.py#L134-L142"),
            order="action-before-vo"
            )
        
        '''
        Step 7 - Illustrate main and explain assembly
        '''
        guide_step(
            7,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/selenium_demos/selenium_function_demo.py#L186-L189"),
            order="action-before-vo"
            )
        
#-------------------Demonstration-------------------#

        '''
        Step 8 - Demo function 1 - explain
        '''
        guide_step(
            8,
            lambda: open_url(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/selenium.py#L139-L149"),
            order="action-before-vo"
            )
        
        '''
        Step 9 - Demo function 1 - demonstrate
        '''
        guide_step(
            9,
            lambda: open_link_in_new_tab(driver, "https://magento.softwaretestingboard.com/"),
            lambda: click_button_by_span_text(driver, "AGREE"),
            )
        
        '''
        Step 10 - Demo function 2 - explain
        '''
        guide_step(
            10,
            lambda: switch_to_tab(driver, 0),
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/selenium.py#L115-L124"),
            order="action-before-vo"
            )
        
        '''
        Step 11 - Demo function 2 - demonstrate
        '''
        guide_step(
            11,
            lambda: switch_to_tab(driver, 2),
            lambda: sleep_for(1),
            lambda: click_element(driver, ".authorization-link > a"),
            lambda: sleep_for(1),
        )
        
        '''
        Step 12 - Demo function 3 - explain
        '''
        guide_step(
            12,
            lambda: switch_to_tab(driver, 0),
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/selenium.py#L127-L136"),
            order="action-before-vo"
            )
        
        '''
        Step 13 - Demo function 3 - demonstrate
        '''
        guide_step(
            13,
            lambda: switch_to_tab(driver, 2),
            lambda: sleep_for(1),
            lambda: type_into_field(driver, "email", "test-user@email.com"),
            lambda: sleep_for(1),
            lambda: type_into_field(driver, "pass", "testuser-1"),
        )
        
        '''
        Step 14 - Demo function 4 - explain
        '''
        guide_step(
            14,
            lambda: switch_to_tab(driver, 0),
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/selenium.py#L100-L112"),
            order="action-before-vo"
            )
        
        '''
        Step 15 - Demo function 4 - demonstrate
        '''
        guide_step(
            15,
            lambda: switch_to_tab(driver, 2),
            lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/women.html"),
            lambda: sleep_for(1),
            lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/women/tops-women.html"),
            lambda: sleep_for(1),
            lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/women/tops-women/jackets-women.html"),
            lambda: sleep_for(1),
            lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/men.html"),
            lambda: sleep_for(1),
            lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/men/tops-men.html"),
            lambda: sleep_for(1),
            lambda: hover_over_element(driver, "https://magento.softwaretestingboard.com/men/tops-men/jackets-men.html"),            
            )

#-------------------Core Logic Walkthrough-------------------#

        '''
        Step 16 - Move to utils file - get_env_settings
        '''
        guide_step(
            16,
            lambda: switch_to_tab(driver, 0),
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/utils.py#L6-L29"),
            order="action-before-vo"
            )
        
        '''
        Step 17 - Move to utils file - extract filenames
        '''
        guide_step(
            17,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/utils.py#L32-L40"),
            order="action-before-vo"
            )
        
        '''
        Step 18 - Move to utils file - guide_step
        '''
        guide_step(
            18,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/utils.py#L42-L65"),
            order="action-before-vo"
            )
        
        '''
        Step 19 - Move to audio file
        '''
        guide_step(
            19,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/audio.py#L52-L65"),
            order="action-before-vo"
            )
        
        '''
        Step 20 - Move to video file
        '''
        guide_step(
            20,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/video.py#L9-L29"),
            order="action-before-vo"
            )
        
        '''
        Step 21 - Move to assembly file - audio + video
        '''
        guide_step(
            21,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/assembly.py#L10-L29"),
            order="action-before-vo"
            )
        
        '''
        Step 22 - Move to assembly file - assemble_clips
        '''
        guide_step(
            22,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/assembly.py#L32-L54"),
            order="action-before-vo"
            )
        
        '''
        Step 23 - Move to assembly file - assemble
        '''
        guide_step(
            23,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/assembly.py#L57-L75"),
            order="action-before-vo"
            )
        
        '''
        Step 24 - Move to assembly file - cleanup
        '''
        guide_step(
            24,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/guideframe/assembly.py#L77-L95"),
            order="action-before-vo"
            )
        
#-------------------Workflow walkthrough-------------------#

        '''
        Step 25 - Move to workflows
        '''
        guide_step(
            25,
            lambda: open_url(driver, "https://github.com/chipspeak/GuideFrame/tree/main/.github/workflows"),
            order="action-before-vo"
            )   
        
        '''
        Step 26 - Move to workflows - render.yaml
        '''
        guide_step(
            26,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/.github/workflows/render.yaml#L1-L25"),
            order="action-before-vo"
            )
        
        '''
        Step 27 - Move to workflows - render.yaml pt 2
        '''
        guide_step(
            27,
            lambda: highlight_github_code(driver, "https://github.com/chipspeak/GuideFrame/blob/main/.github/workflows/render.yaml#L26-L40"),
            order="action-before-vo"
            )
        
#-------------------Conclusion-------------------# 

        '''
        Step 28 - GitHub page
        '''
        guide_step(
            28,
            lambda: open_url(driver, "https://github.com/chipspeak/GuideFrame"),
            order="action-before-vo"
            )
        
        '''
        Step 29 - PyPi page
        '''
        guide_step(
            29,
            lambda: open_url(driver, "https://pypi.org/project/guideframe/"),
            order="action-before-vo"
            )
        
        '''
        Step 30 - Docs page
        '''
        guide_step(
            30,
            lambda: open_url(driver, "https://chipspeak.github.io/GuideFrame/"),
            order="action-before-vo"
            )
        
#-------------------Walkthrough Complete-------------------# 
    
    finally:
        print("Script complete -> moving to assembly")
        driver.quit()


# Main function to run the test and assemble the clips (now passing the number of steps to the assembly function)
if __name__ == "__main__":
    guideframe_script()
    assemble(30)
```

## GuideFrame Code Walkthrough Markdown

```markdown
## Step 1 
Guide-Frame is a tool which allows software engineers to generate walkthrough videos using python. This demo aims to illustrate the functionality of Guide-Frame by examining its codebase. Before we dive into the underlying logic, lets first examine a Guide-Frame script in order to provide some broader context.

## Step 2
The selenium functions demo will serve as an example of a GuideFrame script. Each script is a python file and must also have a markdown file with a matching name. Let's briefly touch on the format and role of this markdown file. 

## Step 3
GuideFrame creates the voiceover based on this markdown file. It simply requires a user to create a ## heading with the text 'Step Number'. Under this heading, the user can add whatever text corresponds to the actions they define in the main GuideFrame script. This promotes ease of adjustment in the event of purely audio changes. Lets switch back to the main script and run through some of the setup syntax.

## Step 4
All the python script requires is the relevant imports as seen at the top of the file. A user should then define a guideframe script function, as seen here on line 7. After some initial environment setup, via the functions imported from the GuideFrame package, a user can start defining their GuideFrame steps.

## Step 5
Let's examine steps 1 and 2 to illustrate the syntax of a GuideFrame step. Each step takes a number as an argument in addition to a lambda function and an opptional argument for the order of the voicever relative to the interactions. In the case of step 1, lambda is set to none in order to hang on the main webpage while the voiceover is performed. Step 2 features a call to the click button by span text function to click the agree button. 

## Step 6
Lets skip to step 14 to demonstrate the ability to pass multiple actions. In this case, we're filling review fields on the test site. A user can pass as many actions to a step as they wish and GuideFrame will iterate through them.

## Step 7
Once a user has defined all of their guide steps within a function, they should call it within main. They should then pass the number of steps to the assemble function. This function carries out the assembly of all generated audio and video segments. Now that we've got a high level understanding of GuideFrame, let's take a look at the underlying code.

## Step 8
Let's start off by examining one of the selenium functions. The selenium file acts as an SDK which allows users to more easily create individual interactions. There are numerous actions available but for this demonstration we'll use a small subset. The first one we'll look at is the open link in new tab function. Like most of these functions, its wrapped in a try block with exception handling. The function takes the webdriver and a h ref as an argument. The h ref is then passed to selenium's native functions. It opens the link and then switches to the most recently opened tab. 

## Step 9
Lets demonstrate it by using the magento test site. We'll use the function to open the test site in a new tab and switch to it.

## Step 10
The click element function takes a driver and a C S S selector as arguments. It uses selenium's functionality to wait for the element to appear and then clicks on it. 

## Step 11
Let's return to the test site to demonstrate that. In this case we'll click on the sign in button. 

## Step 12
The type into field function takes the driver, element i d and text as arguments. It uses seleniums ability to pass text into form fields to achieve its purpose. 

## Step 13
Let's switch back to magento to see it in action. In this case we can fill the login details. We achieve this by using two different functions within one guide step. 

## Step 14
The final function we'll examine allows a user to hover over elements. This function takes a h ref as an argument. It uses selenium's action chains to move to the h ref's element. 

## Step 15
When defining this particular step, we also pass sleep functions to allow space between selections. 

## Step 16
Now that we've demonstrated some of the functions, lets dive a little deeper into the code that makes this possible. The utils file contains much of the logic relating to the guide steps themselves. The function seen here uses script arguments to extract environment variables.

## Step 17
This pair of functions simply serve to extract the scripts name for use in additional logic.

## Step 18
The guide step function orchestrates much of the core logic via calls to various functions. It extracts environment data and then passes this to f f m peg to begin a screen recording. It then checks the order variable and loops through the actions passed as arguments. The generate voiceover function is then called based on the order. This takes the step number and markdown file in order to pull the text from its match. Finally, the function ends by stopping the f f m peg recording.

## Step 19
Much of the remaining logic should be relatively clear. Within the audio file, regex is used to extract the text under the markdown headings. This is then passed to the generate voiceover function. This uses g t t s to create the audio clip. Finally, an additional function sleeps based on the length of this audio clip. This ensures that interactions don't occur until a voiceover segment is complete.

## Step 20
The video file simply contains the functions called in the guide steps. They start and stop f f mpeg, taking the environment variables previously mentioned.

## Step 21
The assembly file is where the audio and video segments for each step are combined. This first function checks for the existence of the matching audio and video files. f f m peg is then used to combine them into a single video with voiceover.

## Step 22
The combine all videos function takes the output files and a name as arguments. It then writes these to a text file. This list of files is then passed to f f m peg for concatination. The final file name is dictated by the second function argument.

## Step 23
The assemble function takes the steps number and uses it to loop through all of the created files. It then passes these to the assemble audio video function mentioned earlier. It then creates the required name and an array based on the combined files. Both the array and filename are then passed to the combine all videos function.

## Step 24
Finally, a cleanup loop removes all of the files generated through this process. 

## Step 25
The final layer of guideframe is its use as a git hub action. This allows users to run guideframe on repository updates.

## Step 26
This render workflow activates on push events. It spins up an ubuntu git hub runner and installs the requirements needed to run guideframe. Note the pip install commands here don't install the guideframe package. This is because this workflow runs within the source repository. Within the template repository, these python installations are replaced with pip install guideframe.

## Step 27
Once the environment is set up, the virtual display is started. The tutors demo is then run before a final step uploads this output as an artifact. This allows the user to download the final mp4 from the workflow.

## Step 28
This concludes the code walkthrough. GuideFrame is available on GitHub via the link seen here.

## Step 29
It can also be found here on PyPi.

## Step 30
And finally, the official documentation can be found here. Thanks for watching!
```
