import requests
from bs4 import BeautifulSoup


def web_search(query):

    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for a in soup.select(".result__a")[:3]:
        results.append(a.get_text())

    return "\n".join(results) if results else "No results found."
