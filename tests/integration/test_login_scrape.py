
import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from lib.config import Config, ConfigError
from services.login import metactf_login, LoginError
from services.scraper import scrape_problems, get_save_dir

def test_login_and_scrape(monkeypatch):
    # Skip if .env is missing or incomplete
    try:
        config = Config()
    except ConfigError:
        pytest.skip(".env missing or incomplete for integration test.")

    playwright = browser = context = page = None
    try:
        playwright, browser, context, page = metactf_login(config)
        save_dir = get_save_dir()
        problems = scrape_problems(page, save_dir)
        assert isinstance(problems, list)
        assert all('title' in p for p in problems)
        assert all('id' in p for p in problems)
        assert all('url' in p for p in problems)
    except LoginError as e:
        pytest.fail(f"Login failed: {e}")
    finally:
        if context:
            context.close()
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
