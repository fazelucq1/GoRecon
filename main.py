import argparse
import os
from pyrecon.search import shodan_search
from pyrecon.screenshot import capture_screenshot
from pyrecon.report import generate_report
from shodan import APIError

def main():
    parser = argparse.ArgumentParser(description='PyRecon CLI')
    parser.add_argument('--service', required=True,
                        help='Name of service to search (e.g. gophish)')
    parser.add_argument('--output', help='Output HTML report file', default='report.html')
    args = parser.parse_args()

    try:
        results = shodan_search(args.service)
    except APIError as e:
        print(f"Shodan API error: {e}")
        return

    hosts = [match.get('ip_str') for match in results.get('matches', [])]

    if not hosts:
        print('No hosts found for service:', args.service)
        return

    os.makedirs('screenshots', exist_ok=True)
    entries = []
    for ip in hosts:
        url = f"http://{ip}"
        try:
            path = capture_screenshot(url)
            entries.append({'host': ip, 'url': url, 'screenshot': path})
        except Exception as e:
            print(f"Failed to screenshot {url}: {e}")

    generate_report(entries, args.output)
    print(f"Report generated: {args.output}")

if __name__ == '__main__':
    main()
