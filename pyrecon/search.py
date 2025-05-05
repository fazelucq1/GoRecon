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
        print(f"[DEBUG] Querying URL: {url}")
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
        except Exception as e:
            print(f"[ERROR] Request failed: {e}")
            continue
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/url?q='):
                link = href.split('&')[0].replace('/url?q=', '')
            elif href.startswith('http'):
                link = href
            else:
                continue
            print(f"[DEBUG] Found link: {link}")
            try:
                host = urllib.parse.urlparse(link).hostname
                if host and not host.endswith('google.com'):
                    ip = socket.gethostbyname(host)
                    print(f"[DEBUG] Resolved {host} -> {ip}")
                    ips.add(ip)
            except Exception as e:
                print(f"[ERROR] Failed to resolve link {link}: {e}")
    print(f"[DEBUG] Total unique IPs found: {len(ips)}")
    return ips

def google_search(service: str) -> list:
    dork = f'intitle:"{service} - Login" inurl:login'
    print(f"[DEBUG] Using Dork: {dork}")
    results = google_dork_search(dork, num_results=30)
    return list(results)
