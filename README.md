# PyRecon🧭

A Python tool that analyzes hosts running a given service, captures their web interfaces, performs WHOIS analysis, and generates a Tailwind HTML report.

## Installation
```bash
git clone https://github.com/fazelucq1/PyRecon.git
cd PyRecon
pip install -r requirements.txt
```

## Configuration
No API credentials are required for this version.

## Usage
```bash
python main.py --service <service> [--port <port>] [--output report.html]
```

### Example for Gophish on default port 80:
```bash
python main.py --service gophish --output gophish_report.html
```

### Example specifying port 3333:
```bash
python main.py --service gophish --port 3333 --output gophish_report.html
```

The tool will:
1. Analyze the provided hosts running the specified service.
2. Extract hostnames and resolve to IPs.
3. Perform WHOIS analysis on the hosts.
4. Capture screenshots at `http://<IP>:<port>`.
5. Save screenshots in `screenshots/`.
6. Generate a Tailwind-styled HTML report including links, screenshots, and WHOIS information.
