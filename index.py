import requests
import os
import time

URL = os.environ["PRODUCT_URL"]
TG_TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]

while True:
    r = requests.get(URL)

    if "Add to cart" in r.text:
        print("RESTOCK!")

    # time.sleep(60)


def send_tg(msg):
    requests.post(
        f"https://api.telegram.org/botTOKEN/sendMessage",
        data={"chat_id":CHATID,"text":msg}
    )