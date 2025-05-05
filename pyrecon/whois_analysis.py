import re
import socket
import whois
from ipwhois import IPWhois
import dns.resolver
import dns.reversename
import tldextract

def reverse_dns(ip):
    """Esegue un reverse DNS per ottenere il dominio associato a un IP."""
    try:
        rev_name = dns.reversename.from_address(ip)
        risposta = dns.resolver.resolve(rev_name, 'PTR')
        return str(risposta[0]).rstrip('.')
    except Exception:
        return None

def whois_dominio(dominio):
    """Recupera informazioni WHOIS per un dominio."""
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
    """Recupera informazioni WHOIS per un IP."""
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

def analizza_host(host, ip):
    """Analizza un host e restituisce informazioni WHOIS."""
    is_ip = re.match(r'^\d{1,3}(\.\d{1,3}){3}$', host) is not None
    risultato = {
        'host': host,
        'ip': ip,
        'domain': None
    }

    if is_ip:
        dominio_ptr = reverse_dns(ip)
        if dominio_ptr:
            risultato['domain'] = dominio_ptr
            risultato.update(whois_dominio(dominio_ptr))
        else:
            risultato.update(whois_ip(ip))
    else:
        parts = tldextract.extract(host)
        dominio_pulito = f"{parts.domain}.{parts.suffix}"
        risultato['domain'] = dominio_pulito
        risultato.update(whois_dominio(dominio_pulito))

    return risultato
