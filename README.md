# job-scraper

A Python script that monitors IT job offers via the Adzuna API and alerts you when new ones appear.

## How it works

1. Fetches job offers from the Adzuna API (Germany)
2. Compares results with offers already stored in a local SQLite database
3. Displays only the **new** offers since the last run
4. Saves the new offers to the database

## Setup

```bash
pip install requests python-dotenv
```

Create a `.env` file at the root of the project:

```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

Get your free API credentials at: https://developer.adzuna.com

## Usage

```bash
python main.py
```

Run it once a day to get notified of new offers.

## Project structure

```
job-scraper/
├── main.py       # entry point — orchestrates everything
├── scraper.py    # calls the Adzuna API and parses results
├── database.py   # SQLite read/write logic
├── .env          # your API keys (never commit this)
├── .gitignore    # ignores .env and jobs.db
└── jobs.db       # created automatically on first run
```

## Tech stack

- `requests` — HTTP requests to the Adzuna API
- `python-dotenv` — loads API keys from the `.env` file
- `sqlite3` — local database (built into Python, no install needed)
