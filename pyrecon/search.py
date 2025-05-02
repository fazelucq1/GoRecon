import shodan
from config import SHODAN_API_KEY

def shodan_search(service: str) -> dict:
    api = shodan.Shodan(SHODAN_API_KEY)
    return api.search(service)
