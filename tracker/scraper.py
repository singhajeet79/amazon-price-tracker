import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


class ScrapingError(Exception):
    pass


def fetch_page(url: str, timeout: int = 10) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=timeout)

    if response.status_code != 200:
        raise ScrapingError(f"HTTP {response.status_code}")

    if "captcha" in response.text.lower():
        raise ScrapingError("Amazon blocked request")

    return BeautifulSoup(response.text, "html.parser")


def extract_title(soup: BeautifulSoup) -> str:
    title = soup.select_one("#productTitle")
    if not title:
        raise ScrapingError("Title not found")
    return title.get_text(strip=True)


def extract_price(soup: BeautifulSoup) -> float:
    selectors = [
        "span.a-price span.a-offscreen",
        "span.a-offscreen",
        "span.a-price-whole",
    ]

    for selector in selectors:
        tag = soup.select_one(selector)
        if tag:
            raw = tag.get_text()
            cleaned = (
                raw.replace("₹", "")
                .replace("$", "")
                .replace(",", "")
                .strip()
            )
            try:
                return float(cleaned)
            except ValueError:
                pass

    raise ScrapingError("Price not found")
