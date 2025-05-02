import shodan
from config import SHODAN_API_KEY

def shodan_search(query: str) -> dict:
    api = shodan.Shodan(SHODAN_API_KEY)
    try:
        result = api.search(query)
        return result
    except shodan.APIError as e:
        raise RuntimeError(f"Errore Shodan: {e}")
