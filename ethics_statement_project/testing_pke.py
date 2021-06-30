from pke.unsupervised import YAKE
from nltk.corpus import stopwords

document = "Machine learning (ML) is the study of computer algorithms that improve automatically through experience. It is seen as a subset of artificial intelligence."

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
print(key_phrases)