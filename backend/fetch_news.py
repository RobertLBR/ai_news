import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def fetch_ai_news():
    """Fetch AI news from a predefined source."""
    url = "https://news.163.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_items = []
    for item in soup.select('.news_title a'):  # Adjust selector for 163.com
        title = item.text.strip()
        url = item['href']
        # Fetch detailed content if needed
        detail_response = requests.get(url)
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
        summary = detail_soup.select_one('.post_text').text.strip() if detail_soup.select_one('.post_text') else "No summary available"
        news_items.append({
            'title': title,
            'summary': summary,
            'url': url
        })
    return news_items

def save_news_to_file(news_items):
    """Save news items to a JSON file named with today's date."""
    today = datetime.now().strftime('%Y-%m-%d')
    file_path = f"../data/news_{today}.json"
    
    with open(file_path, 'w') as f:
        json.dump(news_items, f, indent=4)
    return file_path

if __name__ == "__main__":
    news = fetch_ai_news()
    save_news_to_file(news)
    print(f"News saved to: ../data/news_{datetime.now().strftime('%Y-%m-%d')}.json")