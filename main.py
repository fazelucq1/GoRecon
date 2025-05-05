import requests
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

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
        "num": min(max_results, 10)  # Google API limita a 10 risultati per richiesta
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

def take_screenshot(url, index):
    """Acquisisce uno screenshot dell'URL e lo salva in screenshots/."""
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    
    screenshot_path = f"{screenshot_dir}/screenshot_{index}.png"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.set_window_size(1280, 720)
        driver.get(url)
        time.sleep(2)  # Attendi caricamento pagina
        driver.save_screenshot(screenshot_path)
        driver.quit()
        return screenshot_path
    except Exception as e:
        print(f"Errore screenshot per {url}: {e}")
        return None

def generate_html_report(urls):
    """Genera un report HTML con Tailwind CSS."""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyRecon Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto py-10 px-4">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">PyRecon Search Report</h1>
        <p class="text-gray-600 mb-4">Risultati per la query: <code class="bg-gray-200 px-1 rounded">intitle:"Gophish - Login" inurl:login</code></p>
        <div class="bg-white shadow-md rounded-lg overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">URL</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Screenshot</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
    """
    
    for index, url in enumerate(urls):
        screenshot_path = take_screenshot(url, index)
        screenshot_html = f'<img src="{screenshot_path}" alt="Screenshot di {url}" class="max-w-xs h-auto rounded shadow">' if screenshot_path else '<span class="text-red-500">Screenshot non disponibile</span>'
        
        html_content += f"""
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <a href="{url}" target="_blank" class="text-blue-600 hover:underline break-all">{url}</a>
                        </td>
                        <td class="px-6 py-4">{screenshot_html}</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
        </div>
        <footer class="mt-8 text-gray-500 text-sm">
            <p>Generato da PyRecon il {}</p>
        </footer>
    </div>
</body>
</html>
    """.format(time.strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        with open("report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Report generato: report.html")
    except Exception as e:
        print(f"Errore generazione report: {e}")

def main():
    query = 'intitle:"Gophish - Login" inurl:login'
    urls = search_urls(query)
    if urls:
        generate_html_report(urls)
    else:
        print("Nessun URL trovato.")

if __name__ == "__main__":
    main()
