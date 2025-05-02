import argparse
import os
from pyrecon.search import shodan_search
from pyrecon.screenshot import capture_screenshot
from pyrecon.report import generate_report

def main():
    parser = argparse.ArgumentParser(description='PyRecon CLI')
    parser.add_argument('--service', required=True,
                        help='Name of service to search (e.g. gophish)')
    parser.add_argument('--output', help='Output HTML report file', default='report.html')
    args = parser.parse_args()

    results = shodan_search(args.service)
    hosts = [match.get('ip_str') for match in results.get('matches', [])]

    os.makedirs('screenshots', exist_ok=True)
    entries = []
    for ip in hosts:
        url = f"http://{ip}"
        path = capture_screenshot(url)
        entries.append({'host': ip, 'url': url, 'screenshot': path})

    generate_report(entries, args.output)
    print(f"Report generated: {args.output}")

if __name__ == '__main__':
    main()
