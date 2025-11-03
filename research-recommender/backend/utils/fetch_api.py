import requests
import xml.etree.ElementTree as ET
from datetime import datetime

ARXIV_BASE = "https://export.arxiv.org/api/query"
ns = {"atom": "http://www.w3.org/2005/Atom"}  # make sure namespace is defined

def fetch_arxiv(query, max_results=10):
    params = {
        'search_query': f'all:{query}',
        'start': 0,
        'max_results': max_results
    }
    r = requests.get(ARXIV_BASE, params=params, timeout=10)
    if r.status_code != 200:
        return []

    root = ET.fromstring(r.text)
    entries = []  # this is the list we will return

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        authors = ", ".join([a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)])
        link = entry.find("atom:id", ns).text
        summary = entry.find("atom:summary", ns).text.strip()

        # published date
        published_raw = entry.find("atom:published", ns).text 
        published_date = datetime.strptime(published_raw, "%Y-%m-%dT%H:%M:%SZ")
        published_str = published_date.strftime("Submitted on %d %b %Y")  # "Submitted on 25 Aug 2021"

        source = "arXiv"

        # append to list
        entries.append({
            "title": title,
            "authors": authors,
            "link": link,
            "summary": summary,
            "published": published_str,
            "source": source
        })

    return entries
