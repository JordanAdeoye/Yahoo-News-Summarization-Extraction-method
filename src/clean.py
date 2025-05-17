import re

# Below comments are some things that need to be cleaned from the articles
# 
# pic.twitter.com/...
# — theblaze (@theblaze) ...
# more from 
# \xa0
# \'
# [...]
# —
# View this post on Instagram
# Emojis, line breaks, odd formatting, etc.

emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002500-\U00002BEF"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U00010000-\U0010ffff"
    u"\u2640-\u2642"
    u"\u2600-\u2B55"
    u"\u200d"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\ufe0f"  # dingbats
    u"\u3030"
"]+", flags=re.UNICODE)

def clean_up(working_set_copy, num_of_new_articles):
    for j, i in enumerate(working_set_copy[:num_of_new_articles]):
        key = list(i.keys())[0]
        text = i[key]

        text = re.sub('"|“', "", text)
        text = re.sub('\\\xa0', " ", text)
        text = re.sub("\\\'", "'", text)

        if re.search(emoji_pattern, text):
            text = re.sub(emoji_pattern, '', text)

            reg = re.search(r'(\.|,)([ ]){2,}(\.|,)', text)
            reg2 = re.search(r'\s{2,}(\.|,)', text)
            if reg:
                text = re.sub(r'(\.|,)([ ]){2,}(\.|,)', reg.groups()[-1] + ' ', text)
            if reg2:
                text = re.sub(r'\s{2,}(\.|,)', reg2.groups()[-1] + ' ', text)

        reggs = re.search(r'(\[)(.+)(\])', text)
        if reggs:
            text = re.sub(r'(\[)(.+)(\])', reggs.groups()[1], text)

        text = re.sub(r'([\. | |pic\.].{,25}[ ]+—[ ]+[a-zA-Z ]+\s\(@\w+\)\s\w{3,9}\s\d{1,2},\s\d{2,4})', '. ', text)
        text = re.sub(r'\s{2,}View this post on Instagram\s{2,}A post shared by .{2,15}\s?\(@.+\)', '', text)

        working_set_copy[j][key] = text

    return working_set_copy[:num_of_new_articles]
