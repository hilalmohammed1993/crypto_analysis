import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def fetch_news(query, limit=5):
    """
    Fetches news headlines from Google News RSS.
    """
    # Simple Google News RSS URL
    url = f"https://news.google.com/rss/search?q={query}+crypto&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

    soup = BeautifulSoup(response.content, features="xml")
    items = soup.findAll('item')
    
    news_items = []
    for item in items[:limit]:
        title = item.title.text
        link = item.link.text
        pub_date = item.pubDate.text
        news_items.append({
            'title': title,
            'link': link,
            'pub_date': pub_date
        })
        
    return news_items

def analyze_sentiment(text):
    """
    Analyzes sentiment of a string.
    Returns polarity (-1 to 1) and a subjective analysis.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
        
    return sentiment, polarity
