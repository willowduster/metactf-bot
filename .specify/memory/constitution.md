
# metactf-bot Constitution


<!--
Sync Impact Report (2025-12-13)
Version change: (template) → 1.0.0
Modified principles: All (template → concrete)
Added sections: None
Removed sections: None
Templates requiring updates:
	✅ plan-template.md (Python 3.14, venv, Playwright, commit/branch rules)
	✅ spec-template.md (no new mandatory sections)
	✅ tasks-template.md (Python 3.14, venv, Playwright, commit/branch rules)
Follow-up TODOs: TODO(RATIFICATION_DATE): Set original ratification date
-->

## Core Principles

### I. Python 3.14 Virtual Environment
All code MUST be written for Python 3.14 and executed within a project-specific virtual environment (venv). No global or system Python usage is permitted. Rationale: Ensures reproducibility and environment isolation.

### II. Simple, Readable Code
All code MUST be simple, clear, and easy to understand. Avoid unnecessary complexity. Rationale: Simplicity reduces bugs and onboarding time.

### III. Frequent, Descriptive Commits
Commits MUST be made frequently, each with a descriptive message summarizing the change. Rationale: Enables traceability and easier code review.

### IV. No Direct Work on Main Branch
All development MUST occur on feature or topic branches. Direct commits or merges to main are strictly prohibited. Rationale: Protects main branch stability and enables code review.

### V. Playwright for Browser Automation
All browser automation MUST use Playwright. Chromedriver or Selenium are not permitted except for legacy migration. Rationale: Playwright provides modern, reliable browser automation.

### VI. No Headless Chromedriver Unless Directed
Chromedriver MUST NOT be run in headless mode unless explicitly directed by project leadership or specification. Rationale: Prevents undetected UI issues and ensures test visibility.


## Additional Constraints

- All Python dependencies MUST be managed via requirements.txt or pyproject.toml.
- All automation scripts MUST be compatible with Windows PowerShell 5.1.
- All code and documentation MUST be in English.

## Development Workflow

- All work MUST begin with a new branch from main.
- Each commit MUST be pushed to a remote branch before opening a pull request.
- Pull requests MUST reference the related feature, bug, or task.
- All code MUST pass automated tests and linting before merge.
- Code reviews are REQUIRED before merging to main.



## Governance

- This constitution supersedes all other workflow or coding practices in the repository.
- Amendments require a pull request, explicit documentation of changes, and a migration plan if breaking.
- All PRs and reviews MUST verify compliance with these principles.
- Constitution version MUST be incremented according to semantic versioning:
	- MAJOR: Backward-incompatible changes or removals.
	- MINOR: New principles or sections, or expanded guidance.
	- PATCH: Clarifications, typo fixes, or non-semantic refinements.
- Compliance reviews MUST be performed at least quarterly.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2025-12-13

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
