from guideframe.selenium import *  # your helper SDK (click_element, open_url, sleep_for, etc.)
from guideframe.assembly import assemble
from guideframe.utils import guide_step, get_env_settings

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""markdown
## Step 1
Open Blockscape and wait for the first category to render.

## Step 2
Within the first category only, click the first two tiles (in order), pausing briefly and clearing selection after each.
"""

# ---------------- Selectors ----------------
BLOCKSCAPE_URL = "https://pwright.github.io/blockscape/"

CATEGORY = ".category[data-cat]"           # Any category section
GRID_IN_CAT = ".grid"                      # The grid inside a category
TILE_IN_CAT = ".tile"                      # Tiles within a category's grid
TILE_NAME = ".name"
CLEAR_BUTTON = "#clear"

# If you want strict CSS for “first two tiles in first category”, these work too:
# FIRST_CATEGORY_CSS = '.category[data-cat]:nth-of-type(1)'
# FIRST_TILE_CSS     = '.category[data-cat]:nth-of-type(1) .grid .tile:nth-of-type(1)'
# SECOND_TILE_CSS    = '.category[data-cat]:nth-of-type(1) .grid .tile:nth-of-type(2)'

# ---------------- Small helpers ----------------
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

def click_first_two_tiles_in_first_category(driver, pause_seconds=0.7):
    # Ensure categories exist
    wait_for_any(driver, CATEGORY)
    categories = driver.find_elements(By.CSS_SELECTOR, CATEGORY)
    if not categories:
        raise RuntimeError("No categories found on Blockscape page.")

    first_cat = categories[0]
    grid = first_cat.find_element(By.CSS_SELECTOR, GRID_IN_CAT)
    tiles = grid.find_elements(By.CSS_SELECTOR, TILE_IN_CAT)
    if len(tiles) < 2:
        raise RuntimeError(f"Expected at least 2 tiles in first category, found {len(tiles)}.")

    # Work on the first two tiles only
    for idx, tile in enumerate(tiles[:2], start=1):
        # Defensive re-fetch (avoid stale element if layout reflows)
        first_cat = driver.find_elements(By.CSS_SELECTOR, CATEGORY)[0]
        grid = first_cat.find_element(By.CSS_SELECTOR, GRID_IN_CAT)
        tile = grid.find_elements(By.CSS_SELECTOR, TILE_IN_CAT)[idx - 1]

        name = tile.find_element(By.CSS_SELECTOR, TILE_NAME).text
        tile_id = tile.get_attribute("data-id")

        scroll_center(driver, tile)
        tile.click()
        print(f"[Blockscape] Clicked tile {idx}: id={tile_id}, name='{name}' in first category")
        sleep_for(pause_seconds)

        # Clear selection before moving on
        click_element(driver, CLEAR_BUTTON)
        sleep_for(0.25)

# ---------------- GuideFrame script ----------------
def guideframe_script():
    driver = None
    try:
        env_settings = get_env_settings()
        driver_location = env_settings["driver_location"]
        driver = driver_setup(driver_location)
        set_window_size(driver)

        # Step 1 — open page, wait for first category
        guide_step(
            1,
            lambda: open_url(driver, BLOCKSCAPE_URL),
            lambda: wait_for_any(driver, CATEGORY),
            order="action-before-vo"
        )

        # Step 2 — only first two tiles in the first category
        guide_step(
            2,
            lambda: click_first_two_tiles_in_first_category(driver, pause_seconds=0.7),
            order="action-before-vo"
        )

    finally:
        print("Script complete -> moving to assembly")
        if driver:
            driver.quit()

if __name__ == "__main__":
    guideframe_script()
    assemble(2)
