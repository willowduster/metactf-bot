# MetaCTF Bot

A fully autonomous MetaCTF competition bot that logs in, scrapes problems, solves, and submits flags using Playwright.

## Features
- Automated login and environment selection
- Problem scraping and file download
- Flag extraction from descriptions and files
- Autonomous flag submission with feedback detection
- Robust error handling and logging
- Virtual environment and Playwright browser automation

## Requirements
- Python 3.14+
- Playwright (`pip install playwright` and `python -m playwright install`)
- `python-dotenv` for environment variable loading
- All dependencies installed in a virtual environment (`.venv`)

## Setup
1. Clone the repository and create a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python -m playwright install
   ```
2. Create a `.env` file in the project root with:
   ```env
   META_CTF_USERNAME=your_email@example.com
   META_CTF_PASSWORD=your_password
   TARGET_CTF_ENV=Practice CTF Environment
   ```


## Usage
Run the bot from the project root:
```powershell
.venv\Scripts\python.exe src/cli/solve_and_submit.py
```
- The bot will log in, scrape all problems, attempt to solve and submit flags, and log results.
- Debug artifacts (screenshots, HTML) and all scraped files are saved in the `data/` folder (which is gitignored by default).

## Notes
- All configuration is via `.env`.
- The bot is fully autonomous; no CLI interaction is required.
- For debugging, set Playwright to non-headless mode in `login.py` if needed.
- All logs are written to the console and `automation.log` (if configured).

## Troubleshooting
- If you see `IndentationError` or similar, ensure your files use only spaces for indentation.
- If Playwright is not installed, run `pip install playwright` and `python -m playwright install` in your venv.
- If login fails, check your `.env` credentials and environment name.

## License
MIT
