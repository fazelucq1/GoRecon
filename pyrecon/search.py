import os
import socket
import urllib.parse
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
CX = os.getenv('GOOGLE_CX')

if not (API_KEY and CX):
    raise RuntimeError('Set GOOGLE_API_KEY and GOOGLE_CX in .env')

def search_service(service: str, port: int = 80, num_results: int = 20) -> list:
    dork = f'intitle:"{service}" inurl:{port}'
    print(f"[DEBUG] Using Google Custom Search Dork: {dork}")
    service_api = build('customsearch', 'v1', developerKey=API_KEY)
    start = 1
    results = []
    seen = set()
    while len(results) < num_results:
        resp = service_api.cse().list(q=dork, cx=CX, start=start).execute()
        items = resp.get('items', [])
        if not items:
            break
        for item in items:
            link = item.get('link')
            print(f"[DEBUG] Found URL: {link}")
            hostname = urllib.parse.urlparse(link).hostname
            if hostname and hostname not in seen:
                try:
                    ip = socket.gethostbyname(hostname)
                    print(f"[DEBUG] Resolved {hostname} -> {ip}")
                    results.append((hostname, ip))
                    seen.add(hostname)
                except Exception as e:
                    print(f"[ERROR] DNS resolution failed for {hostname}: {e}")
                if len(results) >= num_results:
                    break
        start += len(items)
    print(f"[DEBUG] Total hosts resolved: {len(results)}")
    return results
