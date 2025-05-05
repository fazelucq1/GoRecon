# PyRecon🧭

A reconnaissance and reporting tool using Google Dorks in Python.

## Installation
```
git clone https://github.com/fazelucq1/PyRecon.git
cd PyRecon
```

```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py --service <service> [--output report.html]
```
Example:
```bash
python main.py --service gophish --output gophish_report.html
```
This will:
1. Perform a Google Dork search for the service name.
2. Extract hostnames and resolve IPs.
3. Capture screenshots of each host at `http://<IP>`.
4. Generate an HTML report styled with Tailwind including links and screenshots.
