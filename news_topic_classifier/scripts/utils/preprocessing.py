from typing import List, Dict
import pandas as pd
from utils.data_io import get_columns_to_saved

def articles_to_df(source: str, articles: List[Dict]) -> pd.DataFrame:
    """
    Converts a list of articles into a dataframe

    Steps include:
    - Converts a list into a pandas dataframe
    - Selects certains columns of interest, based on a config file
    - Renames columns for uniformity

    Args:
        source (str): The source API used
        articles (List[Dict]): The list of articles to be converted

    Returns:
        pd.DataFrame: Dataframe with selected columns renamed
    """
    config = get_columns_to_saved(source)
    df = pd.DataFrame(articles)
    df = df[config.keys()].copy()
    df.rename(columns = config, inplace = True)
    return df

def deduplicate_articles(articles: List[Dict], key: str = "title") -> List[Dict]:
    """
    Remove duplicate articles based on a key (e.g., title or url).

    Args:
        articles (List[Dict]): List of articles
        key (str): The key criteria to drop duplicates

    Returns:
        List[Dict]: Dataframe with no duplicates
    """
    df = pd.DataFrame(articles)
    if key in df.columns:
        df = df.drop_duplicates(subset = [key])
    return df.to_dict(orient = "records")