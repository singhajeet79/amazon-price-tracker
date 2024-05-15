"""
This script checks the price and extracts features from a given URL.
"""

import requests
from bs4 import BeautifulSoup

# Function to check price and extract features
def check_price_and_features(url, budget, timeout=10):
    """
    Check the price and extract features of a product from the given URL.

    Args:
        url (str): The URL of the product page.
        budget (float): The budget limit.
        timeout (int, optional): Timeout for the request in seconds. Default is 10.

    Returns:
        dict or None: A dictionary containing product information if found, else None.
    """
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
    }

    response = requests.get(url, headers=headers, timeout=timeout)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_title = soup.find('span', id='productTitle')
    product_price = soup.find('span', class_="a-price-whole")
    product_price_fraction = soup.find('span', class_="a-price-fraction")

    if product_title and product_price:
        product_title = product_title.get_text().strip()
        product_price = product_price.get_text().replace(',', '') + (product_price_fraction.get_text() if product_price_fraction else '')

        try:
            product_price = float(product_price)

            features = soup.find_all('span', class_='a-list-item')
            feature_list = [feature.get_text().strip() for feature in features][:5]

            within_budget = product_price <= budget

            return {
                'title': product_title,
                'price': product_price,
                'within_budget': within_budget,
                'features': feature_list
            }
        except ValueError:
            print("Error converting price to float:", product_price)
            return None
    else:
        print("Error finding product title or price on the page.")
        if not product_title:
            print("Product title not found.")
        if not product_price:
            print("Product price not found.")
        return None

