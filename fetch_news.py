import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def fetch_ai_news():
    """Fetch AI news from a predefined source."""
    url = "https://example-ai-news-source.com"  # Replace with actual source
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_items = []
    for item in soup.select('.news-item'):  # Adjust selector based on source
        title = item.select_one('h2').text.strip()
        summary = item.select_one('p').text.strip()
        url = item.select_one('a')['href']
        news_items.append({
            'title': title,
            'summary': summary,
            'url': url
        })
    return news_items

def save_news_to_file(news_items):
    """Save news items to a JSON file named with today's date."""
    today = datetime.now().strftime('%Y-%m-%d')
    file_path = f"news_{today}.json"
    
    with open(file_path, 'w') as f:
        json.dump(news_items, f, indent=4)
    return file_path

if __name__ == "__main__":
    news = fetch_ai_news()
    save_news_to_file(news)
    print(f"News saved to: news_{datetime.now().strftime('%Y-%m-%d')}.json")