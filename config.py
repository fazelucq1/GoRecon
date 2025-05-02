from dotenv import load_dotenv
import os

load_dotenv()

SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')
if not SHODAN_API_KEY:
    raise RuntimeError('Imposta SHODAN_API_KEY in .env')
