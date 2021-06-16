from logging import debug


class Sparql:
    def __init__(self) -> None:
        from SPARQLWrapper import Wrapper
        self.sparql_wrapper = None
        self.format = Wrapper.XML #SPARQLWrapper default
        
    def create_sparql_wrapper(self, endpoint_url):
        """submits a sparql query to endpoint, returns results as XML

        Developed for Wikidata sparql endpoint. It should be generic.
        But it hasn't been tested on other endpoints.
        
        :param endpoint_url: Any sparql endpoint 
        :param query: SPARQL query as string
        :return: results in XML as defined by w3c(?)

        """
        import logging
        import sys
        from SPARQLWrapper import SPARQLWrapper
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        logging.debug("creating sparql wrapper")
        self.sparql_wrapper = SPARQLWrapper(endpoint_url, agent=user_agent)
        logging.debug("created sparql wrapper")


    def set_query(self):
        import logging
        logging.debug(f"running query {query}")
        self.sparql_wrapper.setQuery(query)
        
    
    def set_return_format(self, format):
        
        if format is None or format != "JSON":
            print("format defaults to XML")
        else:
            self.sparql_wrapper.setReturnFormat(format)
    
    def run_query(self):
        import logging
        from SPARQLWrapper import XML
        import SPARQLWrapper
        self.sparql_wrapper.setReturnFormat(XML)
        results = self.sparql_wrapper.query()
        if results is None:
            print("Query failed to return results")
        else: 
            # SPARQL wrapper returns an XML minidom object which we convert to an XML string
            if self.format is SPARQLWrapper.Wrapper.XML: 
                logging.debug(f"results {type(results)}")
                convert = results.convert()
                logging.debug(f"convert {type(convert)}")
                converted_xml = convert.toxml()
                logging.debug(f"xml {type(converted_xml)}")
            
        return results
        
    @classmethod
    def test_sparql(cls):
        """ """
        import SPARQLWrapper
        WIKIDATA_SPARQL_ENDPOINT_URL = "https://query.wikidata.org/sparql"
        #SPARQL query
        query = """#research council
        SELECT ?researchcouncil ?researchcouncilLabel 
        WHERE 
        {
        ?researchcouncil wdt:P31 wd:Q10498148.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }"""
        my_sparql = Sparql() 
        my_sparql.create_sparql_wrapper(WIKIDATA_SPARQL_ENDPOINT_URL)
        # my_sparql.set_return_format(SPARQLWrapper.Wrapper.JSON)
       
        results =  my_sparql.run_query()
        logging.debug(results[:5])

    @classmethod
    def submit_sparql_query(cls, endpoint_url, query):
        
        import sys
        import logging
        from SPARQLWrapper import SPARQLWrapper, XML
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(XML)
        results = sparql.query()
        logging.debug(f"results {type(results)}")
        convert = results.convert()
        logging.debug(f"convert {type(convert)}")
        converted_xml = convert.toxml()
        logging.debug(f"xml {type(converted_xml)}")

    @classmethod
    def test_integrated_query(cls):
        import logging
        WIKIDATA_SPARQL_ENDPOINT_URL = "https://query.wikidata.org/sparql"
        query = """#research council
    SELECT ?researchcouncil ?researchcouncilLabel 
    WHERE 
    {
    ?researchcouncil wdt:P31 wd:Q10498148.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }"""


        results = cls.submit_sparql_query(WIKIDATA_SPARQL_ENDPOINT_URL, query)
        if results is None:
            logging.warn("No results")
        else:
            logging.info(f"{len(results)} Characters returned")
            logging.debug(results[1:500])



    

def main(loglevel="info"):
    
    import logging
    levels = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warn': logging.WARNING,
            'warning': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG
        }
    level = levels.get(loglevel.lower())


    logging.basicConfig(
                level=level, format='%(levelname)s: %(message)s')


    logging.info("running test")
    Sparql.test_sparql()
    #Sparql.test_integrated_query()


if __name__ == "__main__":
    main(loglevel="debug")
    

