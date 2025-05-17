import requests
from bs4 import BeautifulSoup as bs

def scrape_yahoo_articles():
    url = 'https://www.yahoo.com'
    r = requests.get(url)
    r.raise_for_status()

    html = bs(r.content, 'html.parser')
    body = html.find_all(class_="List(n) P(0) grid-layout stream-grid stream-items")
    content = body[0].find_all(class_="Pos(r) D(f)")

    articles = []
    for i in content:
        try:
            key = i.get_text('}').split('}')[4]
            value = i.find('a').get('href')
        except:
            continue
        else:
            articles.append({key: value})

    return articles
