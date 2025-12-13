from lib.logging import logger
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
    # Only select .panel elements (problems)
    cards = page.query_selector_all('.problem-card, .card.problem, .card, .panel')
    print(f"[DEBUG] Found {len(cards)} candidate problem panels.")
    if not cards:
        logger.error("No problem panels found. Check selector or page structure.")
        return problems
    cards = cards[:3]  # Only process the first 3 problems for testing
    skipped = 0
    for idx, card in enumerate(cards):
        # Skip if no .panel-body.problem-content (not a real problem)
        content = card.query_selector('.panel-body.problem-content')
        if not content:
            print(f"[DEBUG] Skipping panel {idx+1}: no .panel-body.problem-content found.")
            skipped += 1
            continue
        # Title: .panel-heading .panel-title span (first span)
        try:
            title = card.query_selector('.panel-heading .panel-title span').inner_text().strip()
        except Exception:
            title = f"Problem {idx+1}"
        # Description: first <p> in .panel-body.problem-content
        try:
            description = content.query_selector('p').inner_text().strip()
        except Exception:
            description = ""
        # Links: all <a href> in .panel-body.problem-content
        links = []
        for a in content.query_selector_all('a[href]'):
            href = a.get_attribute('href')
            if href:
                links.append(href)
        # Download files: any <a> with file-like href
        file_links = [a for a in content.query_selector_all('a[href]') if any(ext in a.get_attribute('href') for ext in ['.zip','.txt','.pdf','.doc','.csv','.bin','.exe','.tar','.gz','.7z','.rar','.pcap','places.sqlite'])]
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
                # Track open pages before download
                context = page.context
                pages_before = set(context.pages)
                # Use a short timeout for download event
                with page.expect_download(timeout=5000) as download_info:
                    file_a.click()
                    # Immediately close any new tab opened by the click
                    pages_after = set(context.pages)
                    new_pages = pages_after - pages_before
                    for new_page in new_pages:
                        if new_page != page:
                            logger.info("Closing extra tab opened for download (immediate cleanup).")
                            new_page.close()
                    # Ensure main problems page is visible (bring to front)
                    page.bring_to_front()
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
            'url': None,
        }
        problems.append(problem)
        # Save each problem as JSON
        with open(os.path.join(save_dir, f'{problem["id"]}.json'), 'w', encoding='utf-8') as f:
            json.dump(problem, f, indent=2, ensure_ascii=False)
    print(f"[DEBUG] Skipped {skipped} panels without problem content.")
    logger.info(f"Scraped {len(problems)} problems.")
    return problems

def get_save_dir() -> str:
    date_str = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'metactf', date_str)
