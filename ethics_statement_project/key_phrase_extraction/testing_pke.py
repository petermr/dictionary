import os
import pandas as pd
import logging
import spacy
import pke
from pke import utils
import numpy as np


nlp = spacy.load("en_core_web_sm")


HOME = os.getcwd()
df = pd.read_csv(os.path.join(HOME, 'ethics_statement_frontiers_1000_spacy.csv'), usecols = ['parsed'])
parsed_ethics_statement = df.parsed.to_list()
logging.basicConfig(level=logging.INFO)
logging.info(f"found {len(parsed_ethics_statement)} ethics statements")

document = ' '.join(map(str, parsed_ethics_statement))
from pke.unsupervised import YAKE
from nltk.corpus import stopwords
from pke import compute_document_frequency
from string import punctuation

df1 =pd.read_csv(os.path.join(HOME, 'ethics_statement_frontiers_1000_spacy.csv'), usecols =['parsed'])
pes = df1.parsed.to_list()
with open('your_file.txt', 'w', encoding='utf-8') as f:
    for item in pes:
      f.write("%s\n" % item)
#pke.utils.compute_lda_model("your_file.txt", "C:/Users/91981/dictionary/ethics_statement_project/ldamod.gz", n_topics=10, extension='txt', language='en', normalization='stemming')
"""Compute Document Frequency (DF) counts from a collection of documents.

N-grams up to 3-grams are extracted and converted to their n-stems forms.
Those containing a token that occurs in a stoplist are filtered out.
Output file is in compressed (gzip) tab-separated-values format (tsv.gz).
"""

# stoplist for filtering n-grams
stoplist=list(punctuation)

# compute df counts and store as n-stem -> weight values
compute_document_frequency(input_dir= "your_file.txt" ,
                           output_file= "C:/Users/91981/dictionary/ethics_statement_project/dftsv.tsv.gz",
                           extension='txt',           # input file extension
                           language='en',                # language of files
                           normalization="stemming",    # use porter stemmer
                           stoplist=stoplist)

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


import pke

# define the set of valid Part-of-Speeches
pos = {'NOUN', 'PROPN', 'ADJ'}

# 1. create a TextRank extractor.
extractor = pke.unsupervised.TextRank()

# 2. load the content of the document.
extractor.load_document(input=document,
                        language='en',
                        normalization=None)

# 3. build the graph representation of the document and rank the words.
#    Keyphrase candidates are composed from the 33-percent
#    highest-ranked words.
extractor.candidate_weighting(window=2,
                              pos=pos,
                              top_percent=0.33)

# 4. get the 10-highest scored candidates as keyphrases
keyphrases_textrank = extractor.get_n_best(n=10)
for key_phrase in keyphrases_textrank :
    logging.info(f"phrases found using text rank {key_phrase}")
import pke

# define the set of valid Part-of-Speeches
pos = {'NOUN', 'PROPN', 'ADJ'}

# 1. create a SingleRank extractor.
extractor = pke.unsupervised.SingleRank()

# 2. load the content of the document.
extractor.load_document(input=document,
                        language='en',
                        normalization=None)

# 3. select the longest sequences of nouns and adjectives as candidates.
extractor.candidate_selection(pos=pos)

# 4. weight the candidates using the sum of their word's scores that are
#    computed using random walk. In the graph, nodes are words of
#    certain part-of-speech (nouns and adjectives) that are connected if
#    they occur in a window of 10 words.
extractor.candidate_weighting(window=10,
                              pos=pos)

# 5. get the 10-highest scored candidates as keyphrases
keyphrases_singlerank = extractor.get_n_best(n=10)
for key_phrase in keyphrases_singlerank:
    logging.info(f"phrases found using single rank {key_phrase}")
import pke

# define the valid Part-of-Speeches to occur in the graph
pos = {'NOUN', 'PROPN', 'ADJ'}

# define the grammar for selecting the keyphrase candidates
grammar = "NP: {<ADJ>*<NOUN|PROPN>+}"

# 1. create a PositionRank extractor.
extractor = pke.unsupervised.PositionRank()

# 2. load the content of the document.
extractor.load_document(input=document,
                        language='en',
                        normalization=None)

# 3. select the noun phrases up to 3 words as keyphrase candidates.
extractor.candidate_selection(grammar=grammar,
                              maximum_word_number=3)

# 4. weight the candidates using the sum of their word's scores that are
#    computed using random walk biaised with the position of the words
#    in the document. In the graph, nodes are words (nouns and
#    adjectives only) that are connected if they occur in a window of
#    10 words.
extractor.candidate_weighting(window=10,
                              pos=pos)

# 5. get the 10-highest scored candidates as keyphrases
keyphrases_position = extractor.get_n_best(n=10)
for key_phrase in keyphrases_position:
    logging.info(f"phrases found using position rank {key_phrase}")

from rake_nltk import Rake
r = Rake()
r.extract_keywords_from_text(document)
print(r.get_ranked_phrases())




import pke

# 1. create a KPMiner extractor.
extractor = pke.unsupervised.KPMiner()

# 2. load the content of the document.
extractor.load_document(input=document,
                        language='en',
                        normalization=None)


# 3. select {1-5}-grams that do not contain punctuation marks or
#    stopwords as keyphrase candidates. Set the least allowable seen
#    frequency to 5 and the number of words after which candidates are
#    filtered out to 200.
lasf = 5
cutoff = 200
extractor.candidate_selection(lasf=lasf, cutoff=cutoff)

# 4. weight the candidates using KPMiner weighting function.
df = pke.load_document_frequency_file(input_file="C:/Users/91981/dictionary/ethics_statement_project/dftsv.tsv.gz")
alpha = 2
sigma = 3
extractor.candidate_weighting(df=df, alpha=alpha, sigma=sigma)

# 5. get the 10-highest scored candidates as keyphrases
keyphrases_kpminer = extractor.get_n_best(n=10)
for key_phrase in keyphrases_kpminer :
    logging.info(f"phrases found using kpminer {key_phrase}")

import string
import pke

# 1. create a TfIdf extractor.
extractor = pke.unsupervised.TfIdf()

# 2. load the content of the document.
extractor.load_document(input=document,
                        language='en',
                        normalization=None)

# 3. select {1-3}-grams not containing punctuation marks as candidates.
stoplist=stopwords.words('english')
extractor.candidate_selection(n=3, stoplist=stoplist)

# 4. weight the candidates using a `tf` x `idf`
df = pke.load_document_frequency_file(input_file="C:/Users/91981/dictionary/ethics_statement_project/dftsv.tsv.gz")
extractor.candidate_weighting(df=df)

# 5. get the 10-highest scored candidates as keyphrases
keyphrases_tfidf= extractor.get_n_best(n=10)
for key_phrase in keyphrases_tfidf:
    logging.info(f"phrases found using tf-idf {key_phrase}")

import pke
from nltk.corpus import stopwords

# define the valid Part-of-Speeches to occur in the graph
pos = {'NOUN', 'PROPN', 'ADJ'}

# define the grammar for selecting the keyphrase candidates
grammar = "NP: {<ADJ>*<NOUN|PROPN>+}"

# 1. create a TopicalPageRank extractor.
extractor = pke.unsupervised.TopicalPageRank()

# 2. load the content of the document.
extractor.load_document(input=document,
                        language='en',
                        normalization=None)

# 3. select the noun phrases as keyphrase candidates.
extractor.candidate_selection(grammar=grammar)

# 4. weight the keyphrase candidates using Single Topical PageRank.
#    Builds a word-graph in which edges connecting two words occurring
#    in a window are weighted by co-occurrence counts.
extractor.candidate_weighting(window=10,
                              pos=pos,
                              lda_model="C:/Users/91981/dictionary/ethics_statement_project/ldamod.gz")

# 5. get the 10-highest scored candidates as keyphrases
keyphrases_topical = extractor.get_n_best(n=10)
for key_phrase in keyphrases_topical:
    logging.info(f"phrases found using topical page rank {key_phrase}")
