import os
import json
import datetime
import feedparser
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import chardet

def detect_encoding(byte_content):
    """自动检测字节流的编码"""
    result = chardet.detect(byte_content)
    return result['encoding'] or 'utf-8'

def fetch_article_content(url):
    """双重策略获取内容（优先检测编码+BeautifulSoup）"""
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/133.0.0.0 Safari/537.36')
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        raw = resp.content
        enc = detect_encoding(raw)
        text = raw.decode(enc, errors='replace')

        soup = BeautifulSoup(text, 'html.parser')
        selectors = [
            'div.article-content', 'div.article', 'div.content',
            'div#content', 'div.main-content', 'div.news-txt'
        ]
        content = ""
        for sel in selectors:
            block = soup.select_one(sel)
            if block:
                paragraphs = block.find_all('p')
                content = " ".join(p.get_text(strip=True) for p in paragraphs)
                if content:
                    break

        if not content:
            article = Article(url, language='zh', memoize_articles=False)
            article.download()
            article.parse()
            content = article.text

        return content[:300] + "..." if len(content) > 300 else content

    except Exception as e:
        return f"内容获取失败: {str(e)}"

def fetch_news(rss_url, limit=5):
    """抓取新闻列表"""
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/133.0.0.0 Safari/537.36')
        }
        resp = requests.get(rss_url, headers=headers, timeout=10)
        raw = resp.content
        enc = detect_encoding(raw)
        decoded = raw.decode(enc, errors="replace")

        feed = feedparser.parse(decoded)

        articles = []
        for entry in feed.entries[:limit]:
            title = entry.get("title", "无标题").strip()
            url = entry.get("link", "")
            summary = entry.get("summary", "").strip()
            if not summary or len(summary) < 20:
                summary = fetch_article_content(url)
            articles.append({
                "title": title,
                "summary": summary,
                "url": url
            })
        return articles
    except Exception as e:
        print(f"⚠️ 新闻获取失败: {str(e)}")
        return []

def save_news_to_file(news_list, folder="../data"):
    """按日期保存到 JSON 文件"""
    os.makedirs(folder, exist_ok=True)
    today = datetime.date.today().isoformat()  # 格式 YYYY-MM-DD
    file_path = os.path.join(folder, f"news_{today}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    print(f"✅ 新闻已保存到 {file_path}")

if __name__ == "__main__":
    # 示例稳定 RSS 源：中国新闻网即时新闻
    RSS_URL = "https://www.chinanews.com.cn/rss/scroll-news.xml"
    news_list = fetch_news(RSS_URL, limit=5)
    save_news_to_file(news_list)
