from guideframe.selenium import *  # selenium helpers (unchanged import)
from guideframe.assembly import assemble
from guideframe.utils import guide_step, get_env_settings

"""markdown
## Step 1
We’re switching to Skupper, specifically v2. Skupper is a layer-7 service interconnect for multi-cluster and hybrid. This walkthrough orients you on what’s new in v2 and where to find install, reference, and docs.

## Step 2
Start at the Skupper v2 landing page. It centralizes v2 overview, install commands, links to examples, and the v2 documentation set.

## Step 3
Open the v2 overview. v2 is a substantial change from v1, improving the model around sites, links, listeners, and connectors. It’s the baseline for everything that follows.

"""

def guideframe_script():
    driver = None
    try:
        # Setup
        env = get_env_settings()
        driver_location = env["driver_location"]
        driver = driver_setup(driver_location)
        set_window_size(driver)
        open_url(driver, "https://skupper.io/")

# ------------------- Overview ------------------- #

        # Step 1 - Skupper intro
        guide_step(1, lambda: None)

        # Step 2 - v2 landing
        guide_step(2,
            lambda: open_url(driver, "https://skupper.io/v2/index.html"),
            order="action-before-vo"
        )

        # Step 3 - v2 overview
        guide_step(3,
            lambda: open_url(driver, "https://skupper.io/v2/overview.html"),
            order="action-before-vo"
        )

    finally:
        print("Script complete -> moving to assembly")
        if driver:
            driver.quit()

if __name__ == "__main__":
    guideframe_script()
    assemble(3)
