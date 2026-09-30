"""BTC Tracker : prix quotidien + Fear & Greed + alerte Telegram d'achat DCA.

Stratégie : acheter les jours de peur extrême (score <= 25), montant selon le
score, ne jamais vendre.
Secrets GitHub (jamais dans le code) : TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.
"""
import os
from datetime import datetime, timezone

import requests

PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
FNG_URL = "https://api.alternative.me/fng/?limit=1"
PRICE_FILE = "prix_btc_usd.txt"
BUYS_FILE = "achats_dca.csv"

# (score max inclus, montant conseillé en $), du plus bas au plus haut
TIERS = [(9, 800), (19, 500), (25, 300)]

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


def advised_amount(value):
    for max_score, amount in TIERS:
        if value <= max_score:
            return amount
    return None


def count_buys():
    if not os.path.exists(BUYS_FILE):
        return 0
    with open(BUYS_FILE) as f:
        return max(0, sum(1 for _ in f) - 1)


def log_buy(date, price, value, label, amount):
    new = not os.path.exists(BUYS_FILE)
    with open(BUYS_FILE, "a") as f:
        if new:
            f.write("date,prix_usd,fng,classification,montant_conseille_usd\n")
        f.write(f"{date},{price},{value},{label},{amount}\n")


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

    amount = advised_amount(value)
    if amount is None:
        print("Pas un jour d'achat.")
        return

    log_buy(now.date().isoformat(), price, value, label, amount)
    emoji = "🚨" if value < 10 else "🔴" if value < 20 else "🟠"
    lines = [
        f"{emoji} BTC — {LABELS_FR.get(label, label)} ({value}/100)",
        f"Prix : {price:,.0f} $".replace(",", " "),
        f"👉 Achat conseillé : {amount} $",
        "Barème : <10 → 800 $ · 10-19 → 500 $ · 20-25 → 300 $",
        f"Jours d'achat depuis le lancement : {count_buys()}",
        "Stratégie : acheter dans la peur extrême, ne jamais vendre.",
    ]
    send_telegram("\n".join(lines))


if __name__ == "__main__":
    main()
