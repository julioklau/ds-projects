from dotenv import load_dotenv
from utils.data_io import save_to_jsonl
from utils.api_fetcher import fetch_news
from utils.checkpoint import CheckpointManager
from utils.preprocessing import articles_to_df
import os
from typing import Dict, List

load_dotenv()
API_URL = os.getenv('fcsapi_url') 
API_KEY = os.getenv('fcsapi_apikey') 
SOURCE = "fcsapi"
PAGE_SIZE = 100

def fetch_by_category_paginated(
    offset: int, 
    category: str
) -> List[Dict]:
    
    params = {
        "access_key": API_KEY,
        "category": category,
        "language": "en",
        "limit": PAGE_SIZE,
        "offset": offset
    }
    
    print(f"📄 Fetched {params['offset']}")
    data, _ = fetch_news(
        api_url = API_URL,
        params = params,
        headers = {}
    )

    if not data or data.get("code") != 200:
        print("❌ Stopped due to error or credits limit.")
        return []

    result = data.get("response", [])
    if result:
        news_df = articles_to_df(SOURCE, result)
        news_df['target'] = category
        news_df['source'] = SOURCE
        return news_df.to_dict(orient="records")
    else:
        return result

def process_fcsapi() -> None:
    checkpoint = CheckpointManager()
    categories = checkpoint.get_unfinished_categories(SOURCE)
    for category in categories:
        print(f'Category: {category}')
        curent_status = checkpoint.get_status(SOURCE, category)
        current_amount = curent_status['current_amount']
        lower_limit = current_amount
        news = []
        while current_amount < curent_status['expected']:
            articles = fetch_by_category_paginated(current_amount, category)
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
    process_fcsapi()