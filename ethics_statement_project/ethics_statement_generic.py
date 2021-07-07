import os


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
        OUTPUT = 'e_cancer_trial_30'
        self.create_project_and_make_csv(
            working_directory, QUERY, HITS, OUTPUT)

    def test_term_creation(self, working_directory, QUERY, HITS, OUTPUT, TERMS_XML_PATH):
        """

        :param working_directory: 
        :param HITS: 
        :param TERMS_XML_PATH:
        :param QUERY:
        :param OUTPUT:

        """
        import os
        #self.create_project_files(QUERY, HITS, OUTPUT)
        # self.install_ami()
        dict_with_parsed_xml = self.make_dict_with_pmcids(
            working_directory, OUTPUT)
        terms = self.get_terms_from_ami_xml(TERMS_XML_PATH)
        self.add_ethic_statements_to_dict(dict_with_parsed_xml)
        self.add_if_file_contains_terms(
            terms=terms, dict_with_parsed_xml=dict_with_parsed_xml)
        self.remove_tems_which_have_false_terms(
            dict_with_parsed_xml=dict_with_parsed_xml)
        self.convert_dict_to_csv(
            path=f'{OUTPUT}_19091212.csv', dict_with_parsed_xml=dict_with_parsed_xml)

    def frontiers_ethics_statement(self):
        """ """

        import os
        working_directory = os.getcwd()
        QUERY = "(METHODS:'stem cell') AND ethics statement AND frontiers"
        HITS = 1000
        OUTPUT = 'ethics_statement_frontiers_1000'
        self.create_project_and_make_csv(
            working_directory, QUERY, HITS, OUTPUT)

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
        dict_with_parsed_xml = self.make_dict_with_pmcids(
            working_directory, OUTPUT)
        self.add_ethic_statements_to_dict(dict_with_parsed_xml)
        self.convert_dict_to_csv(
            path=f'{OUTPUT}_spacy.csv', dict_with_parsed_xml=dict_with_parsed_xml)

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
        all_paragraphs = glob(os.path.join(
            working_directory, output, '*', 'sections', '**', '[1_9]_p.xml'), recursive=True)
        for statement in all_paragraphs:
            self.find_pmcid_from_file_name_and_make_dict_key(
                dict_with_parsed_xml, statement)
        logging.info(f"Found {len(dict_with_parsed_xml)} ethics statements")
        return dict_with_parsed_xml

    def find_pmcid_from_file_name_and_make_dict_key(self, dict_with_parsed_xml, paragraph_file):
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
        #os.system('pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_sm-0.4.0.tar.gz')
        nlp = spacy.load("en_core_web_sm")
        #nlp = spacy.load("en_core_sci_sm")
        import xml.etree.ElementTree as ET
        for ethics_statement in dict_with_parsed_xml:
            tree = ET.parse(ethics_statement)
            root = tree.getroot()
            self.iterate_over_xml_and_populate_dict(
                dict_with_parsed_xml, ethics_statement, nlp, root)

    def add_if_file_contains_terms(self, terms, dict_with_parsed_xml):
        """

        :param terms: 
        :param dict_with_parsed_xml:

        """
        for statement in dict_with_parsed_xml:
            dict_with_parsed_xml[statement]['has_terms'] = False
            for term in terms:
                if term in dict_with_parsed_xml[statement]['parsed']:
                    dict_with_parsed_xml[statement]['has_terms'] = term
                    break

    def get_terms_from_ami_xml(self, xml_path):
        """

        :param xml_path:

        """
        import xml.etree.ElementTree as ET
        tree = ET.parse(xml_path)
        root = tree.getroot()
        terms = []
        for para in root.iter('entry'):
            terms.append(para.attrib["term"])
        return terms

    def iterate_over_xml_and_populate_dict(self, dict_with_parsed_xml, ethics_statement, nlp, root):
        """

        :param dict_with_parsed_xml: 
        :param ethics_statement:
        :param nlp:
        :param root:

        """
        import xml.etree.ElementTree as ET
        from bs4 import BeautifulSoup
        try:
            xmlstr = ET.tostring(root, encoding='utf8', method='xml')
            print(xmlstr)
            soup = BeautifulSoup(xmlstr)
            text = soup.get_text()
            print(text)
            dict_with_parsed_xml[ethics_statement]['parsed'] = text
        except:
            dict_with_parsed_xml[ethics_statement]['parsed'] = "empty"
        doc = nlp(dict_with_parsed_xml[ethics_statement]['parsed'])
        entities, labels, position_end, position_start = self.make_required_lists()
        for ent in doc.ents:
            self.add_parsed_entities_to_lists(
                entities, labels, position_end, position_start, ent)
        self.add_lists_to_dict(dict_with_parsed_xml, entities, ethics_statement, labels, position_end,
                               position_start)

    def make_required_lists(self):
        """ """
        entities = []
        labels = []
        position_start = []
        position_end = []
        return entities, labels, position_end, position_start

    def add_lists_to_dict(self, dict_with_parsed_xml, entities, ethics_statement, labels, position_end, position_start):
        """

        :param dict_with_parsed_xml: 
        :param position_end: 
        :param position_start:
        :param entities:
        :param ethics_statement:
        :param labels:

        """
        dict_with_parsed_xml[ethics_statement]['entities'] = entities
        dict_with_parsed_xml[ethics_statement]['labels'] = labels
        dict_with_parsed_xml[ethics_statement]['position_start'] = position_start
        dict_with_parsed_xml[ethics_statement]['position_end'] = position_end

    def add_parsed_entities_to_lists(self, entities, labels, position_end, position_start, ent=None):
        """

        :param ent: 
        :param labels: 
        :param position_end: 
        :param entities:
        :param position_start:

        """
        if ent:
            entities.append(ent)
            labels.append(ent.label_)
            position_start.append(ent.start_char)
            position_end.append(ent.end_char)
        else:
            entities.append("empty")
            labels.append("empty")
            position_start.append("empty")
            position_end.append("empty")

    def convert_dict_to_csv(self, path, dict_with_parsed_xml):
        """

        :param path:
        :param dict_with_parsed_xml:

        """
        import logging
        import pandas as pd
        df = pd.DataFrame(dict_with_parsed_xml)
        df = df.T
        df.to_csv(path, encoding='utf-8')
        logging.info(f"wrote output to {path}")

    def remove_tems_which_have_false_terms(self, dict_with_parsed_xml):
        statement_to_pop = []
        for statement in dict_with_parsed_xml:
            if dict_with_parsed_xml[statement]['has_terms'] == False:
                statement_to_pop.append(statement)
                print(f"term not found for {statement}")

        for term in statement_to_pop:
            dict_with_parsed_xml.pop(term)


ethic_statement_creator = EthicStatements()
# ethic_statement_creator.demo()
ethic_statement_creator.test_term_creation(os.getcwd(), 'e_cancer_clinical_trial_50', 30, 'e_cancer_clinical_trial_50', os.path.join(
    os.getcwd(), 'results', 'rake', 'ethics_statement.xml'))
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

'''
Credits to Ayush Garg for helping with linking PMC to the parsed text and the entities recognized.
He has also converted the code into a class.
'''
