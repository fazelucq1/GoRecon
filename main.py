import requests
from dotenv import load_dotenv
import os

def search_urls(query, max_results=10):
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")
    
    if not api_key or not cse_id:
        raise ValueError("GOOGLE_API_KEY o GOOGLE_CSE_ID mancanti nel file .env")
    
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": min(max_results, 10)  #10 requests
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("items", [])
        urls = [item["link"] for item in results if "link" in item]
        return urls
    except Exception as e:
        print(f"Errore durante la ricerca: {e}")
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
