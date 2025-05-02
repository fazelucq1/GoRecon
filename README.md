# PyRecon 🧭

A reconnaissance and reporting tool ported to Python.

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
Create a file `.env` in the root with:
```
SHODAN_API_KEY=your_api_key
```

## Usage
```bash
python main.py --service <service> [options]
```
Available services:
- `shodan`: perform a Shodan search
- `screenshot`: capture a screenshot of a URL
- `report`: generate an HTML report

Examples:
```bash
python main.py --service shodan --query apache
python main.py --service screenshot --query https://example.com
python main.py --service report --input shodan_output.json --output report.html
```
