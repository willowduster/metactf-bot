
# Feature Specification: MetaCTF Bot Solver

**Feature Branch**: `001-metactf-bot-solver`  
**Created**: 2025-12-13  
**Status**: Draft  
**Input**: User description: "Build a bot to scrape and solve problems from MetaCTF.com. The bot should use credentials and target env from .env, launch a Chrome-based browser, log in, select the target 'Compete!' button for the active TARGET_CTF_ENV, save all active problems (with links and files) locally, iterate through each problem, analyze files and links to solve, find the MetaCTF{flag}, and input them into the solution field."

## User Scenarios & Testing *(mandatory)*


### User Story 1 - Interactive Login and Problem Selection (Priority: P1)

A user runs the bot, which logs into MetaCTF.com using credentials from the .env file, selects the correct CTF environment, and retrieves a list of unsolved problems. The bot displays the list in the terminal and prompts the user to select which problem to scrape and solve. Only the selected problem is scraped, analyzed, and attempted.

**Why this priority**: This is the foundation for all further automation; without reliable login and interactive selection, no other automation is possible.

**Independent Test**: Can be fully tested by running the bot, verifying that the list of unsolved problems is shown, and that only the selected problem is scraped and solved.

**Acceptance Scenarios**:

1. **Given** valid credentials and a target environment in .env, **When** the bot is run, **Then** it logs in, selects the correct environment, lists unsolved problems, and prompts the user for selection.
2. **Given** a user selection, **When** the user chooses a problem, **Then** the bot scrapes, analyzes, and attempts to solve only that problem.
3. **Given** invalid credentials, **When** the bot is run, **Then** it fails gracefully and reports the error.

---


### User Story 2 - Interactive Problem Solving and Flag Submission (Priority: P2)

After the user selects a problem, the bot scrapes the problem, analyzes its files and links, attempts to solve the problem by searching for MetaCTF{flag} patterns, and submits the flag in the solution field on MetaCTF.com. The process repeats or exits as desired by the user.

**Why this priority**: Automating the solve-and-submit loop for a user-selected problem is the core value proposition of the bot.

**Independent Test**: Can be fully tested by running the bot, selecting a problem, and verifying that the correct flag is found and submitted for that problem only.

**Acceptance Scenarios**:

1. **Given** a list of unsolved problems, **When** the user selects a problem, **Then** the bot scrapes, analyzes, and attempts to solve and submit the flag for only that problem.
2. **Given** a problem with no flag present, **When** the bot analyzes it, **Then** it skips or reports the problem as unsolved.

---

### User Story 3 - Robust Error Handling and Logging (Priority: P3)

The bot provides clear logging and error handling throughout the process, including failed logins, missing files, or submission errors.

**Why this priority**: Good error handling and logging are essential for debugging and reliability.

**Independent Test**: Can be fully tested by simulating errors (e.g., wrong credentials, network issues) and verifying that logs are clear and actionable.

**Acceptance Scenarios**:

1. **Given** a network failure, **When** the bot is running, **Then** it logs the error and retries or exits gracefully.
2. **Given** a missing or malformed .env file, **When** the bot is run, **Then** it reports the configuration error clearly.

---

### Edge Cases

- What happens when MetaCTF changes its login flow or page structure?
- How does the system handle rate limiting or CAPTCHAs?
- What if a problem has no downloadable files or links?
- How does the bot behave if the .env file is missing or incomplete?
- What if a flag is already submitted or the submission fails?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST read credentials and target environment from a .env file.
- **FR-002**: System MUST launch a Chrome-based browser (not headless by default) using Playwright.
- **FR-003**: System MUST log into MetaCTF.com and select the correct CTF environment.
- **FR-004**: System MUST scrape all active problems, including links and downloadable files, and save them locally.
- **FR-005**: System MUST iterate through each problem, analyze files and links, and attempt to find MetaCTF{flag} values.
- **FR-006**: System MUST submit found flags to the correct solution fields on MetaCTF.com.
- **FR-007**: System MUST provide clear logging and error handling for all major steps.
- **FR-008**: System MUST NOT run Chromedriver in headless mode unless explicitly directed.
- **FR-009**: System MUST commit code frequently with descriptive messages and never work directly on main branch.

### Key Entities

- **Credentials**: Represents the username, password, and target environment loaded from .env.
- **Problem**: Represents a MetaCTF problem, including title, description, links, downloadable files, and solution field.
- **Flag**: Represents a MetaCTF{flag} value found in problem resources.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of active problems for the selected environment are saved locally with all resources.
- **SC-002**: 90%+ of problems with a MetaCTF{flag} present are solved and submitted automatically.
- **SC-003**: All errors (login, scraping, submission) are logged with actionable messages.
- **SC-004**: No direct commits to main branch; all work is on feature branches with frequent, descriptive commits.

- **SC-005**: The bot completes a full CTF scrape/solve/submit cycle (up to 500 problems) in under 10 minutes on a typical broadband connection.

## Performance and Scale

- The bot should process and submit all problems for a CTF environment (typically 100–200 problems) within 10 minutes, with <1% error rate for scraping/submission.
- Designed for single-user automation, targeting CTFs with up to 500 problems and 1000 file downloads per run.
