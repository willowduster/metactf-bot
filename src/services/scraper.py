from src.lib.logging import logger
from playwright.sync_api import Page
from typing import List, Dict
import os
import json
from datetime import datetime


def scrape_problems(page: Page, save_dir: str) -> List[Dict]:
    """
    Scrape all active problems from the MetaCTF dashboard and save them to disk.
    Downloads any files/links for each problem.
    Returns a list of problem dicts.
    """
    logger.info("Scraping active problems list...")
    problems = []
    os.makedirs(save_dir, exist_ok=True)
    cards = page.query_selector_all('.problem-card')
    for idx, card in enumerate(cards):
        title = card.query_selector('.problem-title').inner_text()
        url = card.query_selector('a').get_attribute('href')
        description = card.query_selector('.problem-description').inner_text()
        links = [a.get_attribute('href') for a in card.query_selector_all('a.problem-link')]
        # Download files linked in the problem (e.g., <a class="problem-link file-link" ...>)
        file_links = [a for a in card.query_selector_all('a.problem-link') if 'file' in (a.get_attribute('class') or '')]
        problem_dir = os.path.join(save_dir, f'problem_{idx+1}')
        os.makedirs(problem_dir, exist_ok=True)
        files = []
        for file_a in file_links:
            file_url = file_a.get_attribute('href')
            if not file_url:
                continue
            filename = file_url.split('/')[-1].split('?')[0]
            file_path = os.path.join(problem_dir, filename)
            try:
                # Use Playwright to download if possible (handles auth/session)
                with page.expect_download() as download_info:
                    file_a.click()
                download = download_info.value
                download.save_as(file_path)
                logger.info(f"Downloaded file: {file_path}")
                files.append(file_path)
            except Exception as e:
                logger.error(f"Failed to download file {file_url}: {e}")
        solution_field_selector = 'input.solution-field'  # Update as needed
        problem = {
            'id': f'problem-{idx+1}',
            'title': title,
            'description': description,
            'links': links,
            'files': files,
            'solution_field_selector': solution_field_selector,
            'url': url,
        }
        problems.append(problem)
        # Save each problem as JSON
        with open(os.path.join(save_dir, f'{problem["id"]}.json'), 'w', encoding='utf-8') as f:
            json.dump(problem, f, indent=2, ensure_ascii=False)
    logger.info(f"Scraped {len(problems)} problems.")
    return problems

def get_save_dir() -> str:
    date_str = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'metactf', date_str)
