# 🔍 Job Scraper

A Python CLI tool that monitors job offers via the Adzuna API and alerts you when new ones appear.

---

## 🛠️ Built With

| Technology | Usage |
|------------|-------|
| [Python] | Core language |
| [Adzuna API] | Job offers data source |
| [SQLite] | Local storage & duplicate detection |
| [requests] | HTTP calls to the API |
| [python-dotenv] | Secure API key management |

---

## 📁 Project Structure

```
job-scraper/
├── main.py           # Entry point — CLI args, orchestration, CSV export
├── scraper.py        # Adzuna API calls & error handling
├── database.py       # SQLite read/write logic
├── test_database.py  # Unit tests (4 tests)
├── .env              # Your API keys (never committed)
├── .gitignore        # Ignores .env and jobs.db
└── jobs.db           # Created automatically on first run
```

---

## ✨ Features

- 🔎 Fetch job offers by keyword via the Adzuna API
- 🆕 Detect and display only **new offers** since last run
- 💾 Store seen offers in a local SQLite database
- 📄 Export new offers to a timestamped CSV file
- 🛡️ Proper error handling (no internet, API down, missing keys)
- 🧪 Unit tested with `unittest`

---

## ⚙️ Run Locally

### Clone the repository

```bash
git clone https://github.com/Yusko0o/job-scraper.git
cd job-scraper
```

### Install dependencies

```bash
pip install requests python-dotenv
```

### Set up your API keys

Create a `.env` file at the root of the project:

```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

Get your free credentials at: https://developer.adzuna.com

### Run

```bash
# Default search (python developer)
python main.py

# Custom keywords
python main.py --keywords "flask backend"

# With CSV export
python main.py -k "junior developer" --export
```

### Run tests

```bash
python -m unittest test_database.py -v
```

---

## 👤 Author

**Yusko0o**
- GitHub: [@Yusko0o](https://github.com/Yusko0o)

---

*Made with ❤️ and a lot of coffee ☕*  
*No vibe coding ❤️*
