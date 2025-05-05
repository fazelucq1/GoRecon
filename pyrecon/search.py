import requests
from bs4 import BeautifulSoup
import socket
import urllib.parse

def google_dork_search(dork: str, num_results: int = 20) -> set:
    query = urllib.parse.quote_plus(dork)
    url = f'https://www.google.com/search?q={query}&num={num_results}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = set()
    for a in soup.select('a'):
        href = a.get('href')
        if href and href.startswith('/url?q='):
            link = href.split('&')[0].replace('/url?q=', '')
            links.add(link)
    ips = set()
    for link in links:
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
    return list(google_dork_search(dork))
