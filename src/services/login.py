from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from src.lib.config import Config, ConfigError
from src.lib.logging import logger
from datetime import datetime
import os

def _debug_capture(page):
    debug_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'metactf', 'debug')
    os.makedirs(debug_dir, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(debug_dir, f'login_fail_{ts}.png')
    html_path = os.path.join(debug_dir, f'login_fail_{ts}.html')
    try:
        page.screenshot(path=screenshot_path, full_page=True)
        logger.error(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logger.error(f"Failed to save screenshot: {e}")
    try:
        html = page.content()
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.error(f"HTML dump saved: {html_path}")
    except Exception as e:
        logger.error(f"Failed to save HTML dump: {e}")

class LoginError(Exception):
    pass

def metactf_login(config):
    """
    Launches browser, logs in to MetaCTF, selects the target environment, and returns the page object.
    Raises LoginError on failure.
    """
    playwright = None
    browser = None
    context = None
    page = None
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        logger.info("Navigating to MetaCTF login page...")
        page.goto("https://metactf.com/login", timeout=30000)
        logger.info("Page loaded. Attempting to fill username and password fields...")
        # Wait for username field to be visible
        page.wait_for_selector('#email_input', timeout=10000)
        page.fill('#email_input', config.username)
        page.fill('#password_input', config.password)
        logger.info("Credentials filled. Submitting login form...")
        page.click('#login_page_button')
        page.wait_for_load_state("networkidle", timeout=15000)
        logger.info("Login submitted, waiting for dashboard...")
        # Wait for dashboard or error
        if page.query_selector("text=Invalid username or password"):
            raise LoginError("Invalid MetaCTF credentials.")
        logger.info(f"Selecting environment: {config.target_env}")
        page.click(f'text="{config.target_env}"')
        page.wait_for_load_state("networkidle", timeout=10000)
        # Wait for and click the correct Compete! button
        compete_buttons = page.query_selector_all('button, a')
        found = False
        for btn in compete_buttons:
            try:
                if btn.inner_text().strip() == "Compete!":
                    btn.click()
                    found = True
                    logger.info("Clicked Compete! button.")
                    break
            except Exception:
                continue
        if not found:
            raise LoginError("Could not find Compete! button after selecting environment.")
        page.wait_for_load_state("networkidle", timeout=10000)
        # Click the main menu item "Problems" to go to the problems page
        logger.info("Clicking main menu item 'Problems' to reach problems page...")
        problems_menu = None
        menu_items = page.query_selector_all('a, button')
        for item in menu_items:
            try:
                if item.inner_text().strip() == "Problems":
                    problems_menu = item
                    break
            except Exception:
                continue
        if not problems_menu:
            raise LoginError("Could not find 'Problems' menu item after Compete! button.")
        problems_menu.click()
        page.wait_for_load_state("networkidle", timeout=10000)
        logger.info("Arrived at problems page.")
        return playwright, browser, context, page
    except PlaywrightTimeoutError as e:
        logger.error(f"Timeout during login: {e}")
        if page:
            _debug_capture(page)
        raise LoginError("Timeout during MetaCTF login.")
    except Exception as e:
        logger.error(f"Login failed: {e}")
        if page:
            _debug_capture(page)
        raise LoginError(str(e))
    finally:
        # Do not close browser here; let caller handle cleanup for debugging
        pass