# PyRecon🧭

A Python tool that uses the Google Custom Search API to discover hosts running a given service, captures their web interfaces, and generates a Tailwind HTML report.

## Installation
```bash
git clone https://github.com/fazelucq1/PyRecon.git
cd PyRecon
pip install -r requirements.txt
```

## Configuration
Change your credentials in the `.env` file:
```dotenv
GOOGLE_API_KEY=...
GOOGLE_CX=...
```

## Setting up Google API Credentials

### Step 1: Get Google API Credentials
- Go to the [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or select an existing one
- Enable the **Custom Search JSON API**:
  - Navigate to `APIs & Services` > `Library`
  - Search for **Custom Search JSON API**
  - Click **Enable**

### Step 2: Create API Key
- Go to `APIs & Services` > `Credentials`
- Click **Create Credentials** > **API Key**
- Copy this key and add it to your `.env` file as `GOOGLE_API_KEY`

### Step 3: Create Custom Search Engine (CX)
- Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
- Click **Get Started**
- Configure your search engine:
  - Set it to search the entire web
  - Give it any name and description
- After creation, go to the **Control Panel**
  - Find your **Search engine ID** — this is your `GOOGLE_CX` value in `.env`

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

The tool constructs the Google dork:
```
intitle:"<service>" inurl:<port>
```

It will:
1. Perform the search via Google Custom Search API.
2. Extract hostnames and resolve to IPs.
3. Capture screenshots at `http://<IP>:<port>`.
4. Save screenshots in `screenshots/`.
5. Generate a Tailwind-styled HTML report including links and screenshots.
