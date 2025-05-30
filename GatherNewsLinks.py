# %%
import feedparser
import os
import shutil
import datetime
import json
import pandas as pd
from urllib.parse import urlparse, parse_qs

# Function to get top articles
def get_top_articles(query, source='google', num_articles=5):
    if source == 'google':
        url = f'https://news.google.com/rss/search?q={query}'
    elif source == 'bing':
        url = f'https://www.bing.com/news/search?q={query}&format=rss'
    else:
        raise ValueError("Source must be either 'google' or 'bing'")
    
    feed = feedparser.parse(url)
    articles = []
    
    for entry in feed.entries[:num_articles]:
        # Extract source details if available
        source_href = entry.get('source', {}).get('href', '#')
        source_title = entry.get('source', {}).get('title', 'Unknown Source')
        
        # Extract the original link from the Google News redirect link
        original_link = entry.link
        if 'news.google.com' in original_link:
            parsed_url = urlparse(original_link)
            query_params = parse_qs(parsed_url.query)
            original_link = query_params.get('url', [original_link])[0]  # Fallback to the original link if 'url' is not found
        
        articles.append({
            'title': entry.title,
            'link': original_link,
            'source': {'href': source_href, 'title': source_title},
            'published': entry.published
        })
    
    return articles

# Function to save articles to a JSON file
def save_articles_to_json(articles, filename, topic):
    if os.path.exists(filename):
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        shutil.move(filename, f'{filename}_{now}.json')
    
    with open(filename, 'w') as f:
        json.dump(articles, f, indent=4)

# Function to create an HTML file from the JSON file
def create_html_file_from_json(json_file, html_file, topic):
    with open(json_file, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    with open(html_file, 'w') as file:  
        file.write('<html>\n<head>\n<title>News Articles</title>\n</head>\n<body>\n')
        file.write(f'<h1>Topic: {topic}</h1>\n')
        file.write('<ul>\n')
        for index, row in df.iterrows():
            source_href = row['source'].get('href', '#')
            source_title = row['source'].get('title', 'Unknown Source')
            published = row['published']
            file.write(f'<li><a href="{row["link"]}">{row["title"]}</a> - source: <a href="{source_href}">{source_title}</a> - published: {published}</li>\n')
        file.write('</ul>\n')
        file.write('</body>\n</html>')

# Example usage
if __name__ == "__main__":
    topic = "technology"
    articles = get_top_articles(query=topic, source='google', num_articles=5)
    json_filename = "news_articles.json"
    html_filename = "news_articles.html"
    
    save_articles_to_json(articles, json_filename, topic)
    create_html_file_from_json(json_filename, html_filename, topic)



