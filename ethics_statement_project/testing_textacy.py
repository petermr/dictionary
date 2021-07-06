#testing_textacy
import pandas as pd
import spacy
import textacy
import os
import logging
HOME = os.getcwd()
df = pd.read_csv(os.path.join(HOME, 'ethics_statement_frontiers_100.csv'), usecols = ['parsed'])
#preproc = textacy.preprocessing.make_pipeline(textacy.preprocessing.normalize.unicode,textacy.preprocessing.normalize.quotation_marks,textacy.preprocessing.normalize.whitespace)
#preproc_records = ((preproc(text), meta) for text, meta in records)
parsed_paragraphs = df.parsed.to_list()
corpus = textacy.Corpus("en_core_web_sm", data=parsed_paragraphs)
print(corpus)

from functools import partial
for doc in corpus:
    terms = list(textacy.extract.terms(doc,ngs=partial(textacy.extract.ngrams, n=2, include_pos={"NOUN", "ADJ"}),ents=partial(textacy.extract.entities, include_types={"PERSON", "ORG", "GPE", "LOC"})))

for term in terms:
    tokenized_docs = (textacy.extract.terms_to_strings(terms, by="lemma"))

import textacy.representations
doc_term_matrix, vocab = textacy.representations.build_doc_term_matrix(tokenized_docs, tf_type="linear", idf_type="smooth")
doc_term_matrix

import textacy.tm
model = textacy.tm.TopicModel("nmf", n_topics=10, max_iter=1000)
model.fit(doc_term_matrix)

doc_topic_matrix = model.transform(doc_term_matrix)
doc_topic_matrix.shape

doc_topic_matrix