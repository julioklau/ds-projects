import json
from pathlib import Path
from typing import Dict, List

RAW_FOLDER = "01_raw"

def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]

def get_script_path() -> Path:
    return Path(__file__).resolve().parents[1]

def get_columns_to_saved(source: str) -> Dict:
    return load_json(get_script_path()/"config"/"saved_columns.json").get(source, {})

def save_to_jsonl(data: list[Dict], filename: str, folder: Path = get_project_root()/"data"/RAW_FOLDER) -> None:
    """
    Save a list of dictionaries to a JSON Lines (.jsonl) file.

    Args:
        data (list[Dict]): List of dictionaries to save.
        filename (str): Name of the file to create (e.g., "news.jsonl").
        folder (str, optional): Folder path to save the file. Defaults to "data/raw".
    """
    Path(folder).mkdir(parents = True, exist_ok = True)
    path = Path(folder) / filename
    with open(path, "w", encoding = "utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii = False) + "\n")

def load_jsonl(filepath: str) -> List[Dict]:
    """
    Load data from a JSON Lines (.jsonl) file into a list of dictionaries.

    Args:
        filepath (str): Path to the .jsonl file.

    Returns:
        List[Dict]: List of dictionaries read from the file.
    """
    with open(filepath, "r", encoding = "utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def load_json(path: Path):
    with open(path, "r", encoding = "utf-8") as f:
        return json.load(f)