import numpy as np
import pandas as pd

from gensim.test.utils import common_texts
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from collections import namedtuple
import gensim.utils
import re
import string

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords

data: pd.DataFrame = pd.read_csv('../data_concated.csv')
data.drop_duplicates('reason', inplace=True)
test = data.iloc[0]['reason']

stopwords_english = stopwords.words('english')
reasons = np.array(data['reason'])
left_animes = np.array(data['left'])
right_animes = np.array(data['right'])

docs = []
punctuation_regexp = re.compile('[%s]' % string.punctuation)
print("START PREPROCESS")
n = 0
for left_anime, right_anime, reason in zip(left_animes, right_animes, reasons):
    print("{}/{}".format(n, len(left_animes)))
    try:
        r = punctuation_regexp.sub('', gensim.utils.to_unicode(reason).lower())
    except TypeError:
        print(reason)
        continue
    tokens = word_tokenize(reason)
    removed_stop_words = [w for w in tokens if w not in stopwords_english]
    tags = [left_anime, right_anime]
    docs.append(TaggedDocument(removed_stop_words, tags=tags))
    n += 1

model = Doc2Vec(docs, vector_size=32, min_count=5, window=2, workers=2)
model.save('doc2vec')






