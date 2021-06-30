import os
import pandas as pd
import logging
import numpy as np

HOME = os.getcwd()
df = pd.read_csv(os.path.join(HOME, 'ethics_statement_frontiers_100.csv'), usecols = ['parsed'])
#print(df)
parsed_ethics_statement = df.parsed.to_list()
logging.basicConfig(level=logging.INFO)
logging.info(parsed_ethics_statement)

df_intro = pd.read_csv(os.path.join(HOME, 'ethics_statement_frontiers_100_intro_spacy.csv'), usecols = ['parsed'])
#print(df)
parsed_intro = df_intro.parsed.to_list()
logging.basicConfig(level=logging.INFO)
logging.info(parsed_intro)

combined_parsed = parsed_ethics_statement + parsed_intro
logging.basicConfig(level=logging.INFO)
logging.info("combining the ethics statement and intro lists")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(combined_parsed)
true_k = 3

model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
 print('Cluster %d:' % i),
 for ind in order_centroids[i, :15]:
     print('%s' % terms[ind])



print('\n')
print('Prediction')
X = vectorizer.transform(["The studies involving human participants were reviewed and approved by the Hospital Ethics Committee of the International Peace Maternity Child Health Hospital of China Welfare Institute (IPMCH). The patients/participants provided their written informed consent to participate in this study."])
predicted = model.predict(X)
print(predicted)


'''
from sklearn.preprocessing import normalize
import spacy
nlp = spacy.load("en_core_web_sm")
def vectorize(parsed_ethics_statement):
    # Get the SpaCy vector -- turning off other processing to speed things up
    return nlp(parsed_ethics_statement, disable=['parser', 'tagger', 'ner']).vector

# Now we stack the vectors and normalize them
# Inputs are typically called "X"
X = normalize(np.stack(vectorize(t) for t in parsed_ethics_statement))
print("X (the document matrix) has shape: {}".format(X.shape))
print("That means it has {} rows and {} columns".format(X.shape[0], X.shape[1]))

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X2 = pca.fit_transform(X)
print("X2 shape is {}".format(X2.shape))

import matplotlib.pyplot as plt
def plot_groups(X, y, groups):
    for group in groups:
        plt.scatter(X[y == group, 0], X[y == group, 1], label=group, alpha=0.4)
    plt.legend()
    plt.show()
    
plot_groups(X2, posts.group, ('comp.os.ms-windows.misc', 'alt.atheism'))
'''
'''https://towardsdatascience.com/applying-machine-learning-to-classify-an-unsupervised-text-document-e7bb6265f52'''