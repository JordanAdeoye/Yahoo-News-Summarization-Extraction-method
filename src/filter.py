import json
import re

# Check if the new news article is not in the json file, then append it to the json file then save it
# num_of_new_articles is going to be useful later on when you automate the code to only send the newly added articles

def update_article_list(info, path="data/News_articles2.json"):
    with open(path) as f:
        js_file = json.load(f)

    num_of_new_articles = 0
    for i in info:
        if i not in js_file:
            num_of_new_articles = num_of_new_articles + 1
            print(i)
            js_file.append(i)

    with open(path, 'w') as f:
        json.dump(js_file, f)

    # load the updated json file
    with open(path) as f:
        js_daily = json.load(f)

    working_set = js_daily
    return working_set, num_of_new_articles


# Remove the ads articles. 
# I noticed the ads articles don't have yahoo in the url or the keys are just whitespace. 
# I want to loop through each dictionary and use regex to find the dictionary that does have '.yahoo' and delete them from the list because those are ads or at least I know they are not news articles.
# Remove instances with whitespace as keys in the dictionary.
# Use regex to check for .yahoo in the dictionary value. 
# We reversed the working_set, so it goes from most recent article to least recent.

def filter_valid_articles(working_set, num_of_new_articles):
    working_set_reversed = working_set[::-1]
    for j, i in enumerate(working_set_reversed[:num_of_new_articles]):
        if ' ' in i or not re.search('\.yahoo\.com', working_set_reversed[j][list(i.keys())[0]]):
            num_of_new_articles = num_of_new_articles - 1

    remove_item = []
    for j, i in enumerate(working_set_reversed):
        if ' ' in i or not re.search('\.yahoo\.com', working_set_reversed[j][list(i.keys())[0]]):
            remove_item.append(working_set_reversed[j])

    for i in remove_item:
        working_set_reversed.remove(i)

    return working_set_reversed, num_of_new_articles
