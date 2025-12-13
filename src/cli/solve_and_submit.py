
import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'src')))
from services.solver import solve_all_problems
from lib.logging import logger
from lib.config import Config
from services.login import metactf_login, LoginError
from services.scraper import scrape_problems, get_save_dir

def submit_flag(page, problem, flag):
    prob_num = problem['id'].split('-')[-1]
    form = None
    input_field = None
    submit_btn = None
    # Try to find input by id first
    input_by_id = page.query_selector(f"input#inp{prob_num}.form-control")
    if input_by_id:
        input_field = input_by_id
        form = input_field.evaluate_handle('el => el.closest("form")')
    else:
        input_field = page.query_selector('input.form-control')
        if input_field:
            form = input_field.evaluate_handle('el => el.closest("form")')
    if not input_field or not form:
        logger.error(f"No input field or form found for problem {problem['id']}")
        return False
    submit_btn = form.query_selector('button.submit-button')
    if not submit_btn:
        logger.error(f"No submit button found in form for problem {problem['id']}")
        return False
    input_field.fill(flag)
    submit_btn.click()
    logger.info(f"Submitted flag for {problem['title']}: {flag}")
    dialog_message = {'text': None}
    def handle_dialog(dialog):
        dialog_message['text'] = dialog.message
        dialog.dismiss()
    page.once('dialog', handle_dialog)
    page.wait_for_timeout(2000)
    form_id = f"form{problem['id'].split('-')[-1]}"
    form_group = page.query_selector(f"div.form-group#{form_id}")
    alert = None
    feedback_text = None
    if form_group:
        alert = form_group.query_selector('div.alert, .alert-success, .alert-danger')
        if not alert:
            next_sibling = form_group.evaluate_handle('el => el.nextElementSibling')
            if next_sibling:
                alert = next_sibling.query_selector('div.alert, .alert-success, .alert-danger')
    if alert:
        feedback_text = alert.inner_text().strip()
    if not feedback_text:
        notif_modals = page.query_selector_all('.ui-pnotify')
        for notif in notif_modals:
            style = notif.get_attribute('style')
            if style and 'display: none' in style:
                continue
            title_el = notif.query_selector('.ui-pnotify-title')
            text_el = notif.query_selector('.ui-pnotify-text')
            title = title_el.inner_text().strip() if title_el else ''
            text = text_el.inner_text().strip() if text_el else ''
            modal_text = f"{title} {text}".strip()
            print(f"[DEBUG] PNotify modal: {modal_text}")
            if modal_text:
                feedback_text = modal_text
                break
    if not feedback_text:
        modals = page.query_selector_all('.modal.show, .modal-dialog, .swal2-popup, .bootbox, .modal-content')
        for modal in modals:
            modal_text = modal.inner_text().strip()
            print(f"[DEBUG] Modal text: {modal_text}")
            if 'oops' in modal_text.lower() or 'already tried' in modal_text.lower():
                feedback_text = modal_text
                break
    if not feedback_text and dialog_message['text']:
        feedback_text = dialog_message['text']
        print(f"[DEBUG] JS alert: {feedback_text}")
    if feedback_text:
        print(f"[FEEDBACK] Submission result for '{problem['title']}': {feedback_text}")
        if 'correct' in feedback_text.lower() or 'success' in feedback_text.lower():
            logger.info(f"Flag submission for {problem['title']} succeeded!")
            return True
        elif 'incorrect' in feedback_text.lower() or 'wrong' in feedback_text.lower() or 'oops' in feedback_text.lower() or 'already tried' in feedback_text.lower():
            logger.warning(f"Flag submission for {problem['title']} was incorrect or already tried. Message: {feedback_text}")
            return False
        else:
            logger.warning(f"Flag submission for {problem['title']} got an unknown response: {feedback_text}")
            return False
    pink_selectors = [
        'p[style*="background-color: pink"]',
        'div[style*="background-color: pink"]',
        'span[style*="background-color: pink"]'
    ]
    pink_feedback = None
    for selector in pink_selectors:
        elements = page.query_selector_all(selector)
        for el in elements:
            try:
                text = el.inner_text().strip()
                if text:
                    pink_feedback = text
                    break
            except Exception:
                continue
        if pink_feedback:
            break
    if pink_feedback:
        print(f"[FEEDBACK] Submission result for '{problem['title']}' (pink): {pink_feedback}")
        if 'correct' in pink_feedback.lower() or 'success' in pink_feedback.lower():
            logger.info(f"Flag submission for {problem['title']} succeeded!")
            return True
        elif 'incorrect' in pink_feedback.lower() or 'wrong' in pink_feedback.lower() or 'oops' in pink_feedback.lower() or 'already tried' in pink_feedback.lower():
            logger.warning(f"Flag submission for {problem['title']} was incorrect or already tried. Message: {pink_feedback}")
            return False
        else:
            logger.warning(f"Flag submission for {problem['title']} got an unknown response: {pink_feedback}")
            return False
    logger.warning(f"No feedback detected for {problem['title']} after submission.")
    return False
    # Completely rewritten to avoid any hidden/corrupted characters or indentation issues
    prob_num = problem['id'].split('-')[-1]
    form = None
    input_field = None
    submit_btn = None
    # Try to find input by id first
    input_by_id = page.query_selector(f"input#inp{prob_num}.form-control")
    if input_by_id:
        input_field = input_by_id
        form = input_field.evaluate_handle('el => el.closest("form")')
    else:
        input_field = page.query_selector('input.form-control')
        if input_field:
            form = input_field.evaluate_handle('el => el.closest("form")')
    if not input_field or not form:
        logger.error(f"No input field or form found for problem {problem['id']}")
        return False
    submit_btn = form.query_selector('button.submit-button')
    if not submit_btn:
        logger.error(f"No submit button found in form for problem {problem['id']}")
    input_field.fill(flag)
    submit_btn.click()
    logger.info(f"Submitted flag for {problem['title']}: {flag}")
    dialog_message = {'text': None}
    def handle_dialog(dialog):
        dialog_message['text'] = dialog.message
        dialog.dismiss()
    page.once('dialog', handle_dialog)
    page.wait_for_timeout(2000)
    form_id = f"form{problem['id'].split('-')[-1]}"
    form_group = page.query_selector(f"div.form-group#{form_id}")
    alert = None
    feedback_text = None
    if form_group:
        alert = form_group.query_selector('div.alert, .alert-success, .alert-danger')
        if not alert:
            next_sibling = form_group.evaluate_handle('el => el.nextElementSibling')
            if next_sibling:
                alert = next_sibling.query_selector('div.alert, .alert-success, .alert-danger')
    if alert:
        feedback_text = alert.inner_text().strip()
    if not feedback_text:
        notif_modals = page.query_selector_all('.ui-pnotify')
        for notif in notif_modals:
            style = notif.get_attribute('style')
            if style and 'display: none' in style:
                continue
            title_el = notif.query_selector('.ui-pnotify-title')
            text_el = notif.query_selector('.ui-pnotify-text')
            title = title_el.inner_text().strip() if title_el else ''
            text = text_el.inner_text().strip() if text_el else ''
            modal_text = f"{title} {text}".strip()
            print(f"[DEBUG] PNotify modal: {modal_text}")
            if modal_text:
                feedback_text = modal_text
                break
    if not feedback_text:
        modals = page.query_selector_all('.modal.show, .modal-dialog, .swal2-popup, .bootbox, .modal-content')
        for modal in modals:
            modal_text = modal.inner_text().strip()
            print(f"[DEBUG] Modal text: {modal_text}")
            if 'oops' in modal_text.lower() or 'already tried' in modal_text.lower():
                feedback_text = modal_text
                break
    if not feedback_text and dialog_message['text']:
        feedback_text = dialog_message['text']
        print(f"[DEBUG] JS alert: {feedback_text}")
    if feedback_text:
        print(f"[FEEDBACK] Submission result for '{problem['title']}': {feedback_text}")
        if 'correct' in feedback_text.lower() or 'success' in feedback_text.lower():
            logger.info(f"Flag submission for {problem['title']} succeeded!")
            return True
        elif 'incorrect' in feedback_text.lower() or 'wrong' in feedback_text.lower() or 'oops' in feedback_text.lower() or 'already tried' in feedback_text.lower():
            logger.warning(f"Flag submission for {problem['title']} was incorrect or already tried. Message: {feedback_text}")
            return False
        else:
            logger.warning(f"Flag submission for {problem['title']} got an unknown response: {feedback_text}")
            return False
    pink_selectors = [
        'p[style*="background-color: pink"]',
        'div[style*="background-color: pink"]',
        'span[style*="background-color: pink"]'
    ]
    pink_feedback = None
    for selector in pink_selectors:
        elements = page.query_selector_all(selector)
        for el in elements:
            try:
                text = el.inner_text().strip()
                if text:
                    pink_feedback = text
                    break
            except Exception:
                continue
        if pink_feedback:
            break
    if pink_feedback:
        print(f"[FEEDBACK] Submission result for '{problem['title']}' (pink): {pink_feedback}")
        if 'correct' in pink_feedback.lower() or 'success' in pink_feedback.lower():
            logger.info(f"Flag submission for {problem['title']} succeeded!")
            return True
        elif 'incorrect' in pink_feedback.lower() or 'wrong' in pink_feedback.lower() or 'oops' in pink_feedback.lower() or 'already tried' in pink_feedback.lower():
            logger.warning(f"Flag submission for {problem['title']} was incorrect or already tried. Message: {pink_feedback}")
            return False
        else:
            logger.warning(f"Flag submission for {problem['title']} got an unknown response: {pink_feedback}")
            return False
    debug_dir = os.path.join(os.path.dirname(__file__), '../../data/metactf/debug')
    os.makedirs(debug_dir, exist_ok=True)
    import datetime
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(debug_dir, f'submit_{problem["id"]}_{ts}.png')
    html_path = os.path.join(debug_dir, f'submit_{problem["id"]}_{ts}.html')
    try:
        page.screenshot(path=screenshot_path, full_page=True)
        logger.warning(f"[DEBUG] Screenshot saved: {screenshot_path}")
    except Exception as e:
        logger.error(f"[DEBUG] Failed to save screenshot: {e}")
    logger.warning(f"No feedback detected for {problem['title']} after submission.")
    return False


# === MAIN WORKFLOW ===
if __name__ == "__main__":
    config = Config()
    try:
        playwright, browser, context, page = metactf_login(config)
    except LoginError as e:
        logger.error(f"Login failed: {e}")
        sys.exit(1)
    save_dir = get_save_dir()
    problems = scrape_problems(page, save_dir)
    results = solve_all_problems(problems)
    for result in results:
        flag = result['flag']
        if flag:
            # Find the full problem dict for submit_flag
            problem = next((p for p in problems if p['id'] == result['id']), None)
            if problem:
                submit_flag(page, problem, flag)
            else:
                logger.warning(f"Problem not found for id {result['id']}")
        else:
            logger.warning(f"No flag found for {result['title']}")
    logger.info("Done.")
