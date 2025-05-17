from src.scrape import scrape_yahoo_articles
from src.filter import update_article_list, filter_valid_articles
from src.extract import extract_article_text
from src.clean import clean_up
from src.summarize import summarize_articles, update_summary_file

def main():
    # Step 1: Scrape Yahoo homepage for latest articles
    info = scrape_yahoo_articles()

    # Step 2: Append new articles and load full working set
    working_set, num_new = update_article_list(info)

    # Step 3: Filter out ads, whitespace keys, and non-Yahoo links
    working_set_reversed, num_new_filtered = filter_valid_articles(working_set, num_new)

    # Step 4: Extract article content
    articles_with_text = extract_article_text(working_set_reversed, num_new_filtered)

    # Step 5: Clean the extracted text
    cleaned_articles = clean_up(articles_with_text, num_new_filtered)

    # Step 6: Generate summaries
    summaries = summarize_articles(cleaned_articles, num_new_filtered)

    # Step 7: Append new summaries to the summary file
    update_summary_file(summaries)

    print(f"\n✅ Completed: {num_new_filtered} new articles summarised and saved.")

if __name__ == "__main__":
    main()
