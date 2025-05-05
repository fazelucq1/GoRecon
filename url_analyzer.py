import json
import re
from urllib.parse import urlparse
import tldextract
import whois
from ipwhois import IPWhois
import dns.resolver
import dns.reversename
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def estrai_info_url(url):
    parsed = urlparse(url)
    host = parsed.hostname
    porta = parsed.port or (443 if parsed.scheme == 'https' else 80)
    is_ip = re.match(r'^\d{1,3}(\.\d{1,3}){3}$', host) is not None
    return host, porta, is_ip

def reverse_dns(ip):
    try:
        rev_name = dns.reversename.from_address(ip)
        risposta = dns.resolver.resolve(rev_name, 'PTR')
        return str(risposta[0]).rstrip('.')
    except Exception:
        return None

def whois_dominio(dominio):
    try:
        info = whois.whois(dominio)
        return {
            'registrant': info.get('name'),
            'registrar': info.get('registrar'),
            'address': info.get('address'),
            'admin_contact': info.get('admin') or info.get('emails'),
            'whois_raw': {k: str(v) for k, v in info.items() if v}
        }
    except Exception as e:
        return {'error': f"Errore WHOIS dominio: {str(e)}"}

def whois_ip(ip):
    try:
        ipwhois = IPWhois(ip)
        result = ipwhois.lookup_rdap()
        return {
            'registrant': result.get('network', {}).get('name'),
            'address': result.get('network', {}).get('remarks', [{}])[0].get('description'),
            'admin_contact': result.get('network', {}).get('abuse_c'),
            'registrar': result.get('asn_description'),
            'whois_raw': result
        }
    except Exception as e:
        return {'error': f"Errore WHOIS IP: {str(e)}"}

def cattura_screenshot(url, output_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(url)
        driver.save_screenshot(output_path)
    except Exception:
        pass
    finally:
        driver.quit()

def analizza_url(url, screenshot_dir):
    host, porta, is_ip = estrai_info_url(url)
    risultato = {
        'url': url,
        'ip': host if is_ip else None,
        'port': porta,
        'domain': None if is_ip else host,
        'screenshot': None
    }
    screenshot_path = os.path.join(screenshot_dir, f"{host}_{porta}.png")
    cattura_screenshot(url, screenshot_path)
    risultato['screenshot'] = screenshot_path
    if is_ip:
        dominio_ptr = reverse_dns(host)
        if dominio_ptr:
            risultato['domain'] = dominio_ptr
            risultato.update(whois_dominio(dominio_ptr))
        else:
            risultato.update(whois_ip(host))
    else:
        parts = tldextract.extract(host)
        dominio_pulito = f"{parts.domain}.{parts.suffix}"
        risultato['domain'] = dominio_pulito
        risultato.update(whois_dominio(dominio_pulito))
    return risultato

def genera_report_html(risultati, output_html):
    html_content = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyRecon URL Analysis Report</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 p-8">
    <div class="container mx-auto">
        <h1 class="text-3xl font-bold mb-8">PyRecon URL Analysis Report</h1>
    """
    for idx, risultato in enumerate(risultati, start=1):
        html_content += f"""
        <div class="bg-white shadow-md rounded-lg p-6 mb-8">
            <h2 class="text-2xl font-semibold mb-4">URL {idx}: {risultato['url']}</h2>
            <p><strong>IP:</strong> {risultato.get('ip', 'N/A')}</p>
            <p><strong>Port:</strong> {risultato['port']}</p>
            <p><strong>Domain:</strong> {risultato['domain']}</p>
            <p><strong>Registrant:</strong> {risultato.get('registrant', 'N/A')}</p>
            <p><strong>Registrar:</strong> {risultato.get('registrar', 'N/A')}</p>
            <p><strong>Address:</strong> {risultato.get('address', 'N/A')}</p>
            <p><strong>Admin Contact:</strong> {risultato.get('admin_contact', 'N/A')}</p>
            <div class="mt-4">
                <h3 class="text-xl font-medium">Screenshot:</h3>
                <img src="{risultato['screenshot']}" alt="Screenshot of {risultato['url']}" class="mt-2 max-w-full h-auto">
            </div>
        </div>
        """
    html_content += """
    </div>
</body>
</html>
    """
    with open(output_html, 'w') as f:
        f.write(html_content)

def main(file_input, file_output_json, file_output_html, screenshot_dir='screenshots'):
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    with open(file_input, 'r') as f:
        urls = [riga.strip() for riga in f if riga.strip()]
    risultati = [analizza_url(url, screenshot_dir) for url in urls]
    with open(file_output_json, 'w') as f:
        json.dump(risultati, f, indent=4)
    genera_report_html(risultati, file_output_html)

if __name__ == '__main__':
    main('input_urls.txt', 'output.json', 'report.html')
