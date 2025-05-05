import argparse
import os
from pyrecon.search import search_service
from pyrecon.screenshot import capture_screenshot
from pyrecon.report import generate_report

def main():
    parser = argparse.ArgumentParser(description='PyRecon CLI')
    parser.add_argument('--service', required=True, help='Service name to search (e.g. gophish)')
    parser.add_argument('--port', type=int, default=80, help='Port number to include in dork and screenshot URL')
    parser.add_argument('--output', default='report.html', help='HTML report file')
    args = parser.parse_args()

    print(f"[DEBUG] Searching for service: {args.service} on port: {args.port}")
    hosts = search_service(args.service, args.port)
    print(f"[DEBUG] Hosts found: {hosts}")

    if not hosts:
        print(f'No hosts found for service: {args.service} on port {args.port}')
        return

    os.makedirs('screenshots', exist_ok=True)
    entries = []
    for host, ip in hosts:
        url = f'http://{ip}:{args.port}'
        print(f"[DEBUG] Capturing screenshot for: {url}")
        try:
            path = capture_screenshot(url)
            entries.append({'host': host, 'url': url, 'screenshot': path})
            print(f"[DEBUG] Screenshot saved: {path}")
        except Exception as e:
            print(f'Failed to capture {url}: {e}')

    print(f"[DEBUG] Generating report for {len(entries)} entries")
    generate_report(entries, args.output)
    print(f'Report generated: {args.output}')

if __name__ == '__main__':
    main()
