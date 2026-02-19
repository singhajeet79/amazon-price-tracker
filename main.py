"""
Core scraping logic for Amazon Price Tracker
"""

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
        raise ScrapingError(f"HTTP {response.status_code} received")

    if "captcha" in response.text.lower():
        raise ScrapingError("Amazon blocked request (CAPTCHA)")

    return BeautifulSoup(response.text, "html.parser")


def extract_title(soup: BeautifulSoup) -> str:
    title = soup.select_one("#productTitle")
    if not title:
        raise ScrapingError("Product title not found")
    return title.get_text(strip=True)


def extract_price(soup: BeautifulSoup) -> float:
    selectors = [
        "span.a-price span.a-offscreen",
        "span.a-offscreen",
        "span.a-price-whole",
    ]

    for selector in selectors:
        price_tag = soup.select_one(selector)
        if price_tag:
            raw = price_tag.get_text()
            cleaned = (
                raw.replace("₹", "")
                .replace("$", "")
                .replace(",", "")
                .strip()
            )
            try:
                return float(cleaned)
            except ValueError:
                continue

    raise ScrapingError("Product price not found")


def extract_features(soup: BeautifulSoup) -> list[str]:
    features = soup.select("ul.a-unordered-list.a-vertical.a-spacing-mini span.a-list-item")
    return [f.get_text(strip=True) for f in features][:5]


def check_price_and_features(url: str, budget: float) -> dict:
    soup = fetch_page(url)

    title = extract_title(soup)
    price = extract_price(soup)
    features = extract_features(soup)

    return {
        "title": title,
        "price": price,
        "within_budget": price <= budget,
        "features": features,
    }


if __name__ == "__main__":
    test_url = input("Enter Amazon product URL: ")
    budget = float(input("Enter your budget: "))

    try:
        result = check_price_and_features(test_url, budget)
        print("\n---------------------------")
        print("Title :", result["title"])
        print("Price :", result["price"])
        print("Within Budget:", result["within_budget"])
        print("Features:")
        for f in result["features"]:
            print("-", f)
    except ScrapingError as e:
        print("ERROR:", e)
