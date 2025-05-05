import requests
from dotenv import load_dotenv
import os
import argparse
import logging
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from collections import Counter
import time
import numpy as np

# Configura logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def build_query(args):
    """Costruisce la query Google Dorks dai parametri CLI."""
    query_parts = []
    
    if args.query:
        query_parts.append(args.query)
    if args.intitle:
        query_parts.append(f'intitle:"{args.intitle}"')
    if args.inurl:
        query_parts.append(f'inurl:{args.inurl}')
    if args.site:
        query_parts.append(f'site:{args.site}')
    if args.filetype:
        query_parts.append(f'filetype:{args.filetype}')
    if args.intext:
        query_parts.append(f'intext:"{args.intext}"')
    if args.exclude:
        query_parts.append(f'-{args.exclude}')
    
    return " ".join(query_parts).strip() or 'intitle:"Gophish - Login" inurl:login'

def search_urls(query, max_results=10):
    """Esegue la ricerca tramite Google Custom Search API."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")
    
    if not api_key or not cse_id:
        raise ValueError("GOOGLE_API_KEY o GOOGLE_CSE_ID mancanti nel file .env")
    
    url = "https://www.googleapis.com/customsearch/v1"
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
        logging.info(f"Trovati {len(urls)} URL per la query: {query}")
        return urls
    except Exception as e:
        logging.error(f"Errore durante la ricerca: {e}")
        return []

def generate_charts(urls):
    """Genera grafici e li salva in charts/."""
    chart_dir = "charts"
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)
    
    # Estrai domini
    domains = [urlparse(url).netloc for url in urls]
    domain_counts = Counter(domains)
    
    # Grafico a barre: Conteggio URL per dominio
    plt.figure(figsize=(10, 6))
    plt.bar(domain_counts.keys(), domain_counts.values(), color="skyblue")
    plt.xlabel("Dominio")
    plt.ylabel("Numero di URL")
    plt.title("Conteggio URL per Dominio")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    domain_chart_path = f"{chart_dir}/domain_counts.png"
    plt.savefig(domain_chart_path)
    plt.close()
    
    # Istogramma: Distribuzione lunghezze URL
    url_lengths = [len(url) for url in urls]
    plt.figure(figsize=(10, 6))
    variance = f"Varianza: {round(np.var(url_lengths), 2)}" if url_lengths else "Varianza: N/A"
    plt.hist(url_lengths, bins=10, color="lightgreen", edgecolor="black")
    plt.xlabel("Lunghezza URL")
    plt.ylabel("Frequenza")
    plt.title(f"Distribuzione Lunghezze URL\n{variance}")
    plt.tight_layout()
    length_chart_path = f"{chart_dir}/url_lengths.png"
    plt.savefig(length_chart_path)
    plt.close()
    
    return domain_chart_path, length_chart_path

def generate_html_report(urls, query, domain_chart_path, length_chart_path):
    """Genera un report HTML con Tailwind CSS e grafici."""
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
        <p class="text-gray-600 mb-4">Query: <code class="bg-gray-200 px-1 rounded">{}</code></p>
        <div class="bg-white shadow-md rounded-lg overflow-hidden mb-8">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">URL</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Dominio</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
    """.format(query)
    
    for url in urls:
        domain = urlparse(url).netloc
        html_content += f"""
                    <tr>
                        <td class="px-6 py-4 whitespace-nowrap">
                            <a href="{url}" target="_blank" class="text-blue-600 hover:underline break-all">{url}</a>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap">{domain}</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
        </div>
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Analisi dei Risultati</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white p-4 rounded-lg shadow">
                <h3 class="text-lg font-medium text-gray-700 mb-2">Conteggio URL per Dominio</h3>
                <img src="{}" alt="Conteggio URL per Dominio" class="w-full h-auto">
            </div>
            <div class="bg-white p-4 rounded-lg shadow">
                <h3 class="text-lg font-medium text-gray-700 mb-2">Distribuzione Lunghezze URL</h3>
                <img src="{}" alt="Distribuzione Lunghezze URL" class="w-full h-auto">
            </div>
        </div>
        <footer class="mt-8 text-gray-500 text-sm">
            <p>Generato da PyRecon il {}</p>
        </footer>
    </div>
</body>
</html>
    """.format(domain_chart_path, length_chart_path, time.strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        with open("report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        logging.info("Report generato: report.html")
    except Exception as e:
        logging.error(f"Errore generazione report: {e}")

def main():
    parser = argparse.ArgumentParser(description="PyRecon: Cerca URL con Google Dorks e genera un report HTML.")
    parser.add_argument("--query", help="Query di base (es. 'login page')")
    parser.add_argument("--intitle", help="Cerca nel titolo (es. 'Gophish - Login')")
    parser.add_argument("--inurl", help="Cerca nell'URL (es. 'login')")
    parser.add_argument("--site", help="Limita a un dominio (es. 'example.com')")
    parser.add_argument("--filetype", help="Tipo di file (es. 'pdf')")
    parser.add_argument("--intext", help="Cerca nel testo (es. 'admin')")
    parser.add_argument("--exclude", help="Escludi termine (es. 'signup')")
    parser.add_argument("--max-results", type=int, default=10, help="Numero massimo di risultati (default: 10)")
    
    args = parser.parse_args()
    query = build_query(args)
    urls = search_urls(query, args.max_results)
    
    if urls:
        domain_chart_path, length_chart_path = generate_charts(urls)
        generate_html_report(urls, query, domain_chart_path, length_chart_path)
    else:
        logging.warning("Nessun URL trovato.")

if __name__ == "__main__":
    main()
