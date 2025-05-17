from collections import Counter
from nltk.tokenize import sent_tokenize
import json

# We basically just take the most common sentence from each article and that's our summary 

def summarize_articles(working_set_reversed, num_of_new_articles):
    summary = []

    for j, i in enumerate(working_set_reversed[:num_of_new_articles]):
        sentences = sent_tokenize(working_set_reversed[j][list(i.keys())[0]])
        counts = Counter(sentences).most_common(int(len(sentences) * 0.3))
        summary.append({list(i.keys())[0]: ' '.join([k[0] for k in counts])})

    return summary


def update_summary_file(summary, path="data/summariesconfirm.json"):
    with open(path) as f:
        summary_file = json.load(f)

    for i in summary:
        if i not in summary_file:
            print(i)
            summary_file.append(i)

    with open(path, 'w') as f:
        json.dump(summary_file, f)
