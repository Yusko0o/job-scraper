import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID  = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

API_URL = "https://api.adzuna.com/v1/api/jobs/de/search/1"


def fetch_jobs(keywords: str = "python developer", results_per_page: int = 20) -> list[dict]:
    """
    Fetch job offers from Adzuna API.
    Returns a list of job dicts with keys: title, company, location, url.
    """
    # Check that API keys are present
    if not APP_ID or not APP_KEY:
        raise EnvironmentError(
            "Missing API credentials. Make sure ADZUNA_APP_ID and "
            "ADZUNA_APP_KEY are set in your .env file."
        )

    params = {
        "app_id":           APP_ID,
        "app_key":          APP_KEY,
        "what":             keywords,
        "results_per_page": results_per_page,
        "content-type":     "application/json",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Could not reach the Adzuna API. Check your internet connection.")
    except requests.exceptions.Timeout:
        raise TimeoutError("The Adzuna API took too long to respond. Try again later.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"API error: {e}")

    data = response.json()
    jobs = []

    for result in data.get("results", []):
        title    = result.get("title", "No title")
        company  = result.get("company", {}).get("display_name", "Unknown")
        location = result.get("location", {}).get("display_name", "")
        url      = result.get("redirect_url", "")

        # Skip incomplete results
        if not url:
            continue

        jobs.append({
            "title":    title,
            "company":  company,
            "location": location,
            "url":      url,
        })

    return jobs