---

description: "Task list for MetaCTF Bot Solver feature implementation"
---

# Tasks: MetaCTF Bot Solver

**Input**: Design documents from `/specs/001-metactf-bot-solver/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python 3.14 project in a virtual environment (venv)
- [ ] T003 [P] Install Playwright and configure for browser automation in requirements.txt
- [ ] T004 [P] Configure linting and formatting tools (e.g., black, flake8) in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T005 Ensure no direct work is performed on main branch (enforce via branch protection or pre-commit hook)
- [ ] T006 Commit frequently with descriptive messages (document in CONTRIBUTING.md)
- [ ] T007 Ensure all browser automation uses Playwright (no headless chromedriver unless directed)
- [ ] T008 [P] Create base models/entities (Credentials, Problem, Flag) in src/models/
- [ ] T009 [P] Setup environment configuration management (read .env) in src/lib/config.py
- [ ] T010 Configure error handling and logging infrastructure in src/lib/logging.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Automated Login and Problem Scraping (Priority: P1) 🎯 MVP

**Goal**: Log in to MetaCTF, select the correct environment, and scrape all active problems (with links and files) to local storage.

**Independent Test**: Run the bot and verify that all active problems and their resources are saved locally for the selected environment.

### Implementation for User Story 1

- [ ] T011 [P] [US1] Implement MetaCTF login and environment selection in src/services/login.py
- [ ] T012 [P] [US1] Implement problem list scraping in src/services/scraper.py
- [ ] T013 [P] [US1] Implement file and link download logic in src/services/scraper.py
- [ ] T014 [US1] Save scraped problems and files to data/metactf/<date>/ in src/services/scraper.py
- [ ] T015 [US1] Add validation and error handling for login/scraping in src/services/login.py and src/services/scraper.py
- [ ] T016 [US1] Add logging for all operations in src/lib/logging.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Automated Problem Solving and Flag Submission (Priority: P2)

**Goal**: Analyze saved problems, extract MetaCTF{flag} values, and submit them to MetaCTF.

**Independent Test**: Run the bot on a set of known problems and verify that correct flags are found and submitted.

### Implementation for User Story 2

- [ ] T017 [P] [US2] Implement recursive file and HTML scanning for MetaCTF{flag} in src/services/solver.py
- [ ] T018 [P] [US2] Implement flag submission logic in src/services/submitter.py
- [ ] T019 [US2] Add error handling for unsolved or already-solved problems in src/services/solver.py
- [ ] T020 [US2] Add logging for flag extraction and submission in src/lib/logging.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Robust Error Handling and Logging (Priority: P3)

**Goal**: Provide clear logging and error handling throughout the process, including failed logins, missing files, or submission errors.

**Independent Test**: Simulate errors (e.g., wrong credentials, network issues) and verify that logs are clear and actionable.

### Implementation for User Story 3

- [ ] T021 [P] [US3] Add comprehensive try/except blocks and error messages in all services
- [ ] T022 [P] [US3] Add log messages for all major actions and errors in src/lib/logging.py
- [ ] T023 [US3] Add tests for error scenarios in tests/integration/test_errors.py

**Checkpoint**: At this point, all user stories are independently testable and robust

---

## Final Phase: Polish & Cross-Cutting Concerns

- [ ] T024 [P] Add CLI entrypoint and argument parsing in src/cli/run.py
- [ ] T025 [P] Add README and update quickstart.md
- [ ] T026 [P] Add contract and integration tests for all major flows in tests/contract/ and tests/integration/
- [ ] T027 [P] Review and refactor code for simplicity and clarity
- [ ] T028 [P] Final code lint/format pass

---

## Dependencies

- User Story 1 (P1) must be completed before User Story 2 (P2)
- User Story 2 (P2) must be completed before User Story 3 (P3)
- Setup and Foundational phases must be completed before any user story work

## Parallel Execution Examples

- T003, T004, T008, T009 can be done in parallel after T002
- T011, T012, T013 can be done in parallel after foundational tasks
- T017, T018 can be done in parallel after User Story 1
- T021, T022 can be done in parallel after User Story 2

## Implementation Strategy

- MVP: Complete all tasks for User Story 1 (Phase 3)
- Incremental delivery: Complete each user story phase independently, with tests and validation at each checkpoint
- Polish and cross-cutting tasks only after all user stories are independently testable
