# PyRecon 🧭

## 🚨To make it work you need to have shodan pro🚨

A reconnaissance and reporting tool in Python.  

## Installation
```
git clone https://github.com/fazelucq1/PyRecon.git
cd PyRecon
```
```bash
pip install -r requirements.txt
```

## Configuration
Create a file `.env` at the project root containing:
```
SHODAN_API_KEY=your_api_key
```

## Usage
```bash
python main.py --service <service>
```
Example:
```bash
python main.py --service gophish
```
This will:  
1. Search Shodan for the given service.  
2. For each matching host, capture a screenshot of its web interface.  
3. Generate an HTML report including details and screenshots.

