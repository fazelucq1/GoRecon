import requests
from bs4 import BeautifulSoup
import socket
import urllib.parse

def google_search(service: str, num_results: int = 20) -> list:
    query = urllib.parse.quote_plus(f"inurl:{service}")
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = []
    for a in soup.select('a'):
        href = a.get('href')
        if href and href.startswith('/url?q='):
            link = href.split('&')[0].replace('/url?q=', '')
            links.append(link)

    ips = set()
    for link in links:
        try:
            host = urllib.parse.urlparse(link).hostname
            if host:
                ip = socket.gethostbyname(host)
                ips.add(ip)
        except Exception:
            continue

    return list(ips)
