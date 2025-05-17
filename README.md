# 📰 Yahoo News Summarization Extraction Method

This project scrapes headlines from Yahoo News, filters and cleans the article content, and generates summaries using basic NLP techniques (NLTK). It maintains a running JSON file of articles and summaries.

> ⚠️ **Important Note:**  
> This project was originally built when Yahoo served homepage content as static HTML.  
> As of 2024, Yahoo now uses JavaScript to load much of its content dynamically.  
> As a result, this script may no longer return results unless adapted to use a JavaScript-enabled scraping solution such as **Selenium**, **Playwright**, or **requests-html**.

---

## 🚀 Features

- Scrapes articles from Yahoo's homepage using BeautifulSoup
- Filters out non-news content and duplicate articles
- Extracts raw text from each article page
- Cleans unwanted elements (ads, emojis, quotes, whitespace)
- Summarises articles using most frequent sentences via NLTK
- Appends results to JSON files for persistent storage

---

## 📁 Project Structure
```
Yahoo-News-Summarization-Extraction-method/
├── data/
│ ├── News_articles2.json # scraped article links
│ └── summariesconfirm.json # final summaries
├── src/
│ ├── scrape.py # Yahoo homepage scraper
│ ├── filter.py # filtering + deduplication
│ ├── extract.py # extract article body
│ ├── clean.py # clean up raw text
│ └── summarize.py # summarise with NLTK
├── main.py 
├── requirements.txt 
└── README.md 
```


---

## 🧪 How to Run

> ⚠️ **Warning:**  
> Due to changes in Yahoo’s site structure, the scraper may not return any data unless updated to use a JavaScript renderer.

If you're still exploring the project:

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the script:
```bash
python main.py
```


## 📄 Output Files

- `data/News_articles2.json` — article links and title  
- `data/summariesconfirm.json` — summaries


---

## ⚠️ Disclaimer

This project is for educational use only and respects Yahoo’s terms of service.  
It was originally built as a prototype to explore web scraping, text cleaning, and NLP summarisation.

---

## 📬 Author

**Jordan Adeoye**  
Built to demonstrate skills in web scraping, data cleaning, and NLP-based summarisation.




