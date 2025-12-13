# Data Model: MetaCTF Bot Solver

## Entities

### Credentials
- username: str
- password: str
- target_env: str

### Problem
- id: str
- title: str
- description: str
- links: list[str]
- files: list[str] (paths to downloaded files)
- solution_field_selector: str
- url: str

### Flag
- value: str
- source_file: str (optional)
- found_at: str (file, html, etc)

## Relationships
- Each Problem may have multiple links and files.
- Each Flag is associated with a Problem and may reference a source file or HTML.

## Validation Rules
- Credentials must be loaded from .env and not empty.
- Problem id/title/url must be non-empty.
- Flag value must match regex: `MetaCTF\{[^\}]+\}`

## State Transitions
- Problem: scraped → analyzed → solved/unsolved
- Flag: found → submitted (success/failure)

## Notes
- All fields are required unless marked optional.
- Extend Problem/Flag as needed for new CTF formats.
