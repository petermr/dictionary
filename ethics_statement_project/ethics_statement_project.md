**Table of Contents**
- [1. Motivation and Goals](#1-motivation-and-goals)
- [2. WikiProject Ethics](#2-wikiproject-ethics)
- [3. Test Mini-Corpora - Using `pygetpapers`](#3-test-mini-corpora---using-pygetpapers)
  - [3.1. Mini-Corpus #1](#31-mini-corpus-1)
  - [3.2. Mini-Corpus #2](#32-mini-corpus-2)
  - [3.3. Mini-Corpus #3](#33-mini-corpus-3)
  - [3.4. Mini-corpus #4](#34-mini-corpus-4)
  - [3.5. Mini-corpus #5](#35-mini-corpus-5)
- [4. `ami` dictionary - Ontology](#4-ami-dictionary---ontology)
- [5. Updates](#5-updates)
  - [5.1. Refactoring (20210714)](#51-refactoring-20210714)
  - [5.2. Phrase Match Implementation, Sentence splitter](#52-phrase-match-implementation-sentence-splitter)
  - [5.3. Semantic Model for Ethics Statement, Textacy, Mixed content problem with XML, Boiler Plate](#53-semantic-model-for-ethics-statement-textacy-mixed-content-problem-with-xml-boiler-plate)
  - [5.4. Code review with PMR and Ayush (20210630)](#54-code-review-with-pmr-and-ayush-20210630)
  - [5.5. Meeting on Tuesday (20210629)](#55-meeting-on-tuesday-20210629)
  - [5.6. Meeting on Sunday (20210627)](#56-meeting-on-sunday-20210627)
  - [5.7. Moving away from Jupyter Notebook, trying out different publishers (2021-06-23)](#57-moving-away-from-jupyter-notebook-trying-out-different-publishers-2021-06-23)
  - [5.8. Exploration on 2021-06-18](#58-exploration-on-2021-06-18)
  - [5.9. SPARQL Class (2021-06-16) - Potential Integration with ami](#59-sparql-class-2021-06-16---potential-integration-with-ami)
  - [5.10. Better globbing, Regex and SPARQL Wrapper (2021-06-15)](#510-better-globbing-regex-and-sparql-wrapper-2021-06-15)
  - [5.11. Entity Recognition using spaCy and NLTK with automatic scraping (2021-06-09)](#511-entity-recognition-using-spacy-and-nltk-with-automatic-scraping-2021-06-09)
  - [5.12. Entity Recognition using spaCy (2021-06-06)](#512-entity-recognition-using-spacy-2021-06-06)
  - [5.13. Ethics Statment Prototype dictionary (2021-06-01)](#513-ethics-statment-prototype-dictionary-2021-06-01)
- [6. Meeting Records](#6-meeting-records)
  - [6.1. 2021-07-15](#61-2021-07-15)
  - [6.2. 2021-07-08](#62-2021-07-08)
  - [6.3. 2021-07-01](#63-2021-07-01)
  - [6.4. 2021-06-24](#64-2021-06-24)
  - [6.5. 2021-06-17](#65-2021-06-17)
  - [6.6. 2021-06-10](#66-2021-06-10)
  - [6.7. 2021-06-03](#67-2021-06-03)
  - [6.8. 2021-05-27](#68-2021-05-27)
  - [6.9. 2021-05-20](#69-2021-05-20)
  - [6.10. 2021-05-10](#610-2021-05-10)
  - [6.11. 2021-05-07](#611-2021-05-07)
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

## 3.4. Mini-corpus #4 
To mine for Ethics Committees using `ethics_statement_generic.py`, I created a corpus of 600 papers from Frontiers publisher. The query I sent to EPMC using `pygetpapers`: 
```
"(METHODS:'stem cell') AND ethics statement AND frontiers"
```
- The `.csv` output can be found, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/ethics_statement_frontiers_1000_spacy.csv)
- Only the entities column can be found, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/ethics_committee_frontiers_spacy_entities_column.csv)

## 3.5. Mini-corpus #5 
To move away from publisher specifiicity and to have a smaller corpus, we have created a new corpus using the query:

```
(METHODS:'stem cell') AND (PUB_TYPE:'Clinical Trial')  AND (FIRST_PDATE:[2018-01-01 TO 2018-12-31])
```
It's about 170 papers big. 
Corpus is available [here](https://github.com/petermr/dictionary/tree/main/ethics_statement_project/stem_cell_2018)

# 4. `ami` dictionary - Ontology
I have created a prototype dictionary, after analysing the Ethics Statement sections of Mini-Corpus #1  by using phrase extraction feature of [`ami_gui.py`](https://github.com/petermr/openDiagram/blob/master/physchem/python/ami_gui.py). `ami` uses ([RAKE](https://pypi.org/project/rake-nltk/) to extract and weigh phrases from text. The selected phrases are automatically saved into `keywords.txt` file in the mini-corpus (C-Project) directory.  

I have hand-selected ~ 80 terms from my initial analysis. Using legacy `ami3`, I have converted the `.txt` file into a dictionary in `.xml` format. 
```
C:\Users\shweata\ethics_statement_corpus_1000\results>amidict -v --dictionary ethics_statement --directory rake --input rake/keywords.txt create --informat list --outformats xml,html
```
The prototype dictionary is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/results/rake/ethics_statement.xml). 

# 5. Updates
## 5.1. Refactoring (20210714)
- The code is currently being refactored with the help of Ayush and PMR.
- We are also moving to a new [Repo](https://github.com/petermr/docanalysis), and are packaging it up
- We will also work on documentation and logging. 
## 5.2. Phrase Match Implementation, Sentence splitter 
- Last Saturday (20210710), Ayush and Shweata implemented spaCy's phrase matcher, at a paragraph level as well as sentence level.
- An `ami` dictionary with boiler plate phrases are fed as matching terms to spaCy's phrase matcher
- The workflow has been modified slightly. A paragraph level phrase matchers filters out paragraphs that aren't ethics statements. 
- We, then, split the paragraph into sentences and run phrase matching again. This way we end up with only sentences which are relavant to ethics and useful for information extraction. 
- We also added logging and progress bar
-  On Monday's meeting Shweata and PMR experimented with the same workflow (with minor tweaks in globbing) on essential oil corpus. 
-  We looked if we could find the GPE where plant samples were collected
-   We created a methods section boilerplate dictionary, globbed the methods section and ran the script. 
-   Out of 100, we retrived 50 paragraphs and did Named-Entitry Recognition. There were some false positives. Overall, the results were promising. It also indicates that the workflow is generalizable with tweaks here and there.
-   The main task would be to document, generalize variable names and package the code and test. 
## 5.3. Semantic Model for Ethics Statement, Textacy, Mixed content problem with XML, Boiler Plate
- Shweata met up with Chaitanya on 20210701. He is incharge of:
  - Figuring out which is the best model to implement for key phrase extraction
  - Text similarity 
- PMR and Shweata met up on 20210703 to discuss feasibilities of ideas generated on 20210701's meeting. A detailed documentation is available,here. [The tagger idea](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/ethics_statement_tagger_idea.md)
  - We propose a semantic model for ethics statement, wherein each sentence has a structure and information type. 
  - We also realized that we should be working at sentence-level rather than paragraph-level. Ethics Statement are usually buried within a paragraph explaining the study design.
  - A specific tangible goal would be useful to have at this point to streamline our workflow. 
- Shweata has also looked at spaCy's sentence-splitter. spaCy also does text similarity which we might want to employ to find out similarities between a standard boiler plate and an ethics statement.
- Shweata has also created custom hand-made boiler plate ethics dictionary, which is available [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/ethics_dictionary/ethics_key_phrases/ethics_key_phrases.xml). She has implemented spaCy's `phrase matcher` with terms as phrases to match. Using spaCy's phrase matcher gives us a lot more functionality as we get to choose whether we would like to match only lowercase, and so on! Details [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/ethics_phrase_matcher_sentence_split.ipynb)
- We've also created a mini-corpora to work with sentence-level information extraction. Details, [here](#35-mini-corpus-5) 
- Shweata found a tool called `textacy` which she demonstrated during Tuesday's (20210706) coding session. There were other tools which team members discussed. [Here](https://github.com/petermr/CEVOpen/wiki/Coding-Sessions:-Meeting-Record#date-2021-07-07) is the notes from the session
- Daniel has created new organization on GitHub dedicated to Ethics Statement project.
- 20210707: Shweata has now got `textacy`'s topic modeling to work, thanks to PMR's help! The code is available here to look it. It is still a protoype, but we are able to extract information on different topics in ethics statements or any paragraphs. The code is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/testing_texacy_tutorial.ipynb).
- 20210707:Shweata discovered that, during XML parsing, the parapraphs were cut short due to the child elements between leading and trailing elements. Thanks to Ayush, the problem is now solved. We've implemented beautiful soup to parse. Writing to a `.csv ` became a problem because of `\n` character. But it's worked out now. The code is available [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/ethics_statement_generic.py).
- - ## PKE (20210701)
- PKE is a key phrase extraction Python toolkit. There are multiple models like TFIDF, Text Rank, Topic Rank, and so on. 
## 5.4. Code review with PMR and Ayush (20210630)
- Ayush and Shweata updated about their work on Ethics Statement. They have come up with a prototype to build a feedback loop of looking for ethics committees and key phrases in labelled sections and using them to filter unlabeled ethics statements. They also spent a huge chunk of time debugging their code. They had to re-think their logic of getting the dictionary key by splitting the path. This resulted in getting only the last paragraphs of each section - which was the problem. We resolved it by changing the dictionary key to the section of the path independent of the users working directory.
- In relation to Ethics Statement. Comments from PMR:
    - Linear workflow doesn't always work. As the project grows, it gets complex. There will be more looping and branching.
    - There are different levels that we are working with: Project -> CTree -> sections -> paragraphs -> sentences -> words. It's important, at each step, to know what you are working with.
    - KNIME: A tool to visualize workflow can be employed.
## 5.5. Meeting on Tuesday (20210629)
- Ayush and Shweata met up to code together. Thanks to Ayush's help in coding, we now extract the terms from `ami` ethics statement dictionary, and search the paragraph sections for those terms. 
- This would be very useful to retrieve non-labelled ethics statements, and build a feedback loop. 
## 5.6. Meeting on Sunday (20210627) 
- Shweata and PMR met up to discuss a  potenial workflow for the project. Based on the discussion, Shweata has come up with a prototype workflow. It can be found, [here]()
## 5.7. Moving away from Jupyter Notebook, trying out different publishers (2021-06-23)
[New script](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/ethics_statement_generic.py)
- I've moved away from Jupyter Notebook, for now. It was hard for me to move things around and make changes. 
- made the  code conformant and modular (huge thanks to @ayushgarg). Turned the code into a class. 
- linked PMC Id with the Named-entities in the Ethics Statement using nested dictionary. (Again, grategul to Ayush for helping me implement my ideas)
- Use of `scispacy` - to expand abbreviations(?)
  - I had troubles installing it. The problem was of 2-fold. First, I didn't have C++ downloaded in my system. Once, that was resolved I ran into a problem with Python version. Long story short, I had to downgrade Python on my machine from 3.9. to 3.8. , as one of the dependencies of `scispacy ` didn't support the latest python version. 
  - I'm yet to test out their models
- Building a Wordcloud using `nltk` and `wordcloud` package
- Trying out different publishers
  - springer nature doesn't have useful file naming system
  - PLOS doesn't label Ethics Statement either

## 5.8. Exploration on 2021-06-18
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
## 5.9. SPARQL Class (2021-06-16) - Potential Integration with ami
[SPARQL class](sparql.py)
- In today's CEVOpen coding session, we turned the wrapper to a class. 
- We also explored logging and automatic documentation using `pyment` package. 

## 5.10. Better globbing, Regex and SPARQL Wrapper (2021-06-15)
[New notebook](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/Ethics_staement_dictionary_globbing_annotation_shweata.ipynb)
- Noise in text was one of our main concerns. See the previous notebook to see what I mean. I noticed that Frontiers journal had explicit Ehtics Statement label and better structure. So, I decided to create a corpus of 100 papers from Frontiers journal. 
- After sectioning the paper, I glob the Ethics Statement section from each paper and dump all the statements to a txt file. 
- And as before, I use SpaCy to do Named Entity-Recognition. 
- I've also explored using Regular Expression to retrieve more information on Ethics Committee and whether an approval was required in the first place or not. 
- We also would want to do a supervised search using `pyami` on these Ethics Statement. For that, we would like to query Wikidata and retrieve, let's say, Research Councils or Universitites. We (Peter and I) have a prototype implementation of SPARQLWrapper which queries Wikidata and returns SPARQL endpoint in XML format. We can, potentially, turn the enpoint into an `ami` dictionary. 
- Needs better documentation

## 5.11. Entity Recognition using spaCy and NLTK with automatic scraping (2021-06-09)
  I have now created a [new notebook](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/Ethics_statement_project_scraping_txt_file_containing_ethics.ipynb) which,
-  globs sections of papers in CProject with the word 'ethic' in it.
-  writes the paragraphs in the globbed section to a [`.txt`](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/ethics_statement_clinical_trial_50.txt) file.
-  does Named Entity-Recognition using spaCy
-  The entities with ORG label retrieves Ethics Committee names. 
@Daniel and @PMR: There is a lot of noise because I don't have control over which paragraphs I write. The spaCy model isn't accurate either. Any directions would be helpful. 
##  5.12. Entity Recognition using spaCy (2021-06-06)
The [notebook I've written](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/Ethics_Statement_Entity_Recognition_spacy.ipynb) does Entity Recognition with which I've been able to pull out names of Ethics Committee. 
- I manually scraped roughly 20 Ethics_Statements from a corpus on clinical trials and used spaCY for entity recognition. It is still a prototype, and I hope to extend it to a lot more papers. 
- I have not used any models to do named entity recognition. ML would be useful in this case. 
## 5.13. Ethics Statment Prototype dictionary (2021-06-01)
I have created a prototype dictionary after analysing the Ethics Statement section of Mini-Corpus #1 using [`ami_gui.py`](https://github.com/petermr/openDiagram/blob/master/physchem/python/ami_gui.py). It is available, [here](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/results/rake/ethics_statement.xml).
# 6. Meeting Records
## 6.1. 2021-07-15
- Shweata presented the sentence-level ethics committee extraction. 
- The ethics committees extracted will be put into Wikidata
- Possible directions:
    - Integrate with Wikidata - supervised search
    - Independent supervised searches using different dictionaries
    - Present the work in a Hackathon?
    - Extrapolate the workflow to Acknowledgements, Conflict of Interest, and so on
    - Write up the work
## 6.2. 2021-07-08
- Shweata presented updates in the meeting. It included XML mixed content problem, sentence splitting, phrase matcher, boiler plate dictionary, new standard corpus to work with, and so on. More in the updates section. 
- Immediate tasks outlined were:
  - Integrating with Wikidata
  - Making the structured information (i.e., names of ethics committees, and so on) easy for humans to feed to Wikidata
  - New rows for each organization in the `.csv`.
  - Weighing sentences based on the number of terms hit
- Daniel suggested that he would use Open Refine to feed the data to Wikidata. 
- Daniel has also set up a [new Repo](https://github.com/FAIR-ethics/PMC-ethics/wiki) for the project, and has set up a Wiki outlining the thematic and methodologic goals. 
## 6.3. 2021-07-01
[Workflow](https://github.com/petermr/dictionary/blob/main/ethics_statement_project/project_workflow.md)
- Shweata presented the prototype workflow for the project. You can look at the MD page for more information. Comments from Daniel and PMR: 
  - Think about integrating into Wikidata. Once we have the Ethics Committees, we might want to query Wikidata if it exists or not. 
  - We might want to have logfiles - which contains extracted information. 
  - It would be useful to have a blacklist - a stopwords list to weed out unnecessary noise
  - Since we have implemented filtering using terms in the dictionaries, we might want to score the retrieved paragraphs based on the number of terms hit. 
  - In the entities column of the `.csv`, it would be useful to have a deliminter other than a comma. -> `.tsv`(?)
  - Come up with boilers plates for ethics statements
  - Sentence-level similarity -> Score the sentences based on boiler plates
    - fish for entities
    - determining the contex
    - Similar to SPAM dectectors!
- Shweata, then, presented her initial work with PKE, a python key phrase extracting toolkit. She demonstrated multiple models that can be accessed through PKE to extract key phrases. Comments from Daniel and PMR:
  - Instead of relying on one approach, we could somehow combine these approaches to come up with useful set of terms. It could be by multiplying the scores we get out of each model. 
  - We could manually come up with boiler plate phrases, and then run it through, let's say, YAKE to come up with key phrases. 
  - It'd be useful to give more weight to longer phrases. 
- Useful questions to ask:
  -  What percentage have of ethics statements have an approval number? It might be useful to compare between two years. 
  -  WHO did WHAT to WHOM?
- Daniel will share a guide to ensure better reproducibility when using Jupyter Notebooks. 
- Main tasks:
  - Get away from publisher-specificity.
  - Boiler plates
  - Sentence level similarities
  - Experiment with key phrase extractions. 
- Identifying main subjects of papers. We could then determine whether if we want to look for ethics statements or not, and so on. 
## 6.4. 2021-06-24
- Shweata presented her updates on the code. Read more about it in the updates section dated 2021-06-23. 
- Daniel - Next step would be to feed the mined Ethics Committee names to Wikidata. 
- Shweata will commit the `.csv` to the project directory so that Daniel can pick it up and upload to Wikidata
- PMR demonstrated `pygetpapers`'s integration with crossref
- The project directory has become messy as it has grown gradually. We will have to refactor. 
- A potenial step would be to have a feedback loop between Wikidata and `ami`. 
An interative workflow:
Wikidata SPARQL (SPARQLWrapper) -> `amidict` -> `ami search`
Papers -> (Ethics Statements) -> Ethics Committees (using spaCy) -> Wikidata
- Here is a [query](https://w.wiki/3Y58) Daniel wrote to get us started.
- We might also want to look at crowdsourcing parts of the works that goes into the project - a mixture of automation and manual work
- Rule-based matching, regex or keyword searches are something to look at. 
- 
## 6.5. 2021-06-17
- Shweata presented an enhanced version of her previous Notebook. More information [here](#54-better-globbing-regex-and-sparql-wrapper-2021-06-15). 
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
## 6.6. 2021-06-10
- Shweata presented her initial work with entity recognition. Comments from Daniel and Peter. 
  - Use regex along with globing
  - Tfidf to weigh the terms
- There are two possible ways to go from here:
    - Human Annotation model - coming up with two sets of data, one with phrases which are most common in Ethics Statement and other which aren't. We can then build a model to extract named entities. 
    - Semantic Model - Coming up with a set of rules which we can use to extract named entities, approval numbers and so on.
- Explore Wikidata for research councils and universities. Here is a [query](https://w.wiki/3Tsu) Daniel wrote to begin with. By doing so, we might get a better gauge for what's there and what isn't. 
## 6.7. 2021-06-03
- We have added the dictionary terms as lexemes to Wikidata
- Our next focus would be to retrieve the Ethics Committees involved in the approval process. -> Named entity recognition
- Find more interesting terms related to Ethics Statement using TF-IDF.

## 6.8. 2021-05-27
- @Daniel: Exploring with Wikidata Lexemes and Ethics Statement
- Wikdata Game - You learn or Wikidata learns or both!
  - We can come up with a Wikidata game where we ask people whether a phrase - we extracted from `ami`using RAKE - is usually present in Ethics Statement or not.

## 6.9. 2021-05-20
- We need a way to automate the retrieval of the Ethics Statement. We could do sectioning and retrieve them. But it's harder because most papers don't have a dedicated Ethics Statement (usually buried in the methods section). So, we'll have to create a dictionary, using the phrase we've initially extracted, to help with information retrieval (i.e., get Ethics Statement paragraph from papers). (Q: How does SpaCY give those phrase ranks?)
- After getting, let's say, 1000 Ethics Statement, we can again try unsupervised or even supervised phrase extraction. We can refine our dictionaries and also start extracting hospital names, committee names and their identifiers, and so on.

## 6.10. 2021-05-10
- Build a dictionary manually with frequently used n-grams in Ethics Statements.

## 6.11. 2021-05-07
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
