class EthicStatements:
    """ """

    def __init__(self):
        pass

    def demo(self):
        """ """
        import os
        path_to_project = os.getcwd()
        QUERY = "ethics statement springer nature"
        HITS = 100
        OUTPUT = 'ethics_statement_frontiers_springer_nature_100'
        self.create_project_and_make_csv(path_to_project,QUERY,HITS,OUTPUT)
    
    def frontiers_ethics_statement(self):
   
        import os
        path_to_project = os.getcwd()
        QUERY = "(METHODS:'stem cell') AND ethics statement AND frontiers"
        HITS = 20
        OUTPUT = 'ethics_statement_frontiers_2_20'
        self.create_project_and_make_csv(path_to_project,QUERY,HITS,OUTPUT)

    def create_project_and_make_csv(self,path_to_project,QUERY,HITS,OUTPUT):
        """

        :param path_to_project: 
        :param QUERY: 
        :param HITS: 
        :param OUTPUT: 

        """
        import os
        #self.create_project_files(QUERY,HITS,OUTPUT)
        #self.install_ami()
        dict_with_parsed_xml=self.make_dict_with_pmcids(path_to_project,OUTPUT)
        self.add_ethic_statements_to_dict(dict_with_parsed_xml)
        self.convert_dict_to_csv(path=f'{OUTPUT}_spacy.csv', dict_with_parsed_xml=dict_with_parsed_xml)

    def create_project_files(self,QUERY,HITS,OUTPUT):
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


    def make_dict_with_pmcids(self,path_to_project, output):
        """

        :param path_to_project: param output:
        :param output: 

        """
        import os
        from glob import glob
        import logging
        dict_with_parsed_xml = {}
        ethics_statements = glob(os.path.join(
            path_to_project, output, 'PMC*', 'sections', '*', '[0-9]_ethic*', '[1_9]_p.xml'))
        logging.basicConfig(level=logging.INFO)
        logging.info(ethics_statements)
        for statement in ethics_statements:
            self.find_pmcid_from_file_name_and_make_dict_key(dict_with_parsed_xml, statement)
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

    def add_ethic_statements_to_dict(self,dict_with_parsed_xml):
        """

        :param dict_with_parsed_xml: 

        """
        import spacy 
        nlp = spacy.load("en_core_web_sm")
        #nlp = spacy.load("en_core_sci_sm")
        import xml.etree.ElementTree as ET
        for ethics_statement in dict_with_parsed_xml:
            tree = ET.parse(dict_with_parsed_xml[ethics_statement]['file'])
            root = tree.getroot()
            self.iterate_over_xml_and_populate_dict(dict_with_parsed_xml, ethics_statement, nlp, root)

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
                self.add_parsed_entities_to_lists(ent, entities, labels, position_end, position_start)
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

    def convert_dict_to_csv(self,path,dict_with_parsed_xml):
        """

        :param path: param dict_with_parsed_xml:
        :param dict_with_parsed_xml: 

        """
        import logging
        import pandas as pd
        df = pd.DataFrame(dict_with_parsed_xml)
        df = df.T
        df.to_csv(path, encoding='utf-8')
        logging.basicConfig(level=logging.INFO)
        logging.info("wrote output to csv")
        


ethic_statement_creator=EthicStatements()
#ethic_statement_creator.demo()
ethic_statement_creator.frontiers_ethics_statement()



# displacy.serve(doc, style="ent")

# displacy.serve(doc, style="ent")
# https://datatofish.com/command-prompt-python/

'''

def display_graph_of_dependensies(self, dict_with_parsed_xml):
    for ethic in display_graph_of_dependensies:
        doc = nlp(display_graph_of_dependensies[ethic]['parsed'])
        displacy.serve(doc, style="dep")

'''

'''
Credits to Ayush Garg for helping with linking PMC to the parsed text and the entities recognized. 
He has also converted the code into a class. 
'''