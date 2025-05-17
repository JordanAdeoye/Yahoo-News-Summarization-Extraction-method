import requests
from bs4 import BeautifulSoup as bs

# We go to every dictionary value, and use request to get the content of each article,
# then we use bs4 to get the p tag, which is the text of the article.
# Since we only want the content of the article, but the p tag returns some other information after the end of the article
# (e.g. some recommendation to view other articles), we don't want that.
# One thing I noticed is that most articles end with some words which I store in the end_words list,
# so I loop through each article and once I see any word in the end_words list I delete from that word to the end.
# I wouldn't say it's 100 percent accurate but it's like 90 percent accurate cause there are just so many possible ways for an article to end.

end_words = [
    'Follow us on Twitter and Instagram',
    "follow us on Facebook, Twitter, and Instagram",
    'More Latest News!', 'TRENDING', 'Recommended Stories',
    'POPULAR', 'Read More', 'Latest Stories'
]

def extract_article_text(working_set_reversed, num_of_new_articles):
    for index, working in enumerate(working_set_reversed[:num_of_new_articles]):
        res = requests.get(list(working.values())[0])
        soup = bs(res.content, 'html.parser')
        text = [i.get_text() for i in soup.find_all(['h2', 'p'])]

        for word in text:
            if word in end_words:
                print(index, word)
                working_set_reversed[index][list(working_set_reversed[index].keys())[0]] = text[0:text.index(word)]
                break
            else:
                working_set_reversed[index][list(working_set_reversed[index].keys())[0]] = text[0:]

    return working_set_reversed
