import re
import os

from lib.logging import logger

def extract_flag_from_text(text):
    match = re.search(r"MetaCTF\{.*?\}", text)
    return match.group(0) if match else None

def extract_flag_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return extract_flag_from_text(content)
    except Exception as e:
        logger.error(f"Failed to extract flag from {file_path}: {e}")
        return None

def solve_problem(problem):
    # Try description first
    flag = extract_flag_from_text(problem.get('description', ''))
    if flag:
        return flag, 'description'
    # Try all files
    for file_path in problem.get('files', []):
        flag = extract_flag_from_file(file_path)
        if flag:
            return flag, file_path
    return None, None

def solve_all_problems(problems):
    results = []
    for problem in problems:
        flag, source = solve_problem(problem)
        results.append({'id': problem['id'], 'title': problem['title'], 'flag': flag, 'source': source})
    return results
