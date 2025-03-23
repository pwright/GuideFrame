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