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
To run the MetaCTF bot and Copilot watcher with merged output directly from chat, use:
```powershell
.venv\Scripts\python.exe src/cli/chat_control.py
```

- This will start both the bot and the Copilot watcher, merging their output in real time.
- All [COPILOT] and watcher events will be visible in the chat/terminal.
- Debug artifacts (screenshots, HTML) and all scraped files are saved in the `data/` folder (which is gitignored by default).

### CLI Tools
Use the consolidated CLI tools in `src/cli/` for targeted operations and debugging.

- **Run heuristics on MCP for a problem:**
```powershell
.venv\Scripts\python.exe -m src.cli.mcp_heuristics --problem-id problem-05 --paths /tmp/metactf/problem-05
```

- **Check submission history for a problem:**
```powershell
.venv\Scripts\python.exe -m src.cli.submission_manager check --problem-id problem-05
```

- **Submit a flag for a problem:**
```powershell
.venv\Scripts\python.exe -m src.cli.submission_manager submit --problem-id problem-05 --flag "MetaCTF{example_flag}"
```

- **Run the autosolver orchestrator (runs heuristics and attempts solves):**
```powershell
.venv\Scripts\python.exe -m src.cli.autosolver --problem-id problem-05 --run-heuristics
```

- **Archived one-off scripts:** original per-problem scripts were moved to `src/cli/archived/` for reference.
- **Analysis outputs:** MCP analysis, heuristics results, and other debug artifacts are written to `data/copilot_context/`.

## Notes
- All configuration is via `.env`.
- The bot is fully autonomous; no CLI interaction is required.
- For debugging, set Playwright to non-headless mode in `login.py` if needed.
- All logs are written to the console and `automation.log` (if configured).

## Network Fetch Policy
- **Paused by default:** Automated fetching of external problem-linked URLs (HTTP/HTTPS) is paused to avoid unsolicited network requests.
- **User control:** Fetching can be resumed only with an explicit user approval or command; no external downloads or remote fetches will be performed automatically.
- **Local-first analysis:** The bot will continue to analyze any files already downloaded into `data/` without performing new network requests.
## Troubleshooting
- If you see `IndentationError` or similar, ensure your files use only spaces for indentation.
- If Playwright is not installed, run `pip install playwright` and `python -m playwright install` in your venv.
- If login fails, check your `.env` credentials and environment name.

## License
MIT
