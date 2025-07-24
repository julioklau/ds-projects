from dotenv import load_dotenv
from news_topic_classifier.utils.data_io import save_to_jsonl, fetch_news, load_checkpoint, save_checkpoint
import os

load_dotenv()
API_URL = "https://newsapi.org/v2/everything"
API_KEY = os.getenv('news_api_apikey')  # put in env var or config

def fetch_paged_news(q: str, date: str, category: str, max_pages: int = 5, 
                     checkpoint_path: str = "data/api_checkpoint.json") -> list[dict]:
    checkpoint = load_checkpoint(checkpoint_path)
    start_page = checkpoint.get(category, {}).get(date, 1)

    all_articles = []

    for page in range(start_page, max_pages + 1):
        print(f"📄 Page {page} | {category} | {date}")
        data = fetch_news(
            api_url="https://newsapi.org/v2/everything",
            params={
                "q": q,
                "from": date,
                "to": date,
                "language": "es",
                "sortBy": "publishedAt",
                "pageSize": 100,
                "page": page
            },
            headers={"X-Api-Key": API_KEY}
        )

        if not data or data.get("status") != "ok":
            print("❌ Stopped due to error or credits limit.")
            break

        articles = data.get("articles", [])
        if not articles:
            break

        all_articles.extend(articles)

        # 🔄 Save progress
        checkpoint.setdefault(date, {})[category] = page + 1
        save_checkpoint(checkpoint, checkpoint_path)

        # 💡 Optional: Break if near 100 results per day limit (for free tier)
        if page * 100 >= data.get("totalResults", 0):
            break

    return all_articles

def get_news_api():
    pass