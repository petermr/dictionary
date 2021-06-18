**Table of Contents**
- [1. Motivation and Goals](#1-motivation-and-goals)
- [2. WikiProject Ethics](#2-wikiproject-ethics)
- [3. Test Mini-Corpora - Using `pygetpapers`](#3-test-mini-corpora---using-pygetpapers)
  - [3.1. Mini-Corpus #1](#31-mini-corpus-1)
  - [3.2. Mini-Corpus #2](#32-mini-corpus-2)
  - [3.3. Mini-Corpus #3](#33-mini-corpus-3)
- [4. `ami` dictionary - Ontology](#4-ami-dictionary---ontology)
- [5. Updates](#5-updates)
  - [5.1. Exploration on 2021-06-18](#51-exploration-on-2021-06-18)
  - [5.2. SPARQL Class (2021-06-16) - Potential Integration with ami](#52-sparql-class-2021-06-16---potential-integration-with-ami)
  - [5.3. Better globbing, Regex and SPARQL Wrapper (2021-06-15)](#53-better-globbing-regex-and-sparql-wrapper-2021-06-15)
  - [5.4. Entity Recognition using spaCy and NLTK with automatic scraping (2021-06-09)](#54-entity-recognition-using-spacy-and-nltk-with-automatic-scraping-2021-06-09)
  - [5.5. Entity Recognition using spaCy (2021-06-06)](#55-entity-recognition-using-spacy-2021-06-06)
  - [5.6. Ethics Statment Prototype dictionary (2021-06-01)](#56-ethics-statment-prototype-dictionary-2021-06-01)
- [6. Meeting Records](#6-meeting-records)
  - [6.1. 2021-06-17](#61-2021-06-17)
  - [6.2. 2021-06-10](#62-2021-06-10)
  - [6.3. 2021-06-03](#63-2021-06-03)
  - [6.4. 2021-05-27](#64-2021-05-27)
  - [6.5. 2021-05-20](#65-2021-05-20)
  - [6.6. 2021-05-10](#66-2021-05-10)
  - [6.7. 2021-05-07](#67-2021-05-07)
- [7. Tasks](#7-tasks)
- [8. Previous Documentation](#8-previous-documentation)
  - [8.1. Intial Exploration](#81-intial-exploration)
  - [8.2. Ideas](#82-ideas)
  
# 1. Motivation and Goals
**Daniel Meitchen**: _While the research ecosystem is moving towards increased openness, the speed of this shift varies. For example, the process of ethical review and appraisal of scholarly research remains largely hidden from the public and even from interested observers, which impedes standardization, harmonization and interoperability, both within and across communities. A recent development in parts of biomedicine and related fields has been the systematic addition of ethics statements in publications, so as to provide some information about the ethical aspects of the reported research. Here, we propose to mine such statements for information about the process and to convert this into structured information._

We hope to create dictionaries (ontologies) of,
- Commonly used phrases in Ethics Statement
- Ethics Committees
# 2. WikiProject Ethics
The WikiProject page 
https://www.wikidata.org/wiki/Wikidata:WikiProject_Ethics
# 3. Test Mini-Corpora - Using `pygetpapers`
I have created two mini-corpora, both of them with slightly different queries. Since they are too large (1000 and 2000 papers, respectively), I've uploaded only the metadata (JSON files) of these corpora. 
## 3.1. Mini-Corpus #1
```
pygetpapers -q (METHODS:'ethics statement') -k 1000 -x -o ethics_statement_corpus_1000
```
The `JSON` file is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/eupmc_results.json).

## 3.2. Mini-Corpus #2
```
pygetpapers -q "ethics statement" -k 2000 -x -o ethics_statement_2000_generic
```
The `JSON` file is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/eupmc_results_2000.json).

## 3.3. Mini-Corpus #3
This is a [smaller corpus](https://github.com/petermr/dictionary/tree/main/ethics_statement_project/e_cancer_clinical_trial_50) of 50 papers on cancer clinical trial. 

# 4. `ami` dictionary - Ontology
I have created a prototype dictionary, after analysing the Ethics Statement sections of Mini-Corpus #1  by using phrase extraction feature of [`ami_gui.py`](https://github.com/petermr/openDiagram/blob/master/physchem/python/ami_gui.py). `ami` uses ([RAKE](https://pypi.org/project/rake-nltk/) to extract and weigh phrases from text. The selected phrases are automatically saved into `keywords.txt` file in the mini-corpus (C-Project) directory.  

I have hand-selected ~ 80 terms from my initial analysis. Using legacy `ami3`, I have converted the `.txt` file into a dictionary in `.xml` format. 
```
C:\Users\shweata\ethics_statement_corpus_1000\results>amidict -v --dictionary ethics_statement --directory rake --input rake/keywords.txt create --informat list --outformats xml,html
```
The prototype dictionary is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/results/rake/ethics_statement.xml). 

# 5. Updates
## 5.1. Exploration on 2021-06-18
- I did some experimentation by trying different publishers in EPMC queries. Surprisingly, I did not find ABSTRACTS in the abstracts. So I stuck to searching METHODS section. 
  ```
  (METHODS:"stem cell") AND ethics AND elsevier
  ```
  Hits: 306
 ```
 (METHODS:"stem cell") AND ethics statement AND elsevier
  ```

  Hits: 75

  ```
  (METHODS:"stem cell") AND elsevier
  ```

  Hits: 2186

  ```
  (METHODS:"stem cell") AND ethics statement AND Hindawi
  ```

  Hits: 41

  ```
  (METHODS:"stem cell") AND Hindawi
  ```

  Hits: 1067

  ```
  (METHODS:"stem cell") AND ethics statement AND springer nature

  ```
  Hits: 3338

  ```
  (METHODS:"stem cell") AND ethics AND PLOS
  ```

  Hits: 1481

  ```
  (METHODS:"stem cell") AND ethics statement AND PLOS
  ```

  Hits: 942

  ```
  (METHODS:"stem cell") AND ethics statement AND springer nature
  ```

  Hits: 2594

  ```
  (METHODS:"stem cell") AND ethics AND springer nature
  ```

  Hits: 2683

  ```
  (METHODS:"stem cell") AND springer nature
  ```

  Hits: 4824

  ```
  (METHODS:"stem cell") AND ethics AND frontiers
  ```

  Hits: 892

  ```
  (METHODS:"stem cell") AND frontiers
  ```
  Hits: 1882

- I also found `scispacy` python package, which we might use. 
- I added the label display using spacy to my code. 
## 5.2. SPARQL Class (2021-06-16) - Potential Integration with ami
[SPARQL class](sparql.py)
- In today's CEVOpen coding session, we turned the wrapper to a class. 
- We also explored logging and automatic documentation using `pyment` package. 

## 5.3. Better globbing, Regex and SPARQL Wrapper (2021-06-15)
[New notebook](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/Ethics_staement_dictionary_globbing_annotation_shweata.ipynb)
- Noise in text was one of our main concerns. See the previous notebook to see what I mean. I noticed that Frontiers journal had explicit Ehtics Statement label and better structure. So, I decided to create a corpus of 100 papers from Frontiers journal. 
- After sectioning the paper, I glob the Ethics Statement section from each paper and dump all the statements to a txt file. 
- And as before, I use SpaCy to do Named Entity-Recognition. 
- I've also explored using Regular Expression to retrieve more information on Ethics Committee and whether an approval was required in the first place or not. 
- We also would want to do a supervised search using `pyami` on these Ethics Statement. For that, we would like to query Wikidata and retrieve, let's say, Research Councils or Universitites. We (Peter and I) have a prototype implementation of SPARQLWrapper which queries Wikidata and returns SPARQL endpoint in XML format. We can, potentially, turn the enpoint into an `ami` dictionary. 
- Needs better documentation

## 5.4. Entity Recognition using spaCy and NLTK with automatic scraping (2021-06-09)
  I have now created a [new notebook](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/Ethics_statement_project_scraping_txt_file_containing_ethics.ipynb) which,
-  globs sections of papers in CProject with the word 'ethic' in it.
-  writes the paragraphs in the globbed section to a [`.txt`](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/ethics_statement_clinical_trial_50.txt) file.
-  does Named Entity-Recognition using spaCy
-  The entities with ORG label retrieves Ethics Committee names. 
@Daniel and @PMR: There is a lot of noise because I don't have control over which paragraphs I write. The spaCy model isn't accurate either. Any directions would be helpful. 
##  5.5. Entity Recognition using spaCy (2021-06-06)
The [notebook I've written](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/Ethics_Statement_Entity_Recognition_spacy.ipynb) does Entity Recognition with which I've been able to pull out names of Ethics Committee. 
- I manually scraped roughly 20 Ethics_Statements from a corpus on clinical trials and used spaCY for entity recognition. It is still a prototype, and I hope to extend it to a lot more papers. 
- I have not used any models to do named entity recognition. ML would be useful in this case. 
## 5.6. Ethics Statment Prototype dictionary (2021-06-01)
I have created a prototype dictionary after analysing the Ethics Statement section of Mini-Corpus #1 using [`ami_gui.py`](https://github.com/petermr/openDiagram/blob/master/physchem/python/ami_gui.py). It is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/results/rake/ethics_statement.xml).
# 6. Meeting Records
## 6.1. 2021-06-17
- Shweata presented an enhanced version of her previous Notebook. More information [here](#53-better-globbing-regex-and-sparql-wrapper-2021-06-15). 
Comments and directions:
- Try:
  -  different publishers (PLOS, Hindawi, Springer Nature, Elsevier)
  - Stem Cell Research
- We might involve citizens in annotation where they go through ethics statement and label them. Constructive combination of software and manual annotation. (semi-annotation by software + human annotation)
- n-gram word cloud of common phrases in Ethics Statements. 
- Part of speech tagging
- RDF -> build connections -> Semantic Model
- We might look at conflict of interest. 
  - people -> company
  - people -> stock
- PMR demonstrated his progress with Wikidata browser.
## 6.2. 2021-06-10
- Shweata presented her initial work with entity recognition. Comments from Daniel and Peter. 
  - Use regex along with globing
  - Tfidf to weigh the terms
- There are two possible ways to go from here:
    - Human Annotation model - coming up with two sets of data, one with phrases which are most common in Ethics Statement and other which aren't. We can then build a model to extract named entities. 
    - Semantic Model - Coming up with a set of rules which we can use to extract named entities, approval numbers and so on.
- Explore Wikidata for research councils and universities. Here is a [query](https://w.wiki/3Tsu) Daniel wrote to begin with. By doing so, we might get a better gauge for what's there and what isn't. 
## 6.3. 2021-06-03
- We have added the dictionary terms as lexemes to Wikidata
- Our next focus would be to retrieve the Ethics Committees involved in the approval process. -> Named entity recognition
- Find more interesting terms related to Ethics Statement using TF-IDF.

## 6.4. 2021-05-27
- @Daniel: Exploring with Wikidata Lexemes and Ethics Statement
- Wikdata Game - You learn or Wikidata learns or both!
  - We can come up with a Wikidata game where we ask people whether a phrase - we extracted from `ami`using RAKE - is usually present in Ethics Statement or not.

## 6.5. 2021-05-20
- We need a way to automate the retrieval of the Ethics Statement. We could do sectioning and retrieve them. But it's harder because most papers don't have a dedicated Ethics Statement (usually buried in the methods section). So, we'll have to create a dictionary, using the phrase we've initially extracted, to help with information retrieval (i.e., get Ethics Statement paragraph from papers). (Q: How does SpaCY give those phrase ranks?)
- After getting, let's say, 1000 Ethics Statement, we can again try unsupervised or even supervised phrase extraction. We can refine our dictionaries and also start extracting hospital names, committee names and their identifiers, and so on.

## 6.6. 2021-05-10
- Build a dictionary manually with frequently used n-grams in Ethics Statements.

## 6.7. 2021-05-07
- Create a dictionary with commonly used phrases (engrams) in Ethics Statements
- Pull out identifiers from these statements
- Pull out Ethics Committees and add them to Wikidata
- 
# 7. Tasks
Our next task would be:
-  to convert narrower terms into synonyms (as a child) under a broader entry term. 
-  add Wikidata Ids and Wikipedia links to entries, wherever applicable. 
-  Ethics Committee dictionary
-  refine our initial query used to create the mini-corpus to reduce the false positives.


# 8. Previous Documentation
## 8.1. Intial Exploration
Exploratory work at the beginning of the project is documented on the [Ethics Statement Project](https://github.com/petermr/dictionary/wiki/Ethics-Statement-Project) Wiki page of this repository
## 8.2. Ideas
You can also look at Daniel's [Issue](https://github.com/Daniel-Mietchen/ideas/issues/499) thread which details his previous work on Ethics Statements. 
