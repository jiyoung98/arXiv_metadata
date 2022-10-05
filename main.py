import requests
from bs4 import BeautifulSoup
import time
import argparse
import json
from collections import OrderedDict

def arxiv_request(request_url, outputs=[]):
    response = requests.get(request_url)
    soup = BeautifulSoup(response.text, "xml")
    resumptionToken = soup.find("resumptionToken")
    if resumptionToken:
        resumptionToken = soup.find("resumptionToken").text
        cursor = soup.find("resumptionToken")["cursor"]
        completeListSize = soup.find("resumptionToken")["completeListSize"]
        print("CURSOR_NOW: {}/{}".format(cursor, completeListSize))

    metas = soup.find_all("oai_dc:dc")
    for meta in metas:
        a = OrderedDict()
        metadatas = [child for child in meta.contents if child != '\n']
        for metadata in metadatas:
            name = metadata.name.replace("dc:","")
            content = metadata.text
            a[name] = content
            # full pdf
            if content.startswith("http://arxiv.org/abs/"):
                pdf_url = content.replace("abs","pdf")+".pdf"
                a['pdf_url'] = pdf_url
        outputs.append(a)

    return resumptionToken, outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get ArXive Data - updated Daily')
    parser.add_argument('--start', type=str, help='ex) 2021-01-15', default=None)
    parser.add_argument('--end', type=str, help='ex) 2021-01-20', default=None)
    parser.add_argument('--set', type=str, help='ex) cs, physics:hep-ex, ...', default=None)
    args = parser.parse_args()

    target_url = 'http://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc'
    if args.start :
        target_url += "&from={}".format(args.start)
    if args.end :
        target_url += "&until={}".format(args.end)
    if args.set :
        target_url += "&set={}".format(args.set)
    resumptionToken, outputs = arxiv_request(target_url)

    # When there are more than 1,000 results
    if resumptionToken:
        while True:
            new_request_url = "http://export.arxiv.org/oai2?verb=ListRecords&resumptionToken="+resumptionToken
            try:
                resumptionToken, outputs = arxiv_request(new_request_url, outputs)
            except:
                # when received a response to send the request after 5 seconds
                time.sleep(10)
                resumptionToken, outputs = arxiv_request(new_request_url, outputs)
            if not resumptionToken:
                break

    outputs = {i : outputs[i] for i in range(len(outputs))}
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(outputs, f, ensure_ascii=False, indent="\t")