import os
from tqdm import tqdm


class EthicStatements:
    """ """

    def __init__(self):
        import logging

        logging.basicConfig(level=logging.INFO)

    def demo(self):
        """ """
        import os

        working_directory = os.getcwd()
        QUERY = "ethics statement frontiers"
        HITS = 10
        OUTPUT = "e_cancer_trial_30"
        self.create_project_and_make_csv(working_directory, QUERY, HITS, OUTPUT)

    def test_term_creation(
        self, working_directory, QUERY, HITS, OUTPUT, TERMS_XML_PATH
    ):
        """

        :param working_directory:
        :param HITS:
        :param TERMS_XML_PATH:
        :param QUERY:
        :param OUTPUT:

        """
        import os

        # self.create_project_files(QUERY, HITS, OUTPUT)
        # self.install_ami()
        dict_with_parsed_xml = self.make_dict_with_pmcids(working_directory, OUTPUT)
        terms = self.get_terms_from_ami_xml(TERMS_XML_PATH)
        self.add_ethic_statements_to_dict(dict_with_parsed_xml)
        self.add_if_file_contains_terms(
            terms=terms, dict_with_parsed_xml=dict_with_parsed_xml
        )
        self.remove_tems_which_have_false_terms(
            dict_with_parsed_xml=dict_with_parsed_xml
        )
        self.sentence_based_phrase_matching(
            terms=terms, dict_with_parsed_xml=dict_with_parsed_xml
        )
        self.iterate_over_xml_and_populate_sentence_dict(
            dict_with_parsed_xml=dict_with_parsed_xml
        )

        self.convert_dict_to_csv(
            path=f"{OUTPUT}_20210707_4.csv", dict_with_parsed_xml=dict_with_parsed_xml
        )

    def frontiers_ethics_statement(self):
        """ """

        import os

        working_directory = os.getcwd()
        QUERY = "(METHODS:'stem cell') AND ethics statement AND frontiers"
        HITS = 1000
        OUTPUT = "ethics_statement_frontiers_1000"
        self.create_project_and_make_csv(working_directory, QUERY, HITS, OUTPUT)

    def create_project_and_make_csv(self, working_directory, QUERY, HITS, OUTPUT):
        """

        :param working_directory:
        :param QUERY:
        :param HITS:
        :param OUTPUT:

        """
        import os

        self.create_project_files(QUERY, HITS, OUTPUT)
        # self.install_ami()
        dict_with_parsed_xml = self.make_dict_with_pmcids(working_directory, OUTPUT)
        self.add_ethic_statements_to_dict(dict_with_parsed_xml)
        self.convert_dict_to_csv(
            path=f"{OUTPUT}_spacy.csv", dict_with_parsed_xml=dict_with_parsed_xml
        )

    def create_project_files(self, QUERY, HITS, OUTPUT):
        """

        :param QUERY:
        :param HITS:
        :param OUTPUT:

        """
        import os

        os.system(f'pygetpapers -q "{QUERY}" -k {HITS} -o {OUTPUT} -x')
        os.system(f"ami -p {OUTPUT} section")

    def install_ami(self):
        """ """
        import os

        os.system("git clone https://github.com/petermr/ami3.git")
        os.system("cd ami3")
        os.system("mvn install -Dmaven.test.skip=true")

    def make_dict_with_pmcids(self, working_directory, output):
        """

        :param working_directory:
        :param output:

        """
        import os
        from glob import glob
        import logging

        dict_with_parsed_xml = {}
        all_paragraphs = glob(
            os.path.join(
                working_directory, output, "*", "sections", "**", "[1_9]_p.xml"
            ),
            recursive=True,
        )
        for statement in tqdm(all_paragraphs):
            self.find_pmcid_from_file_name_and_make_dict_key(
                dict_with_parsed_xml, statement
            )
        logging.info(f"Found {len(dict_with_parsed_xml)} paragraphs")
        return dict_with_parsed_xml

    def find_pmcid_from_file_name_and_make_dict_key(
        self, dict_with_parsed_xml, paragraph_file
    ):
        """

        :param dict_with_parsed_xml:
        :param statement:

        """
        dict_with_parsed_xml[paragraph_file] = {}

    def add_ethic_statements_to_dict(self, dict_with_parsed_xml):
        """

        :param dict_with_parsed_xml:

        """
        import spacy
        import os

        # os.system('pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_sm-0.4.0.tar.gz')
        nlp = spacy.load("en_core_web_sm")
        # nlp = spacy.load("en_core_sci_sm")
        import xml.etree.ElementTree as ET

        for ethics_statement in tqdm(dict_with_parsed_xml):
            tree = ET.parse(ethics_statement)
            root = tree.getroot()
            self.iterate_over_xml_and_populate_dict(
                dict_with_parsed_xml, ethics_statement, nlp, root
            )

    def add_if_file_contains_terms(self, terms, dict_with_parsed_xml):
        """

        :param terms:
        :param dict_with_parsed_xml:

        """
        import spacy

        nlp = spacy.load("en_core_web_sm")
        from spacy.matcher import PhraseMatcher

        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp(text) for text in terms]
        matcher.add("TerminologyList", patterns)

        for statement in tqdm(dict_with_parsed_xml):
            matched_phrases = []
            dict_with_parsed_xml[statement]["has_terms"] = False
            dict_with_parsed_xml[statement]["weight"] = 0
            doc = nlp(dict_with_parsed_xml[statement]["parsed"])
            matches = matcher(doc)
            for match_id, start, end in matches:
                matched_span = doc[start:end]
                matched_phrases.append(matched_span.text)
                dict_with_parsed_xml[statement]["has_terms"] = matched_phrases
            dict_with_parsed_xml[statement]["weight"] = len(matched_phrases)

    def sentence_based_phrase_matching(self, terms, dict_with_parsed_xml):
        import spacy

        nlp = spacy.load("en_core_web_sm")
        from spacy.matcher import PhraseMatcher

        for statement in tqdm(dict_with_parsed_xml):
            sentences = self.split_in_sentences(
                dict_with_parsed_xml[statement]["parsed"]
            )

            matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
            patterns = [nlp(text) for text in terms]
            matcher.add("TerminologyList", patterns)
            dict_with_parsed_xml[statement]["sentence_dict"] = {}
            for sentence in tqdm(sentences):
                dict_with_parsed_xml[statement]["sentence_dict"][sentence] = {}
                matched_phrases = []
                doc = nlp(sentence)
                matches = matcher(doc)
                for match_id, start, end in matches:
                    matched_span = doc[start:end]
                    matched_phrases.append(matched_span.text)
                    dict_with_parsed_xml[statement]["sentence_dict"][sentence][
                        "matched_phrases"
                    ] = matched_phrases

    def split_in_sentences(self, text):
        import spacy

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        return [str(sent).strip() for sent in doc.sents]

    def get_terms_from_ami_xml(self, xml_path):
        """

        :param xml_path:

        """
        import xml.etree.ElementTree as ET

        tree = ET.parse(xml_path)
        root = tree.getroot()
        terms = []
        for para in root.iter("entry"):
            terms.append(para.attrib["term"])
        return terms

    def iterate_over_xml_and_populate_sentence_dict(self, dict_with_parsed_xml):
        import spacy

        nlp = spacy.load("en_core_web_sm")

        for ethics_statement in tqdm(dict_with_parsed_xml):
            for sentence in tqdm(
                dict_with_parsed_xml[ethics_statement]["sentence_dict"]
            ):
                doc = nlp(sentence)
                (
                    entities,
                    labels,
                    position_end,
                    position_start,
                ) = self.make_required_lists()
                for ent in doc.ents:
                    self.add_parsed_entities_to_lists(
                        entities, labels, position_end, position_start, ent
                    )
                self.add_lists_to_dict(
                    dict_with_parsed_xml[ethics_statement]["sentence_dict"][sentence],
                    entities,
                    labels,
                    position_end,
                    position_start,
                )

    def iterate_over_xml_and_populate_dict(
        self, dict_with_parsed_xml, ethics_statement, nlp, root
    ):
        """

        :param dict_with_parsed_xml:
        :param ethics_statement:
        :param nlp:
        :param root:

        """
        import xml.etree.ElementTree as ET
        from bs4 import BeautifulSoup

        try:
            xmlstr = ET.tostring(root, encoding="utf8", method="xml")
            soup = BeautifulSoup(xmlstr, features="lxml")
            text = soup.get_text(separator="")
            dict_with_parsed_xml[ethics_statement]["parsed"] = text.replace("\n", "")
        except:
            dict_with_parsed_xml[ethics_statement]["parsed"] = "empty"
        doc = nlp(dict_with_parsed_xml[ethics_statement]["parsed"])
        entities, labels, position_end, position_start = self.make_required_lists()
        for ent in doc.ents:
            self.add_parsed_entities_to_lists(
                entities, labels, position_end, position_start, ent
            )
        self.add_lists_to_dict(
            dict_with_parsed_xml[ethics_statement],
            entities,
            labels,
            position_end,
            position_start,
        )

    def make_required_lists(self):
        """ """
        entities = []
        labels = []
        position_start = []
        position_end = []
        return entities, labels, position_end, position_start

    def add_lists_to_dict(
        self,
        dict_to_add,
        entities,
        labels,
        position_end,
        position_start,
    ):
        """

        :param dict_with_parsed_xml:
        :param position_end:
        :param position_start:
        :param entities:
        :param ethics_statement:
        :param labels:

        """
        dict_to_add["entities"] = entities
        dict_to_add["labels"] = labels
        dict_to_add["position_start"] = position_start
        dict_to_add["position_end"] = position_end

    def add_parsed_entities_to_lists(
        self, entities, labels, position_end, position_start, ent=None
    ):
        """

        :param ent:
        :param labels:
        :param position_end:
        :param entities:
        :param position_start:

        """
        if ent.label_ == "ORG" or ent.label_ == "GPE":
            entities.append(ent)
            labels.append(ent.label_)
            position_start.append(ent.start_char)
            position_end.append(ent.end_char)

    def convert_dict_to_csv(self, path, dict_with_parsed_xml):
        """

        :param path:
        :param dict_with_parsed_xml:

        """
        import logging
        import pandas as pd

        df = pd.DataFrame(dict_with_parsed_xml)
        df = df.T
        df.sort_values(by=["weight"], ascending=False)
        df.to_csv(path, encoding="utf-8", line_terminator="\r\n")
        logging.info(f"wrote output to {path}")

    def remove_tems_which_have_false_terms(self, dict_with_parsed_xml):
        statement_to_pop = []
        for statement in dict_with_parsed_xml:
            if dict_with_parsed_xml[statement]["has_terms"] == False:
                statement_to_pop.append(statement)

        for term in statement_to_pop:
            dict_with_parsed_xml.pop(term)


ethic_statement_creator = EthicStatements()
# ethic_statement_creator.demo()
ethic_statement_creator.test_term_creation(
    os.getcwd(),
    "e_cancer_clinical_trial_50",
    30,
    "e_cancer_clinical_trial_50",
    os.path.join(
        os.getcwd(), "ethics_dictionary", "ethics_key_phrases", "ethics_key_phrases.xml"
    ),
)
#

# displacy.serve(doc, style="ent")

# displacy.serve(doc, style="ent")
# https://datatofish.com/command-prompt-python/

'''

def display_graph_of_dependensies(self, dict_with_parsed_xml):
    """

    :param dict_with_parsed_xml:

    """
    for ethic in display_graph_of_dependensies:
        doc = nlp(display_graph_of_dependensies[ethic]['parsed'])
        displacy.serve(doc, style="dep")

'''

"""
Credits to Ayush Garg for helping with linking PMC to the parsed text and the entities recognized.
He has also converted the code into a class.
"""
