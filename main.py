import requests
from bs4 import BeautifulSoup
import re

def search_urls(query, max_results=10):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"}
    url = f"https://www.google.com/search?q={query}&num={max_results}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        urls = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.startswith("/url?q="):
                # Estrai l'URL reale
                clean_url = re.search(r"/url\?q=(.+?)&", href)
                if clean_url:
                    urls.append(clean_url.group(1))
        
        return urls[:max_results]
    except Exception as e:
        print(f"Errore: {e}")
        return []

def save_to_file(urls, output_file="results.txt"):
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")
        print(f"Salvati {len(urls)} URL in {output_file}")
    except Exception as e:
        print(f"Errore salvataggio: {e}")

def main():
    query = 'intitle:"Gophish - Login" inurl:login'
    urls = search_urls(query)
    save_to_file(urls)

if __name__ == "__main__":
    main()
