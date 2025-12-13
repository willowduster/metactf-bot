# Quickstart: MetaCTF Bot Solver

## Prerequisites
- Python 3.14 installed
- Windows PowerShell 5.1
- [Optional] Node.js (for Playwright install)

## Setup
1. Clone the repository and checkout the feature branch:
   ```powershell
   git clone <repo-url>
   cd metactf-bot
   git checkout 001-metactf-bot-solver
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   playwright install
   ```
4. Copy and edit `.env` with your MetaCTF credentials and target environment.

## Running the Bot
```powershell
python -m src.cli.run
```

- The bot will log in, scrape problems, and attempt to solve and submit flags.
- Scraped data and files are saved under `data/metactf/<date>/`.
- Logs are written to `automation.log` and the console.

## Notes
- Do not run Chromedriver headless unless explicitly directed.
- Commit frequently with descriptive messages; never work directly on main.
- For debugging, set Playwright to non-headless mode.
