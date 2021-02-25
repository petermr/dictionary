# -*- coding: utf-8 -*-

#These are all the imports
import requests
import lxml.etree
import lxml
import os

def search(query,size,synonym='YES'):
  #change synonym to no otherwise yes is the default

  #The code regarding the size of the query currently only works till 100 terms. This is on purpose and I will add Function to access next cursormark which is basically next page of the resultant of the query once I have enough permision and knowledge
  if size<=1000:
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    payload = {'query': query,'resultType':'core','pageSize':1000,'synonym':synonym}
    r = requests.post('https://www.ebi.ac.uk/europepmc/webservices/rest/searchPOST', data=payload,headers=headers)
    return r.content
  if size>1000:
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    payload = {'query': query,'format':format,'resultType':'core','pageSize':1000}
    r = requests.post('https://www.ebi.ac.uk/europepmc/webservices/rest/searchPOST', data=payload,headers=headers)
    xmlschema_doc = lxml.etree.XML(r.content)
    cursor=xmlschema_doc.xpath('//nextCursorMark')
    nextCursorMark=[]
    for a in cursor:
      nextCursorMark.append(a.text)

    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    payload = {'query': query,'format':format,'resultType':'core','cursorMark':nextCursorMark[0],'pageSize':1000}
    r2 = requests.post('https://www.ebi.ac.uk/europepmc/webservices/rest/searchPOST', data=payload,headers=headers)
    return r.content+r2.content

#this is the function that will the the result from search and will download and save the files.
def makefiles(searchvariable,size):
  xmlschema_doc = lxml.etree.XML(searchvariable)
  PMC=[]
  for a in xmlschema_doc.xpath('//fullTextId'):
    PMC.append(a.text)

  for i in PMC[0:size]:
    r = requests.get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{i}/fullTextXML")
    root = lxml.etree.fromstring(r.text)
    tree = lxml.etree.ElementTree(root)
    if not os.path.isdir(os.path.join(str(os.getcwd()),'papers')):
      os.makedirs(os.path.join(str(os.getcwd()),'papers'))
    tree.write(os.path.join(str(os.getcwd()),'papers',f"{i}.xml"))

#type search query in this form
a=search('covid',12)

#pass in this query to makefiles along with the number of files you want to save
makefiles(a,12)
