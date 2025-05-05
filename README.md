# PyRecon

A Python tool for discovering servers running GoPhish, analyzing URLs, collecting WHOIS information, taking screenshots, and generating professional HTML reports using Tailwind CSS.

## Features
- Uses Google Dorks to find GoPhish admin interfaces
- Extracts domain and IP information from URLs
- Performs WHOIS lookups for domains and IPs
- Captures screenshots of websites
- Generates JSON output and HTML reports
- Uses Tailwind CSS for professional report styling

## Prerequisites
- Python 3.8+
- Chrome browser installed
- ChromeDriver (compatible with your Chrome version)
- Internet connection

## Installation
1. Clone the repository:
```bash
git clone https://github.com/fazelucq1/PyRecon.git
cd PyRecon
```
2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Download and configure ChromeDriver:
   - Download from https://chromedriver.chromium.org/
   - Place it in your PATH or specify its location in the script

## Usage
1. Discover GoPhish servers using Google Dorks:
```bash
python url_finder.py --max-results 10 --output input_urls.txt
```
2. Analyze URLs and generate reports:
```bash
python url_analyzer.py
```
3. Output:
   - `input_urls.txt`: List of discovered GoPhish URLs
   - `output.json`: JSON file with analysis results
   - `report.html`: HTML report with Tailwind styling
   - `screenshots/`: Directory containing website screenshots

## Project Structure
```
PyRecon/
├── input_urls.txt      # Input file with URLs
├── url_analyzer.py     # URL analysis script
├── url_finder.py       # GoPhish server discovery script
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
├── screenshots/        # Output directory for screenshots
├── output.json         # Output JSON file
└── report.html         # Output HTML report
```

## Notes
- Ensure ChromeDriver is compatible with your Chrome browser version
- The analyzer runs in headless mode for screenshots
- WHOIS queries may be rate-limited by some registrars
- Screenshots are saved as PNG files in the `screenshots/` directory
- Google Dork searches are limited to avoid rate-limiting
- Use responsibly and respect legal and ethical boundaries
- Requires internet access for Google searches and WHOIS queries
