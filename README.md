# Canvas Tool Checker


This script scans Canvas LMS courses in specified terms to see if a given external tool is enabled in the course navigation. It outputs a CSV report of matching courses.

## Setup

1. Ensure the Python version specified in `.python-version` is available. (Using [pyenv](https://github.com/pyenv/pyenv) to manage your Python installations is highly recommended.)

2. Create a virtual environment and activate it:
   ```shell
   python -m venv venv
   source ./venv/bin/activate
   ```

3. Install the required packages:
   ```shell
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in your Canvas API credentials:
   ```shell
   cp .env.example .env
   # Edit .env and set your values
   ```

## Usage

Run the script with required arguments:

```shell
python main.py --tool-id context_external_tool_36409 --term-ids 2024-30,2024-40,2025-20 --output output/enabled_courses.csv
```

- `--tool-id` (required): The Canvas external tool tab ID to check (e.g., `context_external_tool_36409`).
- `--term-ids` (required): Comma-separated list of SIS term IDs to scan (e.g., `2024-30,2024-40,2025-20`).
- `--output` (optional): Output CSV file path (default: `output/enabled_courses.csv`).

### Example

To scan for the tool ID 36409 in three terms:

```shell
python main.py --tool-id context_external_tool_36409 --term-ids 2024-30,2024-40,2025-20
```

The results will be written to `output/enabled_courses.csv` by default.

## Environment Variables

Set the following variables in your `.env` file or OS environment:

- `CANVAS_ACCESS_TOKEN` (required): Your Canvas API access token
- `CANVAS_PROD_HOSTNAME` (required): Canvas hostname (e.g., `canvas.institution.edu`)
- `CANVAS_ROOT_ACCOUNT_ID` (required): Canvas root account ID (usually `1`)

See `.env.example` for a template.

