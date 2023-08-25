#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup as bs
import requests
import json
import re


# In[ ]:


r = requests.get('https://www.yahoo.com')
r.raise_for_status()


# Returns the content of url 

# In[ ]:


html = bs(r.content)


# In[ ]:


print(html.prettify())


# This is where the the each article are stored in the html code

# In[ ]:


body = html.find_all(class_="List(n) P(0) grid-layout stream-grid stream-items")
content = body[0].find_all(class_="Pos(r) D(f)")


# Code below get the gets and stores the title of each articles and the link to the article and appends it to a list

# In[ ]:


info = []
for i in content:
    try:
        i.get_text('}').split('}')[4]
    except:
        continue
    else:
        info.append({i.get_text('}').split('}')[4]:i.find('a').get('href')})
     

    

# with open('News_articles2.json','w') as f:
#     json.dump(info,f)


# Check if the new news article is not in the json file, then append it to the json file then save it
# 
# num_of_new_articles is going to be useful later on when you automate the code to only send the newly added articles
# 

# In[ ]:




with open('News_articles2.json') as f:
    js_file = json.load(f)

num_of_new_articles = 0
for i in info:
    if i not in js_file:
        num_of_new_articles = num_of_new_articles + 1
        print(i)
        js_file.append(i)
           
with open('News_articles2.json','w') as f:
    json.dump(js_file,f)
        


# In[ ]:


# load the update json file 
with open('News_articles2.json') as f:
    js_daily = json.load(f)
    
working_set = js_daily


# In[ ]:


len(working_set)


# Remove the ads articles
# 
# I noticed the ads articles don't have yahoo in the url or the keys are just whitespace
# 
# I want to loop through each dictionary and use regex to find the dictionary that does have '.yahoo' and delete them from the list because does are ads or atleat i know they are not news article
# 
# Remove instances with whitespace as keys in the dictionary
# 
# Use regex to check for .yahoo in the dictionaty value
# 
# we reversed the the working_set, so it goes from most recent article to least recent

# In[ ]:


# remove the ads articles
# i noticed the ads articles don't have yahoo in the url or the keys are just whitespace

# i want to loop through each dictionary and use regex to find the dictionary that
# does have '.yahoo' and delete them from the list because does are ads or atleat i know they are not news article

# remove instances with whitespace as keys in the dictionary
# use regex to check for .yahoo in the dictionaty value

working_set_reversed = working_set[::-1]
for j,i in enumerate(working_set_reversed[:num_of_new_articles]):
    if  ' ' in i or not re.search('\.yahoo\.com',working_set_reversed[j][list(i.keys())[0]]):
        num_of_new_articles = num_of_new_articles - 1
        
remove_item = []
for j,i in enumerate(working_set_reversed):
    if  ' ' in i or not re.search('\.yahoo\.com',working_set_reversed[j][list(i.keys())[0]]):
        remove_item.append(working_set_reversed[j])

for i in remove_item:
    working_set_reversed.remove(i)    
    


# In[ ]:


# for j,i in enumerate(working_set_reversed[:num_of_new_articles]):
#     print(i.keys())
#           [list(i.keys())[0]])


# In[ ]:


for j,i in enumerate(working_set_reversed[:num_of_new_articles]):

    print(working_set_reversed[j][list(i.keys())[0]])
print('\n')    
print("we have "+str(len(working_set))+" articles in total and we have "+str(num_of_new_articles)+" newly found articles")


# We go to every dictionary values, and use request to get the content of each articles then we use bs4 to get the p tag, which is the text of the article
# 
# since we only want the content of the article but the p tag returns some other information after the end of the article, say some recommendation to view other article and we dont want that, one thing i noticed is that most article end with some words which i store in the end_words list, so i loop through each article and once i see any any word in the end_words list and delete from that word to the end. I wouldn't say its 100 percent accurate but it's like 90 percent accurate cause they are just so many possible ways for an article to end

# In[ ]:


# we go every dictionary values, load it use request and get the <p> tag

end_words= ['Follow us on Twitter and Instagram',
"follow us on Facebook, Twitter, and Instagram",'More Latest News!','TRENDING',
'Recommended Stories',
'TRENDING','POPULAR', 'Read More','Latest Stories']

# end_words = [end_word.lower() for end_word in end_words]

for index,working in enumerate(working_set_reversed[:num_of_new_articles]):
    res = requests.get(list(working.values())[0])
    soup = bs(res.content)
    text = [i.get_text() for i in soup.find_all(['h2','p'])]

    for word in text:
        if word in end_words:
            print(index,word)
            working_set_reversed[index][list(working_set_reversed[index].keys())[0]]  = text[0:text.index(word)]
            break
        else:
            working_set_reversed[index][list(working_set_reversed[index].keys())[0]]  = text[0:]
                


# # Cleaning the articles

# These are some things that need to be cleaned from the articles

# In[ ]:


# pic.twitter.com/8wwe2lximt
# — theblaze (@theblaze) july 27, 2023
# — rep. nancy mace (@repnancymace) july 27, 2023
# more from 
# \xa0
# \'
# [...]

# —
# . that heel flick backwards from @_aryborges 🔥pic.twitter.com/agetnxr7ln — national women’s soccer league (@nwsl) 
# july 24, 2023 she earned her hat 
# trick 20 minutes of play later on another header that went between the legs of panama keeper yenith bailey. she's
# becoming inevitable 🇧🇷hat trick ary borges 🎩 pic.twitter.com/fygalerheo — fox soccer (@foxsoccer) july 24, 2023 
# marta came on for borges in the 75th minute. 

# . germany held nothing back in this one 😤🇩🇪watch all six goals from germany's 2023 fifa women's world cup opener ⬇️ pic.twitter.com/bbx7nlq8vb — fox soccer (@foxsoccer) july 24, 2023 the six goals are the most of the tournament so far. 
# https://t.co/hr1vvd7bmw — tom pelissero (@tompelissero) july 24, 2023 this is a brutal turn of events for the 26-year-old hines.

# . he lost $1.67m salary due to buyout.rep'd by pat brisson @caahockey https://t.co/8w0mfcfrau — puckpedia (@puckpedia) july 24, 2023

# \xa0
# remove \n and [it]
# ”


# In[ ]:


for j,i in enumerate(working_set_reversed[:num_of_new_articles+1]):
    working_set_reversed[j][list(working_set_reversed[j].keys())[0]] = " ".join(working_set_reversed[j][list(working_set_reversed[j].keys())[0]])


# In[ ]:


emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "\U0001F700-\U0001F77F"  # alchemical symbols
                           "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           "\U0001FA00-\U0001FA6F"  # Chess Symbols
                           "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           "\U00002702-\U000027B0"  # Dingbats
                           "\U000024C2-\U0001F251"
                           "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "\U0001F300-\U0001F5FF"  # symbols & pictographs
                           "\U0001F600-\U0001F64F"  # emoticons
                           "\U0001F680-\U0001F6FF"  # transport & map symbols
                           "\U0001F700-\U0001F77F"  # alchemical symbols
                           "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           "\U0001FA00-\U0001FA6F"  # Chess Symbols
                           "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           "\U00002702-\U000027B0"  # Dingbats
                           "\U000024C2-\U0001F251"
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
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

def clean_up(working_set_copy):
    for j,i in enumerate(working_set_copy[:num_of_new_articles]):
        working_set_copy[j][list(working_set_copy[j].keys())[0]] = re.sub('"|“', "", working_set_copy[j][list(working_set_copy[j].keys())[0]])
        working_set_copy[j][list(working_set_copy[j].keys())[0]] = re.sub('\\\xa0', " ", working_set_copy[j][list(working_set_copy[j].keys())[0]])

        working_set_copy[j][list(working_set_copy[j].keys())[0]] = re.sub("\\\'","'",working_set_copy[j][list(working_set_copy[j].keys())[0]])
    
        if re.search(emoji_pattern,working_set_copy[j][list(working_set_copy[j].keys())[0]]):
            working_set_copy[j][list(working_set_copy[j].keys())[0]] = re.sub(emoji_pattern,'',working_set_copy[j][list(working_set_copy[j].keys())[0]])

            reg = re.search(r'(\.|,)([ ]){2,}(\.|,)',working_set_copy[j][list(working_set_copy[j].keys())[0]])
            reg2 = re.search(r'\s{2,}(\.|,)',working_set_copy[j][list(working_set_copy[j].keys())[0]])
            if reg:
                working_set_copy[j][list(working_set_copy[j].keys())[0]] = re.sub(r'(\.|,)([ ]){2,}(\.|,)',reg.groups()[-1]+' ',working_set_copy[j][list(working_set_copy[j].keys())[0]])
            if reg2:
                working_set_copy[j][list(working_set_copy[j].keys())[0]] = re.sub(r'\s{2,}(\.|,)',reg2.groups()[-1]+' ',working_set_copy[j][list(working_set_copy[j].keys())[0]])

        reggs = re.search('(\[)(.+)(\])',working_set_copy[j][list(working_set_copy[j].keys())[0]])
        if reggs:
            working_set_copy[j][list(working_set_copy[j].keys())[0]] = re.sub('(\[)(.+)(\])',reggs.groups()[1],working_set_copy[j][list(working_set_copy[j].keys())[0]])
            
        working_set_copy[j][list(working_set_copy[j].keys())[0]] = re.sub('([\. | |pic\.].{,25}[ ]+—[ ]+[a-zA-Z ]+\s\(@\w+\)\s\w{3,9}\s\d{1,2},\s\d{2,4})','. ',working_set_copy[j][list(working_set_copy[j].keys())[0]])
        working_set_copy[j][list(working_set_copy[j].keys())[0]] = re.sub(r'\s{2,}View this post on Instagram\s{2,}A post shared by .{2,15}\s?\(@.+\)','',working_set_copy[j][list(working_set_copy[j].keys())[0]])
    return working_set_copy[:num_of_new_articles]
        
    

    
articles = clean_up(working_set_reversed)
print(articles[:5])


# In[ ]:





# In[ ]:





# # nltk 

# We basically just take the most common word from each articles and that's our summary 

# In[ ]:


from collections import Counter
from nltk.tokenize import sent_tokenize,word_tokenize,PunktSentenceTokenizer
summary = []

for j,i in enumerate(working_set_reversed[:num_of_new_articles]):
    counts = Counter(sent_tokenize(working_set_reversed[j][list(working_set_reversed[j].keys())[0]])).most_common(int(len(sent_tokenize(working_set_reversed[j][list(working_set_reversed[j].keys())[0]]))*0.3))

    summary.append({list(working_set_reversed[j].keys())[0]:' '.join([k[0] for k in counts])})


# In[ ]:


with open('summariesconfirm.json') as f:
    summary_file = json.load(f)


for i in summary:
    if i not in summary_file :
        print(i)
        summary_file.append(i)
           
with open('summariesconfirm.json','w') as f:
    json.dump(summary_file,f)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




