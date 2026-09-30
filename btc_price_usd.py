"""BTC Tracker : prix quotidien + Fear & Greed + alerte Telegram d'achat DCA.

Stratégie : acheter à chaque jour de Fear / Extreme Fear, ne jamais vendre.
Secrets GitHub (jamais dans le code) : TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
et optionnellement DCA_AMOUNT_USD (montant affiché dans l'alerte).
"""
import os
from datetime import datetime, timezone

import requests

PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
FNG_URL = "https://api.alternative.me/fng/?limit=1"
PRICE_FILE = "prix_btc_usd.txt"
BUYS_FILE = "achats_dca.csv"

LABELS_FR = {
    "Extreme Fear": "Peur extrême",
    "Fear": "Peur",
    "Neutral": "Neutre",
    "Greed": "Avidité",
    "Extreme Greed": "Avidité extrême",
}


def get_price():
    r = requests.get(PRICE_URL, timeout=30)
    r.raise_for_status()
    return r.json()["bitcoin"]["usd"]


def get_fng():
    r = requests.get(FNG_URL, timeout=30)
    r.raise_for_status()
    d = r.json()["data"][0]
    return int(d["value"]), d["value_classification"]


def count_buys():
    if not os.path.exists(BUYS_FILE):
        return 0
    with open(BUYS_FILE) as f:
        return max(0, sum(1 for _ in f) - 1)


def log_buy(date, price, value, label):
    new = not os.path.exists(BUYS_FILE)
    with open(BUYS_FILE, "a") as f:
        if new:
            f.write("date,prix_usd,fng,classification\n")
        f.write(f"{date},{price},{value},{label}\n")


def send_telegram(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("⚠️ Secrets Telegram absents, alerte non envoyée.")
        return
    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=30,
    )
    # Ne jamais afficher la réponse : les logs d'un repo public sont publics.
    print("✅ Alerte Telegram envoyée." if r.ok else f"❌ Échec Telegram (HTTP {r.status_code}).")


def main():
    now = datetime.now(timezone.utc)
    price = get_price()
    value, label = get_fng()
    print(f"💰 BTC {price} $ · F&G {value} ({label})")

    with open(PRICE_FILE, "a") as f:
        f.write(f"{now.isoformat()} - Prix BTC : {price} $ - F&G : {value} ({label})\n")

    if os.getenv("TEST_TELEGRAM") == "true":
        send_telegram(f"🧪 Test BTC Tracker : BTC {price:,.0f} $ · F&G {value} ({label})".replace(",", " "))

    if "Fear" not in label:
        print("Pas un jour d'achat.")
        return

    log_buy(now.date().isoformat(), price, value, label)
    amount = os.getenv("DCA_AMOUNT_USD", "").strip()
    emoji = "🔴" if label == "Extreme Fear" else "🟠"
    lines = [
        f"{emoji} BTC — {LABELS_FR.get(label, label)} ({value}/100)",
        f"Prix : {price:,.0f} $".replace(",", " "),
        f"👉 Jour d'achat DCA{f' : {amount} $' if amount else ''}",
        f"Jours d'achat depuis le lancement : {count_buys()}",
        "Stratégie : acheter dans la peur, ne jamais vendre.",
    ]
    send_telegram("\n".join(lines))


if __name__ == "__main__":
    main()
