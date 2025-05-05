import argparse
import os
from pyrecon.search import google_search
from pyrecon.screenshot import capture_screenshot
from pyrecon.report import generate_report

def main():
    parser = argparse.ArgumentParser(description='PyRecon CLI')
    parser.add_argument('--service', required=True, help='Service to search via Google Dorks')
    parser.add_argument('--output', default='report.html', help='HTML report file')
    args = parser.parse_args()

    hosts = google_search(args.service)

    if not hosts:
        print(f'No hosts found for service: {args.service}')
        return

    os.makedirs('screenshots', exist_ok=True)
    entries = []
    for ip in hosts:
        url = f'http://{ip}'
        try:
            path = capture_screenshot(url)
            entries.append({'host': ip, 'url': url, 'screenshot': path})
        except Exception as e:
            print(f'Failed to capture {url}: {e}')

    generate_report(entries, args.output)
    print(f'Report generated: {args.output}')

if __name__ == '__main__':
    main()
