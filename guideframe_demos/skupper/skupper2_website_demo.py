from guideframe.selenium import *  # selenium helpers (unchanged)
from guideframe.assembly import assemble
from guideframe.utils import guide_step, get_env_settings

"""markdown
## Step 1
Welcome to the Skupper site preview. We'll get oriented to v2, show the easiest install paths, and point to the docs, references, examples, and community.

## Step 2
This gives a concise, step-by-step path using a simple multi-namespace Hello World.

## Step 3
It shows two straightforward install options: kubectl apply or Helm.

## Step 4
This is the one-liner you can use with kubectl to install the controller and CRDs.

"""

def guideframe_script():
    driver = None
    try:
        # Setup
        env = get_env_settings()
        driver_location = env["driver_location"]
        driver = driver_setup(driver_location)
        set_window_size(driver)
        open_url(driver, "https://www.ssorj.net/skupper-website/")

        # ------------------- Overview ------------------- #

        # Step 1 - Home (hang for VO)
        guide_step(1, lambda: None)

        # Step 2 - Getting started
        guide_step(
            2,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/start/index.html"),
            order="action-before-vo",
        )

        # Step 3 - Install on Kubernetes (docs)
        guide_step(
            3,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/installation/kubernetes.html"),
            order="action-before-vo",
        )

        # Step 4 - show install YAML via docs page (renders inline; no download)
        guide_step(
            4,
            lambda: open_url(driver, "https://skupperproject.github.io/skupper-docs/install/index.html"),
            order="action-before-vo"
        )
        

    finally:
        print("Script complete -> moving to assembly")
        if driver:
            driver.quit()

if __name__ == "__main__":
    guideframe_script()
    assemble(4)
