from playwright.sync_api import sync_playwright
from datetime import datetime
import os

# -----------------------------
# Configuration
# -----------------------------
HOME_URL = "https://www.cricbuzz.com"
LIVE_SCORE_URL = "https://www.cricbuzz.com/cricket-match/live-scores"

today = datetime.now().strftime("%Y-%m-%d")

os.makedirs("screenshots", exist_ok=True)

screenshot_file = f"screenshots/live_score_{today}.png"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        slow_mo=300
    )

    page = browser.new_page(
        viewport={"width": 1600, "height": 900}
    )

    print("Opening Cricbuzz Home Page...")

    page.goto(HOME_URL, wait_until="load", timeout=60000)

    # Click "Live Scores"
    page.get_by_role("link", name="Live Scores").click()

    # Wait until Live Scores page opens
    page.wait_for_url("**/cricket-match/live-scores", timeout=60000)

    page.wait_for_load_state("load", timeout=60000)

    page.wait_for_timeout(3000)

    # ------------------------------------------
    # Try to capture the first live match card
    # ------------------------------------------

    try:

        match_card = page.locator(".cb-mtch-lst").first

        match_card.wait_for(timeout=5000)

        match_card.screenshot(path=screenshot_file)

        print("Today's live match screenshot saved.")

    except:

        print("No live match card found.")

        # Capture the whole page instead
        page.screenshot(
            path=screenshot_file,
            full_page=True
        )

        print("Full page screenshot saved.")

    browser.close()

print("Done!")