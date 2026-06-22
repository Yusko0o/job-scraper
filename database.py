import sqlite3

DB_NAME = "jobs.db"


def init_db():
    """Create the jobs table if it doesn't exist yet."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            title    TEXT NOT NULL,
            company  TEXT,
            location TEXT,
            url      TEXT UNIQUE NOT NULL,
            seen_at  TEXT DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


def get_known_urls():
    """Return a set of all URLs already stored in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT url FROM jobs")
    urls = {row[0] for row in cursor.fetchall()}

    conn.close()
    return urls


def save_jobs(jobs: list[dict]):
    """
    Insert new jobs into the database.
    'jobs' is a list of dicts with keys: title, company, location, url
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for job in jobs:
        cursor.execute("""
            INSERT OR IGNORE INTO jobs (title, company, location, url)
            VALUES (:title, :company, :location, :url)
        """, job)

    conn.commit()
    conn.close()
