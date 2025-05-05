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

## License
MIT
