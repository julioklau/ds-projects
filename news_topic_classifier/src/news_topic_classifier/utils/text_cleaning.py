import re
import unicodedata
    
def clean_text(text: str) -> str:
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