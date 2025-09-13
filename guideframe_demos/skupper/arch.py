from guideframe.selenium import *
from guideframe.assembly import assemble
from guideframe.utils import guide_step, get_env_settings

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""markdown
## Step 1 
A Server represents a producer endpoint. It is a program that responds to requests over TCP and is exposed using a connector.

## Step 2 
A Client represents a consumer endpoint. It initiates a request to a server and handles the response. The client capability is enabled by a listener.

## Step 3
A connector binds a local workload to listeners in remote sites. Listeners and connectors are matched using routing keys.

## Step 4
A listener binds a local connection endpoint to connectors in remote sites. Listeners and connectors are matched using routing keys.

## Step 5
On Kubernetes, an attached connector binds a local workload in a peer namespace to listeners in remote sites. Listeners and connectors are matched using routing keys.

## Step 6
Create a short-lived credential used to create a link. An access token contains the URL and secret code of a corresponding access grant.

## Step 7
Redeem a token to establish a link. This consumes the token and forms a secured router to router connection.

## Step 8
A link is a channel for communication between sites. Links carry application connections and requests. A set of linked sites constitutes a network.

## Step 9 
 a Skupper site on Kubernetes. Best when workloads are on Kubernetes and you want integration with namespaces and deployments.

## Step 10
Run a site with Podman containers on a host. Useful for edge or virtual machine scenarios without Kubernetes.

## Step 11
Run a site with Docker. Similar to Podman mode but using Docker as the container runtime.

## Step 12
Run a site under systemd units on a bare host. Good for long lived, OS managed services without a container engine.
"""

BLOCKSCAPE_URL = "https://pwright.github.io/blockscape/"

CATEGORY = '.category[data-cat]'
GRID_IN_CAT = '.grid'
TILE_NAME = '.name'
CLEAR_BUTTON = '#clear'

# Ordered by the default seed on the page
ITEMS = [
    ("endpoints", "server", "Server"),
    ("endpoints", "client", "Client"),
    ("exposure", "connector", "Connector"),
    ("exposure", "listener", "Listener"),
    ("exposure", "attachedconnector", "Attached connector"),
    ("links", "tokenissue", "Token issue"),
    ("links", "tokenredeem", "Token redeem"),
    ("links", "link", "Link"),
    ("sites", "site-k8s", "Kubernetes Site"),
    ("sites", "site-podman", "Podman Site"),
    ("sites", "site-docker", "Docker Site"),
    ("sites", "site-systemd", "systemd Site"),
]

def wait_for_any(driver, css, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, css))
    )

def wait_for_one(driver, css, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css))
    )

def scroll_center(driver, el):
    driver.execute_script('arguments[0].scrollIntoView({block: "center", inline: "center"});', el)

def click_tile(driver, cat_id: str, item_id: str):
    cat_sel = f'.category[data-cat="{cat_id}"]'
    tile_sel = f'{cat_sel} .tile[data-id="{item_id}"]'
    category = wait_for_one(driver, cat_sel)
    grid = category.find_element(By.CSS_SELECTOR, GRID_IN_CAT)
    tile = grid.find_element(By.CSS_SELECTOR, f'.tile[data-id="{item_id}"]')
    name = tile.find_element(By.CSS_SELECTOR, TILE_NAME).text
    scroll_center(driver, tile)
    tile.click()
    print(f"[Blockscape] Selected {cat_id}/{item_id} ({name})")
    return name

def guideframe_script():
    driver = None
    try:
        env_settings = get_env_settings()
        driver_location = env_settings["driver_location"]
        driver = driver_setup(driver_location)
        set_window_size(driver)

        open_url(driver, BLOCKSCAPE_URL)
        wait_for_any(driver, CATEGORY)

        # One step per item
        for step_no, (cat, item, _label) in enumerate(ITEMS, start=1):
            # Clear previous selection at the START of this step
            # so the previous item stayed selected during its entire voiceover.
            actions = []
            if step_no > 1:
                actions += [
                    lambda: click_element(driver, CLEAR_BUTTON),
                    lambda: sleep_for(0.2),
                ]
            actions += [
                lambda c=cat, i=item: click_tile(driver, c, i),
                lambda: sleep_for(0.4),  # small settle before VO starts
            ]

            guide_step(
                step_no,
                *actions,
                order="action-before-vo"  # selection persists during the VO for this step
            )

        # Optional cleanup after last step
        try:
            click_element(driver, CLEAR_BUTTON)
        except Exception:
            pass

    finally:
        print("Script complete -> moving to assembly")
        if driver:
            driver.quit()

if __name__ == "__main__":
    guideframe_script()
    assemble(len(ITEMS))
