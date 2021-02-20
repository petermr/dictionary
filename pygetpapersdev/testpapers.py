class getpapersall:
    def __init__(self, **kwargs):
        import json

    def postquery(self, headers, payload):
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

    def webscrapepmc(self, query, sizeo,):
        from selenium import webdriver
        import time
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
        from selenium.webdriver.common.alert import Alert
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.chrome.options import Options
        from selenium import webdriver
        import chromedriver_autoinstaller

        chromedriver_autoinstaller.install()
        pmcdict = {}
        size = int(sizeo)

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-ssl-errors')

        webdriver = webdriver.Chrome(
            chrome_options=options
        )
        a = 0

        url = f'https://europepmc.org/search?query={query}%20%28IN_EPMC%3Ay%29%20AND%20%28OPEN_ACCESS%3Ay%29&page=1'

        webdriver.get(url)

        while len(pmcdict) <= size:
            time.sleep(2)
            # retrive url in headless browser
            # time.sleep(3)
            results = webdriver.find_elements_by_xpath(
                "//ul[@class='separated-list']/li/div/p[3]/span")
            for i in results:
                ahref = i.text
                pmcid = ahref
                if 'PMC' in pmcid:
                    a += 1
                    if len(pmcdict) < size:
                        print('Scraping paper no.', a)
                        name = pmcid.split()
                        pmcdict[name[-1]] = {}
                        pmcdict[name[-1]]["downloaded"] = False
                    else:
                        break
            if a < size:
                try:
                    webdriver.find_element_by_xpath(
                        "//span[contains(text(), 'Next')]").click()
                except:
                    print("Only found so many papers.")
                    webdriver.quit()

            else:
                webdriver.quit()

                break
            time.sleep(2)

        return dict(pmcdict)

    def europepmc(self, query, size, synonym=True, externalfile=True, fulltext=True):
        import requests
        import xmltodict
        import lxml.etree
        import lxml
        import os
        import json
        size = int(size)
        content = [[]]
        nextCursorMark = ['*', ]
        morepapers = True
        numberofpapersthere = 0
        numberofpages = 0
        # change synonym to no otherwise yes is the default
        # The code regarding the size of the query currently only works till 100 terms. This is on purpose and I will add Function to access next cursormark which is basically next page of the resultant of the query once I have enough permision and knowledge

        while numberofpapersthere <= size and morepapers == True:
            queryparams = self.buildquery(
                nextCursorMark[-1], 1000, query, synonym=synonym)
            builtquery = self.postquery(
                queryparams['headers'], queryparams['payload'])
            if "nextCursorMark" in builtquery["responseWrapper"]:
                nextCursorMark.append(
                    builtquery["responseWrapper"]["nextCursorMark"])
                output_dict = json.loads(json.dumps(builtquery))
                for i in output_dict["responseWrapper"]["resultList"]["result"]:
                    if "pmcid" in i:
                        if numberofpapersthere <= size:
                            content[0].append(i)
                            numberofpapersthere += 1

            else:
                morepapers = False
        if numberofpapersthere > size:

            content[0] = content[0][0:size]
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

            for i in output_dict:

                if "pmcid" in i:
                    an += 1
                    print("Reading Dictionary for paper", an)
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
        df = pd.DataFrame.from_dict(resultantdict,)
        df_transposed = df.T
        df_transposed.to_csv('europe_pmc.csv')
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
        import pandas as pd
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
                            str(os.getcwd()), 'papers', pmcid, "fulltext.xml"), 'wb') as f:
                        f.write(tree)
                    print(f"*/Wrote the xml paper {papernumber}*/")

                    finalxmldict[paper]["downloaded"] = True
                    with open(os.path.join(
                            str(os.getcwd()), 'papers', pmcid, "fulltext.xml"), 'wb') as f:
                        pickle.dump(finalxmldict[paper],
                                    f, pickle.HIGHEST_PROTOCOL)

                    df = pd.Series(finalxmldict[paper]).to_frame('ColumnName')
                    df.to_csv(os.path.join(
                        str(os.getcwd()), 'papers', pmcid, f"{pmcid}.pickle"))

                else:
                    with open(os.path.join(
                            str(os.getcwd()), 'papers', pmcid, "fulltext.xml"), 'wb') as f:
                        f.write(tree)
                    print(f"*/Wrote the xml paper {papernumber}*/")

                    finalxmldict[paper]["downloaded"] = True
                    with open(os.path.join(
                            str(os.getcwd()), 'papers', pmcid, "fulltext.xml"), 'wb') as f:
                        pickle.dump(finalxmldict[paper],
                                    f, pickle.HIGHEST_PROTOCOL)

                    df = pd.Series(finalxmldict[paper]).to_frame('ColumnName')
                    df.to_csv(os.path.join(
                        str(os.getcwd()), 'papers', pmcid, "fulltext.xml"))

                with open('europe_pmc.pickle', 'wb') as f:
                    pickle.dump(finalxmldict, f, pickle.HIGHEST_PROTOCOL)

                print(f"*/Updating the pickle*/")

    def readpickleddata(self, path):
        import pandas as pd
        object = pd.read_pickle(f'{path}')
        return object

    def apipaperdownload(self, query, size):
        queryresult = self.europepmc(query, size)
        self.makecsv(queryresult)
        readpickled = self.readpickleddata("europe_pmc.pickle")
        self.makexmlfiles(readpickled)

    def scrapingpaperdownload(self, query, size):
        queryresult = self.webscrapepmc(query, size)
        self.makexmlfiles(queryresult)


callgetpapers = getpapersall()
query = "artificial intelligence"
numberofpapers = 10
callgetpapers.scrapingpaperdownload(query, numberofpapers)
callgetpapers.apipaperdownload(query, numberofpapers)
