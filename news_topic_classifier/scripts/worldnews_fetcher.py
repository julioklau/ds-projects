from dotenv import load_dotenv
from utils.data_io import load_json, load_jsonl, save_to_jsonl
from utils.api_fetcher import fetch_news
from utils.checkpoint import CheckpointManager
from utils.preprocessing import articles_to_df
from typing import Dict, List
import os

load_dotenv()
API_URL = os.getenv('worldnews_url')
API_KEY = os.getenv('worldnews_apikey')
SOURCE = "worldnews"
PAGE_SIZE = 100

def fetch_by_category_paginated(
    offset: int, 
    category: str,
    from_date: str
) -> List[Dict]:
    
    params = {
        "api-key": API_KEY,
        "category": category,
        "language": "en",
        "number": PAGE_SIZE,
        "offset": offset,
        "earliest-publish-date": from_date,
        "sort":"publish-time",
        "sort_direction":"desc"
    }

    print(f"📄 Fetched {params['offset']}")
    data, headers = fetch_news(
        api_url = API_URL,
        params = params,
        headers = {}
    )

    if not data or headers['X-API-Quota-Left'] == 0:
        print("❌ Stopped due to error or credits limit.")
        return []

    result = data.get("news", [])
    if result:
        news_df = articles_to_df(SOURCE, result)
        news_df['target'] = category
        news_df['source'] = SOURCE
        return news_df.to_dict(orient="records")
    else:
        return result

def process_worldnews() -> None:
    checkpoint = CheckpointManager()
    categories = checkpoint.get_unfinished_categories(SOURCE)
    for category in categories:
        print(f'Category: {category}')
        curent_status = checkpoint.get_status(SOURCE, category)
        current_amount = curent_status.get("current_amount", 0)
        from_date = curent_status.get("date", "")
        lower_limit = current_amount
        news = []
        while current_amount < curent_status['expected']:
            articles = fetch_by_category_paginated(current_amount, category, from_date)
            news.extend(articles)
            current_amount += len(articles)
            if len(news) >= 1000 or current_amount >= curent_status['expected'] or len(articles) == 0:
                filename = "_".join([SOURCE, category, str(lower_limit), str(current_amount)]) + ".jsonl"
                save_to_jsonl(news, filename)
                news = []
                lower_limit = current_amount
                checkpoint.set_current_amount(SOURCE, category, current_amount)
        checkpoint.mark_category_finished(SOURCE, category)
    return

if __name__ == '__main__':
    process_worldnews()