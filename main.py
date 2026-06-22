import argparse
import csv
from datetime import datetime
from database import init_db, get_known_urls, save_jobs
from scraper import fetch_jobs


def parse_args():
    parser = argparse.ArgumentParser(
        description="Track new job offers via the Adzuna API."
    )
    parser.add_argument(
        "--keywords", "-k",
        type=str,
        default="python developer",
        help="Keywords to search for (default: 'python developer')"
    )
    parser.add_argument(
        "--results", "-r",
        type=int,
        default=20,
        help="Number of results to fetch (default: 20)"
    )
    parser.add_argument(
        "--export", "-e",
        action="store_true",
        help="Export new offers to a CSV file"
    )
    return parser.parse_args()


def export_to_csv(jobs: list[dict]):
    """Export a list of jobs to a timestamped CSV file."""
    if not jobs:
        return

    filename = f"new_jobs_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "url"])
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Exported to {filename}")


def main():
    args = parse_args()

    # 1. Make sure the database and table exist
    init_db()

    # 2. Fetch current offers from Adzuna API
    print(f"Fetching jobs for: '{args.keywords}'...")
    try:
        all_jobs = fetch_jobs(keywords=args.keywords, results_per_page=args.results)
    except (EnvironmentError, ConnectionError, TimeoutError, RuntimeError) as e:
        print(f"Error: {e}")
        return

    print(f"Found {len(all_jobs)} offers.")

    # 3. Keep only the ones we haven't seen before
    known_urls = get_known_urls()
    new_jobs = [job for job in all_jobs if job["url"] not in known_urls]

    # 4. Display new offers
    if not new_jobs:
        print("No new offers since last run.")
    else:
        print(f"\n{len(new_jobs)} NEW offer(s):\n")
        for job in new_jobs:
            print(f"  [{job['company']}] {job['title']}")
            print(f"  {job['location']}")
            print(f"  {job['url']}")
            print()

    # 5. Save new jobs to the database
    save_jobs(new_jobs)
    print(f"Saved {len(new_jobs)} new offer(s) to the database.")

    # 6. Optionally export to CSV
    if args.export:
        export_to_csv(new_jobs)


if __name__ == "__main__":
    main()