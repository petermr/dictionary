import json


class getpapersall:
    def __init__(self, **kwargs):
        pass

    def makequery(self, headers, payload):
        import xmltodict
        import requests
        print("*/Making the Request to get all hits*/")

        r = requests.post(
            'https://www.ebi.ac.uk/europepmc/webservices/rest/searchPOST', data=payload, headers=headers)
        print("*/Got the Content*/")

        return xmltodict.parse(r.content)

    def buildquery(self, cursormark, pageSize, query, synonym=True,):
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        payload = {'query': query, 'format': format, 'resultType': 'core',
                   'cursorMark': cursormark, 'pageSize': pageSize, 'synonym': synonym, 'format': 'xml', 'sort_PMCID': 'y'}
        print("*/Building the Query*/")
        return {'headers': headers, 'payload': payload}

    def europepmc(self, size, query, synonym=True, externalfile=True, fulltext=True):
        import requests
        import xmltodict
        import lxml.etree
        import lxml
        import os
        size = int(size)
        # change synonym to no otherwise yes is the default
        # The code regarding the size of the query currently only works till 100 terms. This is on purpose and I will add Function to access next cursormark which is basically next page of the resultant of the query once I have enough permision and knowledge
        if size <= 1000:
            queryparams = self.buildquery(
                '*', size, query, synonym=synonym)
            builtquery = self.makequery(
                queryparams['headers'], queryparams['payload'])

            content = []

            content.append(builtquery)

            return content
        if size > 1000:
            q = size//1000
            r = size % 1000
            i = 0
            nextCursorMark = []
            content = []
            for i in range(q):
                if i == 0:
                    queryparams = self.buildquery(
                        '*', q, query, synonym=synonym)
                    builtquery = self.makequery(
                        queryparams['headers'], queryparams['payload'])
                    nextCursorMark.append(
                        builtquery["responseWrapper"]["nextCursorMark"])
                    content.append(builtquery)
                else:
                    queryparams = self.buildquery(
                        nextCursorMark[-1], 1000, query, synonym=synonym)
                    builtquery = self.makequery(
                        queryparams['headers'], queryparams['payload'])

                    nextCursorMark.append(
                        builtquery["responseWrapper"]["nextCursorMark"])
                    content.append(builtquery)
            if r > 0:
                queryparams = self.buildquery(
                    nextCursorMark[-1], r, query, synonym=synonym)
                builtquery = self.makequery(
                    queryparams['headers'], queryparams['payload'])
                xmlschema_doc = lxml.etree.XML(builtquery)
                cursor = xmlschema_doc.xpath('//nextCursorMark')
                nextCursorMark.append(
                    builtquery["responseWrapper"]["nextCursorMark"])
                content.append(builtquery)
        return content

    # this is the function that will the the result from search and will download and save the files.
    def makecsv(self, searchvariable):
        import pandas_read_xml as pdx
        import xmltodict
        import pandas as pd
        import lxml.etree
        import json
        import pickle

        resultantdict = {}
        an = -1
        for papers in searchvariable:
            an += 1

            output_dict = json.loads(json.dumps(papers))

            for i in output_dict["responseWrapper"]["resultList"]["result"]:
                an += 1
                print("Reading Dictionary for paper", an)
                if i["isOpenAccess"] == 'Y' and "pmcid" in i:
                    pdfurl = []
                    htmlurl = []
                    for x in i["fullTextUrlList"]["fullTextUrl"]:
                        if x["documentStyle"] == "pdf" and x["availability"] == "Open access":
                            pdfurl.append(x["url"])

                        if x["documentStyle"] == "html" and x["availability"] == "Open access":
                            htmlurl.append(x["url"])
                    resultantdict[i["pmcid"]] = {}
                    resultantdict[i["pmcid"]]["htmllinks"] = htmlurl
                    resultantdict[i["pmcid"]]["pdflinks"] = pdfurl
                    try:
                        resultantdict[i["pmcid"]
                                      ]["journaltitle"] = i["journalInfo"]
                    except:
                        print("journalInfo not found for paper", an)
                    try:
                        resultantdict[i["pmcid"]
                                      ]["authorinfo"] = i["authorList"]
                    except:
                        print("Author list not found for paper", an)
                    try:
                        resultantdict[i["pmcid"]]["title"] = i["title"]
                    except:
                        print("Title not found for paper", an)
                    resultantdict[i["pmcid"]]["downloaded"] = False
                    print('Wrote the important Attrutes to a dictionary')

        with open('europe_pmc.pickle', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            print('Wrote the pickle to memory')

            pickle.dump(resultantdict, f, pickle.HIGHEST_PROTOCOL)
        return resultantdict

    def getxml(self, pmcid):
        import requests
        print("*/Making the Request to get full text xml*/")

        r = requests.get(
            f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML")
        print("*/Done*/")

        return r.content

    def getsupplementaryfiles(self, pmcid):
        import requests
        r = requests.get(
            f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/supplementaryFiles")
        return r

    def makexmlfiles(self, finalxmldict):
        import requests
        import lxml.etree
        import lxml
        import pickle
        import os
        print("*/Writing the xml papers to memory*/")
        papernumber = 0
        for paper in finalxmldict:
            papernumber += 1
            if finalxmldict[paper]["downloaded"] == False:
                pmcid = paper
                tree = self.getxml(pmcid)
                if not os.path.isdir(os.path.join(str(os.getcwd()), 'papers', pmcid)):
                    os.makedirs(os.path.join(
                        str(os.getcwd()), 'papers', pmcid))
                    with open(os.path.join(
                            str(os.getcwd()), 'papers', pmcid, f"{pmcid}.xml"), 'wb') as f:
                        f.write(tree)
                    print(f"*/Wrote the xml paper {papernumber}*/")

                    finalxmldict[paper]["downloaded"] = True
                    with open(os.path.join(
                            str(os.getcwd()), 'papers', pmcid, f"{pmcid}.pickle"), 'wb') as f:
                        pickle.dump(finalxmldict[paper],
                                    f, pickle.HIGHEST_PROTOCOL)

                else:
                    with open(os.path.join(
                            str(os.getcwd()), 'papers', pmcid, f"{pmcid}.xml"), 'wb') as f:
                        f.write(tree)
                    print(f"*/Wrote the xml paper {papernumber}*/")

                    finalxmldict[paper]["downloaded"] = True
                    with open(os.path.join(
                            str(os.getcwd()), 'papers', pmcid, f"{pmcid}.pickle"), 'wb') as f:
                        pickle.dump(finalxmldict[paper],
                                    f, pickle.HIGHEST_PROTOCOL)

                with open('europe_pmc.pickle', 'wb') as f:
                    pickle.dump(finalxmldict, f, pickle.HIGHEST_PROTOCOL)
                print(f"*/Updating the pickle*/")

    def readpickleddata(self, path):
        import pandas as pd
        object = pd.read_pickle(f'{path}')
        return object


a = getpapersall()
b = a.europepmc(2000, "ai")
c = a.makecsv(b)
a.makexmlfiles(c)
