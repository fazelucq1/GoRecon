import argparse
import os
from pyrecon.search import search_service
from pyrecon.screenshot import capture_screenshot
from pyrecon.report import generate_report
from pyrecon.whois_analysis import analizza_host  # Importa il nuovo modulo

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyRecon CLI')
    parser.add_argument('--service', required=True, help='Nome del servizio da cercare (es. gophish)')
    parser.add_argument('--port', type=int, default=80, help='Numero della porta per gli screenshot')
    parser.add_argument('--output', default='report.html', help='File HTML del report')
    parser.add_argument('--timeout', type=int, default=5, help='Timeout in secondi per la cattura dello screenshot')
    args = parser.parse_args()

    print(f"[DEBUG] Ricerca su Google CSE per il servizio: {args.service} sulla porta: {args.port}")
    hosts = search_service(args.service, args.port)  # Lista di tuple (host, ip)
    print(f"[DEBUG] Host trovati: {hosts}")

    if not hosts:
        print(f'Nessun host trovato per il servizio: {args.service} sulla porta {args.port}')
        exit(0)

    os.makedirs('screenshots', exist_ok=True)
    entries = []
    for host, ip in hosts:
        print(f"[DEBUG] Analisi WHOIS per: {host} ({ip})")
        whois_data = analizza_host(host, ip)  # Ottieni dati WHOIS
        url = f'http://{ip}:{args.port}'
        print(f"[DEBUG] Cattura screenshot per: {url}")
        try:
            path = capture_screenshot(url, timeout=args.timeout)
            if path:
                entry = {
                    'host': host,
                    'ip': ip,
                    'url': url,
                    'screenshot': path,
                    'whois': whois_data  # Aggiungi i dati WHOIS
                }
                entries.append(entry)
                print(f"[DEBUG] Screenshot salvato: {path}")
            else:
                print(f"Saltato {url} a causa di timeout o irraggiungibilità")
        except Exception as e:
            print(f'Errore nella cattura di {url}: {e}')

    print(f"[DEBUG] Generazione report per {len(entries)} voci")
    generate_report(entries, args.output)
    print(f'Report generato: {args.output}')
