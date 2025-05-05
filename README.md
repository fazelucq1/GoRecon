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
python main.py --service <service> [--port <port>] [--output report.html]
```

Example specifying port 3333:
```bash
python main.py --service gophish --port 3333 --output gophish_report.html
```

PyRecon constructs the Google dork:

```
intitle:"<service>" inurl:<port>
```

It will:
1. Query Google for the dork using `googlesearch`.
2. Extract hostnames from the URLs returned.
3. Resolve hostnames to IPs.
4. Capture screenshots at `http://<IP>:<port>`.
5. Generate an HTML report in Tailwind with links and screenshots.
