# PyRecon 🧭

A Python script to search URLs using Google Dorks via the Google Custom Search API and generate a professional HTML report with analytical charts.

## Requirements
- Python 3.8+
- Dependencies: `requests`, `python-dotenv`, `matplotlib`, `numpy`
- Google API Key and Custom Search Engine ID

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/fazelucq1/PyRecon.git
   cd PyRecon
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

# Get the API 🐝

## Step 1: Get Google API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the "Custom Search JSON API":
   - Navigate to "APIs & Services" > "Library"
   - Search for "Custom Search JSON API"
   - Click "Enable"

## Step 2: Create API Key

1. In Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API Key"
3. Copy this key and put it in your `.env` file as `GOOGLE_API_KEY`

## Step 3: Create Custom Search Engine (CX)

1. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/about/)
2. Click "Get Started"
3. Configure your search engine:
   - You can set it to search the entire web
   - Give it any name and description
4. After creation, go to "Control Panel"
5. Find your "Search engine ID" - this is your `GOOGLE_CX` value for `.env`

## Usage
Run the script with custom Google Dorks parameters:
```bash
python main.py --intitle "Gophish - Login" --inurl login --max-results 10
```
- **Available parameters**:
  - `--query`: Base query (e.g., `login page`)
  - `--intitle`: Search in title (e.g., `Gophish - Login`)
  - `--inurl`: Search in URL (e.g., `login`)
  - `--site`: Restrict to a domain (e.g., `example.com`)
  - `--filetype`: File type (e.g., `pdf`)
  - `--intext`: Search in text (e.g., `admin`)
  - `--exclude`: Exclude term (e.g., `signup`)
  - `--max-results`: Maximum number of results (default: 10)

- **Example**:
  ```bash
  python main.py --site example.com --filetype pdf --exclude signup
  ```

- Results are saved in `report.html`.
- Charts are saved in `charts/`.

## Report
The HTML report includes:
- A table listing found URLs and their domains.
- Charts:
  - URL count by domain (bar chart).
  - URL length distribution (histogram).

## Troubleshooting
- **Error `QStandardPaths: wrong permissions`** (WSL):
  - Fix permissions:
    ```bash
    chmod 0700 /mnt/wslg/runtime-dir
    ```

## Notes
- Ensure the Custom Search Engine associated with the CSE ID is configured to search the entire web at [cse.google.com](https://cse.google.com/cse/).
- The Google Custom Search API has a limit of 100 free queries per day.
- Use responsibly, adhering to Google's terms of service and privacy regulations.
🐝🐝🐝🐝🐝🐝🐝🐝🐝🐝🐝🐝
