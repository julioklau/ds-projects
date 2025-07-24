import json
from pathlib import Path
import requests
import time
from typing import Optional, Dict, Any, List

def save_to_jsonl(data: list[Dict], filename: str, folder: str = "data/raw") -> None:
    """
    Save a list of dictionaries to a JSON Lines (.jsonl) file.

    Args:
        data (list[Dict]): List of dictionaries to save.
        filename (str): Name of the file to create (e.g., "news.jsonl").
        folder (str, optional): Folder path to save the file. Defaults to "data/raw".
    """
    Path(folder).mkdir(parents = True, exist_ok = True)
    path = Path(folder) / filename
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def load_jsonl(filepath: str) -> List[Dict]:
    """
    Load data from a JSON Lines (.jsonl) file into a list of dictionaries.

    Args:
        filepath (str): Path to the .jsonl file.

    Returns:
        List[Dict]: List of dictionaries read from the file.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def merge_jsonl_files(input_folder: str = "data/raw", output_file: str = "data/processed/merged.jsonl") -> None:
    """
    Merge all .jsonl files in a folder into a single JSON Lines file.

    Args:
        input_folder (str, optional): Directory containing input .jsonl files. Defaults to "data/raw".
        output_file (str, optional): Path to save the merged .jsonl file. Defaults to "data/processed/merged.jsonl".
    """
    Path(Path(output_file).parent).mkdir(parents=True, exist_ok=True)
    all_data = []
    for path in Path(input_folder).glob("*.jsonl"):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    all_data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    save_to_jsonl(all_data, Path(output_file).name, Path(output_file).parent)

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
            response = requests.get(api_url, params = params, headers = headers, timeout = 10)
            if response.status_code == 429:
                print("[WARN] Rate limit hit. Sleeping for", rate_limit_sleep, "seconds.")
                time.sleep(rate_limit_sleep)
                continue
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Attempt {attempt} failed: {e}")
            if attempt < retries:
                sleep_time = backoff_factor * attempt
                print(f"[INFO] Retrying in {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
            else:
                print("[ERROR] Max retries reached. Giving up.")
        except ValueError:
            print("[ERROR] Failed to decode JSON.")
            return None
        
def load_checkpoint(path: str = "data/api_checkpoint.json") -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_checkpoint(checkpoint: dict, path: str = "data/api_checkpoint.json") -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii = False, indent = 2)