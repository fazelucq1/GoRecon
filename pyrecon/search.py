import shodan
from config import SHODAN_API_KEY
from shodan import APIError

def shodan_search(service: str) -> dict:
    api = shodan.Shodan(SHODAN_API_KEY)
    try:
        return api.search(service)
    except APIError:
        raise
