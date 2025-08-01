from news_topic_classifier.utils.text_cleaning import clean_text
import pandas as pd

def clean_articles(data: pd.DataFrame) -> pd.DataFrame:
    data["title"] = data["title"].apply(clean_text)
    return data