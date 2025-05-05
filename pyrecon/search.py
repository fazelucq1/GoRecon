from googlesearch import search
import socket
import urllib.parse

def search_service(service: str, port: int = 80, num_results: int = 20) -> list:
    dork = f'intitle:"{service}" inurl:{port}'
    print(f"[DEBUG] Using Google dork: {dork}")
    results = []
    seen = set()
    for url in search(dork, stop=num_results, pause=2.0):
        print(f"[DEBUG] Found URL: {url}")
        try:
            hostname = urllib.parse.urlparse(url).hostname
            if hostname and hostname not in seen:
                ip = socket.gethostbyname(hostname)
                print(f"[DEBUG] Resolved {hostname} -> {ip}")
                results.append((hostname, ip))
                seen.add(hostname)
        except Exception as e:
            print(f"[ERROR] Skipping URL {url}: {e}")
    print(f"[DEBUG] Total hosts resolved: {len(results)}")
    return results
