import requests
import time
from typing import Optional, Dict, Any

def fetch_news(
    api_url: str,
    params: Dict[str, Any],
    headers: Dict[str, str],
    retries: int = 3,
    backoff_factor: float = 1.0,
    rate_limit_sleep: float = 60.0,
) -> Optional[Dict[str, Any]]:
    """
    Fetch one page of news from API with retry and rate limit handling.

    Args:
        api_url: Full API endpoint URL.
        params: Query parameters for the request.
        headers: Headers for authentication or content-type.
        retries: Number of retry attempts for failed requests.
        backoff_factor: Time to wait between retries (increasing each time).
        rate_limit_sleep: Time to wait (in seconds) if rate limit is hit (HTTP 429).

    Returns:
        Parsed JSON response or None if request failed.
    """
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(api_url, params = params, headers = headers, timeout = 30)
            if response.status_code == 429:
                print("[WARN] Rate limit hit. Sleeping for", rate_limit_sleep, "seconds.")
                time.sleep(rate_limit_sleep)
                continue
            response.raise_for_status()
            return response.json(), response.headers
        except requests.RequestException as e:
            print(f"[ERROR] Attempt {attempt} failed: {e}")
            if attempt < retries:
                sleep_time = backoff_factor * attempt
                print(f"[INFO] Retrying in {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                continue
            else:
                print("[ERROR] Max retries reached. Giving up.")
                return None, None
        except ValueError:
            print("[ERROR] Failed to decode JSON.")
            return None, None