# Research: MetaCTF Bot Solver

## Local Storage for Scraped Problems
- Use a dedicated `data/` or `scraped/` directory at the project root.
- Organize by source and date: e.g., `data/metactf/2025-12-13/problem-001.json`.
- Use descriptive, unique, and consistent file names (no spaces or special chars).
- Store structured data as JSON; raw HTML as `.html`; files in subfolders.
- Secure: never store credentials in scraped data; restrict permissions; sanitize filenames.
- For large scale, consider SQLite or cloud storage (not needed for MVP).

## Playwright Login & Scraping (Python)
- Use Playwright's async API for performance.
- Prefer stable selectors (data-testid, aria-label) for login.
- Wait for navigation/network idle after login.
- Use `page.content()` for HTML, `page.on('download')` for files.
- Save HTML and files to disk with sanitized names.
- Use context managers and try/except for cleanup and error handling.
- Store credentials in `.env`, never in code.

## Flag Extraction (MetaCTF{flag})
- Use regex: `r"MetaCTF\{[^\}]+\}"` (case-insensitive if needed).
- Scan `.txt`, `.md`, `.py`, `.html`, etc. Use BeautifulSoup for HTML.
- Use `os.walk()` or `pathlib.Path.rglob()` for recursive scanning.
- Log errors and skipped files; handle encoding issues.
- For binary files, decode with fallback or skip unless needed.

## Error Handling & Logging
- Use `try/except` for all file and browser operations.
- Catch specific exceptions; use `finally` for cleanup.
- Use Python's `logging` module (or loguru for simplicity).
- Log to both file and console; use log levels (info, warning, error).
- Log browser actions, navigation, file saves, and errors.
- Never use bare `except:`; always log or re-raise.

## Decisions & Rationale
- **Local storage**: Flat files in `data/metactf/<date>/` for MVP; simple, portable, and easy to debug.
- **Playwright**: Best for dynamic sites; async API for future concurrency.
- **Regex + BeautifulSoup**: Fast, reliable for flag extraction; extensible for more formats.
- **Logging**: Standard library for MVP; can switch to loguru if needed.

## Alternatives Considered
- Database storage (overkill for MVP)
- Headless operation (not default; only if directed)
- Other scraping tools (requests/bs4 not suitable for JS-heavy sites)
- Advanced flag extraction (YARA, OCR) not needed for MVP
