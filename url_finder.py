import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlparse, urljoin
import re
import argparse
import os
import time

def is_valid_url(url):
    return re.match(r'^https?://', url) is not None

def normalize_url(url, base_url):
    parsed = urlparse(url)
    if not parsed.scheme:
        url = urljoin(base_url, url)
    return url.rstrip('/')

def search_gophish(dork, max_results=10):
    urls = set()
    query = urlencode({'q': dork})
    search_url = f"https://www.google.com/search?{query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(search_url, headers=headers, timeout=5)
        if response.status_code != 200:
            return urls
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/url?q='):
                url = href.split('/url?q=')[1].split('&')[0]
                if is_valid_url(url) and 'gophish' in url.lower():
                    urls.add(normalize_url(url, search_url))
            if len(urls) >= max_results:
                break
        time.sleep(1)
    except Exception:
        pass
    return urls

def find_gophish_urls(max_results=10):
    dorks = [
        'inurl:admin intext:gophish',
        'inurl:3333 intext:gophish',
        'filetype:php inurl:admin intext:gophish',
        'site:*.edu inurl:admin intext:gophish'
    ]
    urls = set()
    for dork in dorks:
        urls.update(search_gophish(dork, max_results))
        if len(urls) >= max_results:
            break
    return urls

def save_urls(urls, output_file):
    with open(output_file, 'w') as f:
        for url in sorted(urls):
            f.write(url + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-results', type=int, default=10, help='Maximum number of URLs to find')
    parser.add_argument('--output', default='input_urls.txt', help='Output file for URLs')
    args = parser.parse_args()
    urls = find_gophish_urls(args.max_results)
    save_urls(urls, args.output)

if __name__ == '__main__':
    main()
