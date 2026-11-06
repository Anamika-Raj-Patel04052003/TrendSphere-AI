import feedparser

RSS_FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml"
}


def fetch_news():
    articles = []

    for source, feed_url in RSS_FEEDS.items():

        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            article = {
                "source": source,
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")
            }

            articles.append(article)

    return articles