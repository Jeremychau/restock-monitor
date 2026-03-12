import os

import requests

def load_env(path: str) -> dict:
    env = dict()
    env_dir = os.path.dirname(os.path.abspath(path))
    env_file = os.path.join(env_dir, "app.env")
    if not os.path.isfile(env_file):
        return env
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                env[key.strip()] = value.strip()
    return env

_env = load_env(__file__)
TG_TOKEN = _env.get("TG_TOKEN", "")
CHAT_ID = _env.get("TG_CHAT_ID", "")
PRODUCT_URL = f"https://shop.weverse.io/api/wvs/display/api/v1/sales/recommended-sales?displayPlatform=WEB&saleId=54196"
PRODUCT_ID = 54189

WEVERSESHOP_HEADERS = {
    "accept": "*/*",
    "accept-language": "en",
    "referer": "https://shop.weverse.io/en/shop/USD/artists/2/sales/54196",
    "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "x-benx-artistid": "2",
    "x-benx-currency": "USD",
    "x-benx-language": "en",
    "x-benx-os": "web",
    "x-user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "x-weverse-usercountry": "HK",
}

def send_tg(msg: str) -> None:
    requests.post(
        f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg},
    )


def get_product() -> dict | None:
    r = requests.get(PRODUCT_URL, headers=WEVERSESHOP_HEADERS)
    if not r.ok:
        return None
    return r.json()

def check_restock() -> None:
    data = get_product()
    if not data:
        return
    sales = data.get("recommendationsSales") or []
    target_id = int(PRODUCT_ID)
    found = False
    for item in sales:
        if item.get("saleId") != target_id:
            continue
        found = True
        if item.get("status") == "SALE":
            name = item.get("name", "")
            send_tg(f"{name} 有貨")
        return
    if not found:
        send_tg(f"Product {target_id} is not available")

check_restock()
