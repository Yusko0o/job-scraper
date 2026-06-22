import os
import sqlite3
import unittest
import database

database.DB_NAME = "test_jobs.db"


class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Called before each test — start with a fresh database."""
        database.init_db()

    def tearDown(self):
        """Called after each test — delete the test database."""
        os.remove(database.DB_NAME)

    def test_init_creates_table(self):
        """init_db() should create the jobs table."""
        conn = sqlite3.connect(database.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result)

    def test_empty_db_returns_no_urls(self):
        """A fresh database should return an empty set."""
        urls = database.get_known_urls()
        self.assertEqual(urls, set())

    def test_save_and_retrieve_jobs(self):
        """Saved jobs should appear in get_known_urls()."""
        jobs = [
            {"title": "Python Dev", "company": "Acme", "location": "Berlin", "url": "https://example.com/1"},
            {"title": "Flask Dev",  "company": "Corp", "location": "Munich", "url": "https://example.com/2"},
        ]
        database.save_jobs(jobs)

        urls = database.get_known_urls()
        self.assertIn("https://example.com/1", urls)
        self.assertIn("https://example.com/2", urls)

    def test_duplicate_url_is_ignored(self):
        """Saving the same URL twice should not create duplicates."""
        job = [{"title": "Python Dev", "company": "Acme", "location": "Berlin", "url": "https://example.com/1"}]

        database.save_jobs(job)
        database.save_jobs(job)  

        conn = sqlite3.connect(database.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE url = 'https://example.com/1'")
        count = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()