import argparse
from gorecon.search import shodan_search
from gorecon.screenshot import capture_screenshot
from gorecon.report import generate_report

def main():
    parser = argparse.ArgumentParser(description='GoRecon Python CLI')
    parser.add_argument('--service', required=True,
                        choices=['shodan', 'screenshot', 'report'],
                        help='Servizio da eseguire')
    parser.add_argument('--query', help='Query per Shodan o URL per screenshot')
    parser.add_argument('--input', help='File JSON di input per report')
    parser.add_argument('--output', help='File di output per report (default: report.json)', default='report.json')
    args = parser.parse_args()

    if args.service == 'shodan':
        if not args.query:
            parser.error('Per shodan è richiesto --query')
        results = shodan_search(args.query)
        print(results)

    elif args.service == 'screenshot':
        if not args.query:
            parser.error('Per screenshot è richiesto --query (URL)')
        path = capture_screenshot(args.query)
        print(f"Screenshot salvato in: {path}")

    elif args.service == 'report':
        if not args.input:
            parser.error('Per report è richiesto --input')
        generate_report(args.input, args.output)
        print(f"Report generato in: {args.output}")

if __name__ == '__main__':
    main()
