import re
import unicodedata
from typing import Dict, List
    
def normalize_articles(raw_articles: List[Dict], category: str, source_label: str) -> List[Dict]:
    """
    Normalize raw articles into a consistent format.

    Args:
        raw_articles (List[Dict]): List of raw article dictionaries from an API or other source.
        category (str): Label to assign to the category field (e.g., "politics").
        source_label (str): Identifier for the article source (e.g., "NewsData").

    Returns:
        List[Dict]: List of normalized article dictionaries with consistent fields.
    """
    normalized = []
    for a in raw_articles:
        normalized.append({
            "title": a.get("title", ""),
            "description": a.get("description", ""),
            "url": a.get("url", ""),
            "date": a.get("published_date", "")[:10],
            "category": category,
            "source": source_label
        })
    return normalized

def clean_text_pipeline(text: str) -> str:
    """
    Clean and normalize a text string for further processing.

    Steps include:
    - Lowercasing
    - Removing accents
    - Stripping URLs
    - Removing punctuation
    - Collapsing whitespace

    Args:
        text (str): The input string to clean.

    Returns:
        str: Cleaned and normalized text.
    """
    text = text.lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")  # remove accents
    text = re.sub(r"http\S+|www\S+", "", text)  # remove URLs
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text)  # normalize whitespace
    return text.strip()