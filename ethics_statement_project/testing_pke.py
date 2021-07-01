import os
import pandas as pd
import logging
import numpy as np

HOME = os.getcwd()
df = pd.read_csv(os.path.join(HOME, 'ethics_statement_frontiers_1000_spacy.csv'), usecols = ['parsed'])
parsed_ethics_statement = df.parsed.to_list()
logging.basicConfig(level=logging.INFO)
logging.info(f"found {len(parsed_ethics_statement)} ethics statements")

document = ' '.join(map(str, parsed_ethics_statement))
from pke.unsupervised import YAKE
from nltk.corpus import stopwords


# 1. Create YAKE keyword extractor
extractor = YAKE()

# 2. Load document
extractor.load_document(input=document,language='en',normalization=None)


# 3. Generate candidate 1-gram and 2-gram keywords
stoplist = stopwords.words('english')
extractor.candidate_selection(n=2, stoplist=stoplist)

# 4. Calculate scores for the candidate keywords
extractor.candidate_weighting(window=2,stoplist=stoplist,use_stems=False)

# 5. Select 10 highest ranked keywords
# Remove redundant keywords with similarity above 80%
key_phrases = extractor.get_n_best(n=10, threshold=0.8)
for key_phrase in key_phrases:
    logging.info(f"phrases found using YAKE{key_phrase}")

import pke
extractor_topicrank = pke.unsupervised.TopicRank()
extractor_topicrank.load_document(document, language='en')
extractor_topicrank.candidate_selection()
extractor_topicrank.candidate_weighting()
keyphrases_topicrank = extractor_topicrank.get_n_best(n=10)
for key_phrase in keyphrases_topicrank:
    logging.info(f"phrases found using topic rank{key_phrase}")

import pke
import string
from nltk.corpus import stopwords

# 1. create a MultipartiteRank extractor.
extractor_multipartiterank = pke.unsupervised.MultipartiteRank()

# 2. load the content of the document.
extractor_multipartiterank.load_document(input=document)

# 3. select the longest sequences of nouns and adjectives, that do
#    not contain punctuation marks or stopwords as candidates.
pos = {'NOUN', 'PROPN', 'ADJ'}
stoplist = list(string.punctuation)
stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
stoplist += stopwords.words('english')
extractor_multipartiterank.candidate_selection(pos=pos, stoplist=stoplist)

# 4. build the Multipartite graph and rank candidates using random walk,
#    alpha controls the weight adjustment mechanism, see TopicRank for
#    threshold/method parameters.
extractor_multipartiterank.candidate_weighting(alpha=1.1,threshold=0.74,method='average')

# 5. get the 10-highest scored candidates as keyphrases
keyphrases_multiparitaterank = extractor_multipartiterank.get_n_best(n=10)
for key_phrase in keyphrases_multiparitaterank:
    logging.info(f"phrases found using multipartite rank {key_phrase}")