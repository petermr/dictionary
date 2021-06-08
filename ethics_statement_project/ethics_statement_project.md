- [2. Dictionary](#2-dictionary)
- [3. Tasks](#3-tasks)
- [4. Update from 2021-05-04 meeting:](#4-update-from-2021-05-04-meeting)
- [5. Entity Recognition using spaCy](#5-entity-recognition-using-spacy)
I have created two mini-corpora, both of them with slightly different queries. Since they are too large (1000 and 2000 papers, respectively), I've uploaded the JSON file containing the metadata for individual corpus. 
### 1.1. Mini-Corpus #1
```
pygetpapers -q (METHODS:'ethics statement') -k 1000 -x -o ethics_statement_corpus_1000
```
The `JSON` file is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/eupmc_results.json).

### 1.2. Mini-Corpus #2
```
pygetpapers -q "ethics statement" -k 2000 -x -o ethics_statement_2000_generic
```
The `JSON` file is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/eupmc_results_2000.json).

## 2. Dictionary
I have created a prototype dictionary after analysing the Ethics Statement section of Mini-Corpus #1 using [`ami_gui.py`](https://github.com/petermr/openDiagram/blob/master/physchem/python/ami_gui.py). The tool does phrase extraction using [RAKE](https://pypi.org/project/rake-nltk/). It also saves the selected phrases into `keywords.txt` file in the mini-corpus (C-Project) directory.  

I have hand-selected ~ 80 terms from my initial analysis. Using legacy `ami3`, I have created the `.txt` file into a dictionary in `.xml` format. 
```
C:\Users\shweata\ethics_statement_corpus_1000\results>amidict -v --dictionary ethics_statement --directory rake --input rake/keywords.txt create --informat list --outformats xml,html
```
The prototype dictionary is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/results/rake/ethics_statement.xml). 

## 3. Tasks
Our next task would be:
-  to convert narrower terms into synonymns (as child) under an a broader entry term. 
-  add Wikidata Ids and Wikipedia links to entries, wherever applicable. 
-  refine our initial query used to create the mini-corpus, to reduce the false-positives.

## 4. Update from 2021-05-04 meeting:
- We have added the dictionary terms as lexemes to Wikidata
- Our next focus would be to retrieve the Ethics Committees involved in the approval process. -> Named entity recognition
- Find more interesting terms related to Ethics Statement using TF-IDF

## 5. Entity Recognition using spaCy
The [notebook I've written](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/Ethics_Statement_Entity_Recognition.ipynb) does Entity Recogintion with which I've been able to pull out names of Ethics Committee. 
- I manually scrapped roughly 20 Ethics_Statements from a corpus on clinical trials and used spaCY for entity recognition. It is still a prototype, and I hope to extend it to a lot more papers. 
- I have not used any models to do named entity recognition. ML would be useful in this case. 

