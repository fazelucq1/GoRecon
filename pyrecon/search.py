import requests
from bs4 import BeautifulSoup
import socket
import urllib.parse

def google_dork_search(dork: str, num_results: int = 20) -> set:
    ips = set()
    headers = {'User-Agent': 'Mozilla/5.0'}
    for start in range(0, num_results, 10):
        query = urllib.parse.quote_plus(dork)
        url = f'https://www.google.com/search?q={query}&num=10&start={start}'
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # parse result links
        for div in soup.select('div.yuRUbf > a'):
            link = div.get('href')
            try:
                host = urllib.parse.urlparse(link).hostname
                if host:
                    ip = socket.gethostbyname(host)
                    ips.add(ip)
            except Exception:
                continue
    return ips

def google_search(service: str) -> list:
    dork = f'intitle:"{service} - Login" inurl:login'
    results = google_dork_search(dork, num_results=30)
    return list(results)
