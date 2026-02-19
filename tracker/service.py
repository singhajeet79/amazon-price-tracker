from tracker.storage import get_trackers_by_contact
from tracker.scraper import (
    fetch_page,
    extract_title,
    extract_price,
    ScrapingError,
)

from tracker.storage import (
    get_or_create_product,
    create_tracker,
    record_price,
    get_active_trackers,
    deactivate_tracker,
)


# -------------------------
# PUBLIC API
# -------------------------

def get_current_price(url: str) -> dict:
    soup = fetch_page(url)
    title = extract_title(soup)
    price = extract_price(soup)

    return {
        "title": title,
        "price": price
    }


def track_product(url: str, target_price: float, channel: str, contact: str) -> dict:
    data = get_current_price(url)

    product_id = get_or_create_product(
        url=url,
        title=data["title"],
        price=data["price"]
    )

    create_tracker(
        product_id=product_id,
        target_price=target_price,
        channel=channel,
        contact=contact
    )

    record_price(product_id, data["price"])

    return {
        "title": data["title"],
        "price": data["price"],
        "target_price": target_price,
        "channel": channel,
        "contact": contact
    }


def run_price_checks():
    trackers = get_active_trackers()

    for tracker_id, product_id, target_price, channel, contact in trackers:
        try:
            from tracker.storage import get_connection
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT url FROM products WHERE id=?", (product_id,))
            url = cur.fetchone()[0]
            conn.close()

            data = get_current_price(url)
            record_price(product_id, data["price"])

            if data["price"] <= target_price:
                send_alert(
                    channel=channel,
                    contact=contact,
                    title=data["title"],
                    price=data["price"],
                    target=target_price
                )
                deactivate_tracker(tracker_id)

        except ScrapingError as e:
            print("Scraping error:", e)


# -------------------------
# ALERT DISPATCHER (stub)
# -------------------------

def send_alert(channel, contact, title, price, target):
    message = f"""
PRICE ALERT!

{title}
Current Price: {price}
Target Price: {target}
"""

    if channel == "email":
        print(f"[EMAIL to {contact}] {message}")

    elif channel == "telegram":
        print(f"[TELEGRAM to {contact}] {message}")

    else:
        print("Unknown channel:", channel)


def list_user_trackers(contact: str):
    return get_trackers_by_contact(contact)


def stop_tracker(tracker_id: int):
    from tracker.storage import deactivate_tracker
    deactivate_tracker(tracker_id)
