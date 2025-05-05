import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import argparse
import os

def is_valid_url(url):
    return re.match(r'^https?://', url) is not None

def normalize_url(url, base_url):
    parsed = urlparse(url)
    if not parsed.scheme:
        url = urljoin(base_url, url)
    return url.rstrip('/')

def crawl_url(start_url, max_depth=2, visited=None):
    if visited is None:
        visited = set()
    if max_depth < 0:
        return set()
    urls = set()
    try:
        response = requests.get(start_url, timeout=5)
        if response.status_code != 200:
            return urls
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if not is_valid_url(href):
                href = normalize_url(href, start_url)
            if href not in visited:
                urls.add(href)
                visited.add(href)
        for url in urls.copy():
            if urlparse(url).netloc == urlparse(start_url).netloc:
                urls.update(crawl_url(url, max_depth - 1, visited))
    except Exception:
        pass
    return urls

def save_urls(urls, output_file):
    with open(output_file, 'w') as f:
        for url in sorted(urls):
            f.write(url + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Starting URL to crawl')
    parser.add_argument('--depth', type=int, default=2, help='Maximum crawling depth')
    parser.add_argument('--output', default='input_urls.txt', help='Output file for URLs')
    args = parser.parse_args()
    urls = crawl_url(args.url, args.depth)
    save_urls(urls, args.output)

if __name__ == '__main__':
    main()
