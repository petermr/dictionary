# wikimedia functions .wikimedia.py
"""
collection of existing Python tools and Wikimedia/Data endpoints
"""
import os
import pandas as pd
import xml.etree.ElementTree as ET
from amidict import Resources

# SPARQL keywords
WIKIDATA_QUERY_URL = 'https://query.wikidata.org/sparql'
# query
FORMAT = 'format'
QUERY = 'query'
# parsing
XSD_DEC = "http://www.w3.org/2001/XMLSchema#decimal"
DATATYPE = "datatype"
TYPE = "type"
LITERAL = "literal"
URI = "uri"
VALUE = "value"
XML_LANG = "xml:lang"
HEAD = "head"
VARS = "vars"
BINDING = "binding"
BINDINGS = "bindings"
RESULT = "result"
RESULTS = "results"

#test query
TEST_QUERY = """
        SELECT 
          ?countryLabel ?population ?area 
#          ?medianIncome ?age
        WHERE {
          ?country wdt:P463 wd:Q458.
          OPTIONAL { ?country wdt:P1082 ?population }
          OPTIONAL { ?country wdt:P2046 ?area }
          OPTIONAL { ?country wdt:P3529 ?medianIncome }
          OPTIONAL { ?country wdt:P571 ?inception. 
            BIND(year(now()) - year(?inception) AS ?age)
          }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
#        LIMIT 3
        """
PYAMIDICT, RESOURCE_DIR, DICT202011, TEMP_DIR, DICTIONARY_TOP = Resources().get_resources()

class WikidataPedia():

    def __init__(self):
#        print("WP init")
        pass

    def help(self):
        print("help for Wikimedia routines NYI")

    def read_sparql_xml(self, file):
        """<?xml version='1.0' encoding='UTF-8'?>
<sparql xmlns='http://www.w3.org/2005/sparql-results#'>
	<head>
		<variable name='wikidata'/>
		...
		<variable name='term'/>
	</head>
	<results>
		<result>
			<binding name='wikidata'>
				<uri>http://www.wikidata.org/entity/Q889</uri>
			</binding>
			...
			<binding name='term'>
				<literal xml:lang='en'>Afghanistan</literal>
			</binding>
		</result>
"""
        print("read_sparql_xml")
        try:
            root = ET.parse(file).getroot()
        except:
            print("cannot parse XML", file)
            return None
        result_list = root.findall("./*/{http://www.w3.org/2005/sparql-results#}result")
        rowdata = []
        for i, result in enumerate(result_list):
            binding_list = result.findall("./{http://www.w3.org/2005/sparql-results#}binding")
            new_row_dict = {}
            for binding in binding_list:
                name = binding.attrib["name"]
                child = list(binding)[0]
                type_ = str(child.tag).partition("}")[2]
                val = child.text
                # there may be other types of output - don't know
                if type == "junk":
                    val = float(val)
                elif type_ == URI:
                    pass
                elif type_ == LITERAL:
                    pass
                else:
                    print("Cannot parse")
                new_row_dict[name] = val
            rowdata.append(new_row_dict)
        return pd.DataFrame(rowdata)



    def post_sparql(self, query, format="json"):
        """https://requests.readthedocs.io/en/master/ HTTP for humans"""
        return self.post_request(WIKIDATA_QUERY_URL, query, format)

    def post_request(self, url, query, format="json"):
        import requests
        if query is None or len(query) == 0:
            print("empty query")
            return
        req = requests.get(url, params={FORMAT: format, QUERY: query})
        print("req", req)
        return req.json()

    def test_query_wikipedia(self):
        """for experimenting"""
        import wikipedia as wp
        """# wikipedia search library (many functions)
        https://wikipedia.readthedocs.io/en/latest/code.html
        """
        print("Bear", wp.search("bear"))
        print("reality_summary", wp.summary("reality checkpoint"))
    #    print("pmr_page", wp.page(title="Peter Murray-Rust", preload=True))
        page = wp.WikipediaPage(title="Chaffinch", preload=True)
        print("categories", page.categories,
## these are quite large
#              "\n", "content", page.content,
    #          "\n", page.coordinates,
    #          "\n", "html", page.html,
    #          "\n", "images", page.images,
    #          "\n", "links", page.links
              )
        pass

    """https://janakiev.com/blog/wikidata-mayors/"""

    def submit_process_sparql(self, query):
        """
        submits query to wikidata and creates table of results.
        uses SPARQL SELECT-names as column-names

        *query* SPARQL query (assumed correct)

        return DataFrame (columns from SPARQL SELECT)
        """
        import pandas as pd

        wm = WikidataPedia();
        query_results_dict = wm.post_sparql(query)
        # results is a 2-element dictionary with keys = "head" and "results"
        # "head' dict with "vars" child dict as list of column names
        head_dict = query_results_dict[HEAD]
        colhead_array = head_dict[VARS]
        # second "results" with "bindings" child list of row dictionaries
        results_dict = query_results_dict[RESULTS]
        bindings = results_dict[BINDINGS]
        return self.create_data_frame_from_bindings(bindings, colhead_array)

    def create_data_frame_from_bindings(self, bindings, colhead_array):
        rowdata = []
        for row_dict in bindings:
            new_row_dict = {}
            for colhead in colhead_array:
                cell_dict = row_dict[colhead]
                datatype_ = cell_dict.get(DATATYPE, None)
                type_ = cell_dict.get(TYPE, None)
                # there may be other types of output - don't know
                if XSD_DEC == datatype_ and LITERAL == type_:
                    val = float(cell_dict.get(VALUE))
                elif type_ == LITERAL:
                    val = cell_dict.get(VALUE, None)
                else:
                    print("Cannot parse", cell_dict)
                new_row_dict[colhead] = val
            rowdata.append(new_row_dict)
        return pd.DataFrame(rowdata)


def main():
    """
    return
    """
    wm = WikidataPedia()
    wm.help()
    df = wm.submit_process_sparql(query=TEST_QUERY)
    print("df", df)
    xml = wm.read_sparql_xml(os.path.join(DICTIONARY_TOP, "openVirus202011/country/work/sparql_final_dict.xml"))
    print("xml", xml)
#    wm.test_query_wikipedia()
    print("end of wikipedia main")

#========================

if __name__ == "__main__":
    main()
else:
    main()

