import os
import pandas as pd
import pathlib
import re
from glob import glob
import xml.etree.ElementTree as ET
import spacy 
from spacy import displacy

HOME= 'C:/Users/shweata/dictionary/ethics_statement_project'

#!pip install git+git://github.com/petermr/pygetpapers
QUERY = "ethics statement frontiers"
HITS = 10
OUTPUT = 'ethics_statement_frontiers_10'


import os
#os.system(f'cmd /k "pygetpapers -q "{QUERY}" -k {HITS} -o {OUTPUT} -x"')
#https://datatofish.com/command-prompt-python/

#!git clone https://github.com/petermr/ami3.git
#!cd ami3
#!mvn install -Dmaven.test.skip=true
#os.system(f'cmd /k "ami -p {OUTPUT} section"')


ethics_statements = glob(os.path.join(HOME, OUTPUT, 'PMC*', 'sections','*', '[0-9]_ethic*', '[1_9]_p.xml'))
print(ethics_statements)

file1 = open(f'{OUTPUT}.txt', "w+", encoding='utf-8')

for file in ethics_statements:
    tree = ET.parse(file)
    root = tree.getroot()
    for para in root.iter('p'):
        #file1.write('para.text')
        print (para.text, file = file1)

text = pathlib.Path(f"{OUTPUT}.txt").read_text(encoding='utf-8')

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
#entities_html = displacy.render(doc, style="ent", page=True)
displacy.serve(doc, style="ent")

entities = []
labels = []
position_start = []
position_end = []


for ent in doc.ents:
    entities.append(ent)
    labels.append(ent.label_)
    position_start.append(ent.start_char)
    position_end.append(ent.end_char)

#displacy.serve(doc, style="ent")
    
df = pd.DataFrame({'Entities':entities,'Labels':labels,'Position_Start':position_start, 'Position_End':position_end})
#pd.set_option("display.max_rows", None, "display.max_columns", None)
df.to_csv(f'{OUTPUT}_labelled_entities.csv', encoding='utf-8')
