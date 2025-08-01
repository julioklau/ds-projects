import json
from pathlib import Path
from typing import Optional, Any, Dict
from utils.data_io import get_script_path

PATH = get_script_path()/"config"/"api_checkpoint.json"

class CheckpointManager:
    def __init__(self, path: Path = PATH):
        self.path = path
        self.data = self._load()

    def _load(self):
        if self.path.exists():
            with open(self.path, "r", encoding = "utf-8") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.path, "w", encoding = "utf-8") as f:
            json.dump(self.data, f, indent = 4)

    def _ensure_source(self, source: str):
        if source not in self.data:
            self.data[source] = {
                "current_category": None,
                "status": {},
                "finished_category": []
            }

    def get_categories(self, source: str) -> list:
        return list(self.data.get(source, {}).get("status", {}).keys())

    def get_status(self, source: str, category: str) -> Optional[dict]:
        return self.data.get(source, {}).get("status", {}).get(category)

    def set_status(self, source: str, category: str, status: Dict[str, Any]):
        self._ensure_source(source)
        self.data[source]["status"][category] = status
        self.save()

    def get_current_page(self, source: str, category: str) -> Optional[int]:
        status = self.get_status(source, category)
        return status.get("current_page") if status else None

    def set_current_page(self, source: str, category: str, page: int):
        if self.get_status(source, category):
            self.data[source]["status"][category]["current_page"] = page
            self.save()

    def get_date(self, source: str, category: str) -> Optional[str]:
        status = self.get_status(source, category)
        return status.get("date") if status else None

    def set_date(self, source: str, category: str, date: str):
        if self.get_status(source, category):
            self.data[source]["status"][category]["date"] = date
            self.save()

    def get_current_amount(self, source: str, category: str) -> Optional[str]:
        status = self.get_status(source, category)
        return status.get("current_amount") if status else None

    def set_current_amount(self, source: str, category: str, amount: int):
        if self.get_status(source, category):
            self.data[source]["status"][category]["current_amount"] = amount
            self.save()

    def add_amount(self, source: str, category: str, amount: int):
        self.set_current_amount(source, category, self.get_current_amount(source, category) + amount)

    def get_expected(self, source: str, category: str) -> Optional[str]:
        status = self.get_status(source, category)
        return status.get("expected") if status else None

    def set_expected(self, source: str, category: str, expected: int):
        if self.get_status(source, category):
            self.data[source]["status"][category]["expected"] = expected
            self.save()

    # --- Finished categories ---

    def get_finished_categories(self, source: str) -> list:
        return self.data.get(source, {}).get("finished_category", [])

    def mark_category_finished(self, source: str, category: str):
        self._ensure_source(source)
        finished = self.data[source]["finished_category"]
        if category not in finished:
            finished.append(category)
            self.save()

    def get_unfinished_categories(self, source: str) -> list:
        categories = set(self.get_categories(source))
        finished = set(self.get_finished_categories(source))
        return list(categories - finished)
    
    # --- Stop date ---
    def get_stop_date(self, source: str) -> Optional[str]:
        return self.data.get(source, {}).get("stop_date")

    def set_stop_date(self, source: str, stop_date: str):
        self._ensure_source(source)
        self.data[source]["stop_date"] = stop_date
        self.save()