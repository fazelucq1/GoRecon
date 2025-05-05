import requests
from bs4 import BeautifulSoup
import socket
import urllib.parse

def ddg_search_dork(dork: str, num_results: int = 30) -> set:
    headers = {'User-Agent': 'Mozilla/5.0'}
    query = urllib.parse.quote_plus(dork)
    url = f'https://html.duckduckgo.com/html/?q={query}&s=0'
    resp = requests.post(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')
    results = soup.find_all('a', {'class': 'result__a'})
    ips = set()
    for a in results[:num_results]:
        link = a['href']
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
    print(f"[DEBUG] Using Dork: {dork}")
    ips = ddg_search_dork(dork)
    print(f"[DEBUG] DDG unique IPs found: {len(ips)}")
    return list(ips)
