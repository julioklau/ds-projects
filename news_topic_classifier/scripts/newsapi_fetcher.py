from dotenv import load_dotenv
from utils.data_io import load_json, save_to_jsonl, get_script_path
from utils.api_fetcher import fetch_news
from utils.checkpoint import CheckpointManager
from utils.preprocessing import articles_to_df
from typing import Dict, List
from datetime import datetime, timedelta
import os

load_dotenv()
API_URL = os.getenv('newsapi_url') 
API_KEY = os.getenv('newsapi_apikey') 
QUERY_PATH = get_script_path()/"config"/"category_queries.json"
SOURCE = "newsapi"
PAGE_SIZE = 100
HEADERS = {"X-Api-Key": API_KEY}

def fetch_by_category(
    q: str, 
    date: str,
    category: str
) -> List[Dict]:

    params = {
        "q": q,
        "from": date,
        "to": date,
        "language": "en",
        "pageSize": PAGE_SIZE,
        "page": 1
    }

    data, _ = fetch_news(
        api_url = API_URL,
        params = params,
        headers = HEADERS
    )

    if not data or data.get("status") != "ok":
        print("❌ Stopped due to error or credits limit.")
        exit(1)

    result = data.get("articles", [])
    if result:
        news_df = articles_to_df(SOURCE, result)
        news_df['target'] = category
        news_df['source'] = SOURCE
        return news_df.to_dict(orient="records")
    else:
        return []

def process_newsapi() -> None:
    checkpoint = CheckpointManager()
    categories = checkpoint.get_unfinished_categories(SOURCE)
    stop_date = datetime.strptime(checkpoint.get_stop_date(SOURCE), "%Y-%m-%d")
    queries = load_json(QUERY_PATH)

    for category in categories:
        print(f'Category: {category}')
        curent_status = checkpoint.get_status(SOURCE, category)
        keywords = queries[category]
        current_date = datetime.strptime(curent_status['date'], "%Y-%m-%d")
        current_amount = curent_status['current_amount']
        while current_date <= stop_date and current_amount < curent_status['expected']:
            date_str = current_date.strftime("%Y-%m-%d")
            print(f"Date: {date_str}")
            news = []
            for query in keywords:
                articles = fetch_by_category(query, date_str, category)
                news.extend(articles)
                    
            #Insertion
            filename = "_".join([SOURCE, category, date_str]) + ".jsonl"
            save_to_jsonl(news, filename)
            current_date += timedelta(days = 1)
            current_amount += len(news)
            checkpoint.set_date(SOURCE, category, current_date.strftime("%Y-%m-%d"))
            checkpoint.set_current_amount(SOURCE, category, current_amount)
        checkpoint.mark_category_finished(SOURCE, category)
    return

if __name__ == '__main__':
    process_newsapi()