from glob import glob
import os
ethics_statements = glob(os.path.join(
    os.getcwd(), 'ethics_statement_frontiers_100', 'PMC*', 'sections', '**', '[1_9]_p.xml'), recursive=True)
print(ethics_statements)
