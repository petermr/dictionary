import os


class EthicStatements:
    """ """

    def __init__(self):
        pass

    def demo(self):
        """ """
        import os
        working_directory = os.getcwd()
        QUERY = "ethics statement frontiers"
        HITS = 10
        OUTPUT = 'ethics_statement_frontiers_100'
        self.create_project_and_make_csv(
            working_directory, QUERY, HITS, OUTPUT)

    def test_term_creation(self, working_directory, QUERY, HITS, OUTPUT, TERMS_XML_PATH):
        import os
        self.create_project_files(QUERY, HITS, OUTPUT)
        # self.install_ami()
        dict_with_parsed_xml = self.make_dict_with_pmcids(
            working_directory, OUTPUT)
        terms = self.get_terms_from_ami_xml(TERMS_XML_PATH)
        self.add_if_file_contains_terms(
            terms=terms, dict_with_parsed_xml=dict_with_parsed_xml)
        self.add_ethic_statements_to_dict(dict_with_parsed_xml)
        self.convert_dict_to_csv(
            path=f'{OUTPUT}.csv', dict_with_parsed_xml=dict_with_parsed_xml)

    def create_project_and_make_csv(self, working_directory, QUERY, HITS, OUTPUT):
        """

        :param working_directory: 
        :param QUERY: 
        :param HITS: 
        :param OUTPUT: 

        """
        import os
        self.create_project_files(QUERY, HITS, OUTPUT)
        self.install_ami()
        dict_with_parsed_xml = self.make_dict_with_pmcids(
            working_directory, OUTPUT)
        self.add_ethic_statements_to_dict(dict_with_parsed_xml)
        self.convert_dict_to_csv(
            path=f'{OUTPUT}.csv', dict_with_parsed_xml=dict_with_parsed_xml)

    def create_project_files(self, QUERY, HITS, OUTPUT):
        """

        :param QUERY: param HITS:
        :param OUTPUT: param HITS:
        :param HITS: 

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

        :param working_directory: param output:
        :param output: 

        """
        import os
        from glob import glob
        dict_with_parsed_xml = {}
        ethics_statements = glob(os.path.join(
            working_directory, output, 'PMC*', 'sections', '*', '*', '[1_9]_p.xml'))
        for statement in ethics_statements:
            self.find_pmcid_from_file_name_and_make_dict_key(
                dict_with_parsed_xml, statement)
        return dict_with_parsed_xml

    def find_pmcid_from_file_name_and_make_dict_key(self, dict_with_parsed_xml, statement):
        """

        :param dict_with_parsed_xml: param statement:
        :param statement: 

        """
        for word in statement.split('\\'):
            if word.startswith('PMC'):
                pmcid = word
                dict_with_parsed_xml[pmcid] = {}
                dict_with_parsed_xml[pmcid]['file'] = statement

    def add_ethic_statements_to_dict(self, dict_with_parsed_xml):
        """

        :param dict_with_parsed_xml: 

        """
        import spacy
        nlp = spacy.load("en_core_web_sm")
        import xml.etree.ElementTree as ET
        for ethics_statement in dict_with_parsed_xml:
            tree = ET.parse(dict_with_parsed_xml[ethics_statement]['file'])
            root = tree.getroot()
            self.iterate_over_xml_and_populate_dict(
                dict_with_parsed_xml, ethics_statement, nlp, root)

    def add_if_file_contains_terms(terms, dict_with_parsed_xml):
        for statement in dict_with_parsed_xml:
            dict_with_parsed_xml[statement]['has_terms'] = False
            for term in terms:
                if dict_with_parsed_xml[statement]['parsed'] == term:
                    dict_with_parsed_xml[statement]['has_terms'] = True
                    break

    def get_terms_from_ami_xml(xml_path):
        import xml.etree.ElementTree as ET
        tree = ET.parse(xml_path)
        root = tree.getroot()
        terms = []
        for para in root.iter('entry'):
            terms.append(para.attrib["term"])
        return terms

    def iterate_over_xml_and_populate_dict(self, dict_with_parsed_xml, ethics_statement, nlp, root):
        """

        :param dict_with_parsed_xml: param ethics_statement:
        :param nlp: param root:
        :param ethics_statement: 
        :param root: 

        """
        for para in root.iter('p'):
            dict_with_parsed_xml[ethics_statement]['parsed'] = para.text
            doc = nlp(dict_with_parsed_xml[ethics_statement]['parsed'])
            entities, labels, position_end, position_start = self.make_required_lists()
            for ent in doc.ents:
                self.add_parsed_entities_to_lists(
                    ent, entities, labels, position_end, position_start)
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

        :param dict_with_parsed_xml: param entities:
        :param ethics_statement: param labels:
        :param position_end: param position_start:
        :param entities: 
        :param labels: 
        :param position_start: 

        """
        dict_with_parsed_xml[ethics_statement]['entities'] = entities
        dict_with_parsed_xml[ethics_statement]['labels'] = labels
        dict_with_parsed_xml[ethics_statement]['position_start'] = position_start
        dict_with_parsed_xml[ethics_statement]['position_end'] = position_end

    def add_parsed_entities_to_lists(self, ent, entities, labels, position_end, position_start):
        """

        :param ent: param entities:
        :param labels: param position_end:
        :param position_start: 
        :param entities: 
        :param position_end: 

        """
        entities.append(ent)
        labels.append(ent.label_)
        position_start.append(ent.start_char)
        position_end.append(ent.end_char)

    def convert_dict_to_csv(self, path, dict_with_parsed_xml):
        """

        :param path: param dict_with_parsed_xml:
        :param dict_with_parsed_xml: 

        """
        import pandas as pd
        df = pd.DataFrame(dict_with_parsed_xml)
        df = df.T
        df.to_csv(path, encoding='utf-8')


ethic_statement_creator = EthicStatements()
# ethic_statement_creator.demo()
ethic_statement_creator.test_term_creation(
    "term_creation_test_cancer_clinal", "Cancer clinical trial", 50, os.getcwd(), "D:\main_projects\\repositories\dictionary\ethics_statement_project\\results\\rake\ethics_statement.xml")
#

# displacy.serve(doc, style="ent")

# displacy.serve(doc, style="ent")
# https://datatofish.com/command-prompt-python/

'''

def display_graph_of_dependensies(self, dict_with_parsed_xml):
    for ethic in display_graph_of_dependensies:
        doc = nlp(display_graph_of_dependensies[ethic]['parsed'])
        displacy.serve(doc, style="dep")

'''
