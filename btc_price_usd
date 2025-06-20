import requests
from datetime import datetime

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    prix_btc = data["bitcoin"]["usd"]
    print(f"💰 Le prix actuel du Bitcoin est de {prix_btc} $")

    with open("/tmp/prix_btc_usd.txt", "a") as f:  # Chemin temporaire
        f.write(f"{datetime.now().isoformat()} - Prix BTC : {prix_btc} $\n")

except Exception as e:
    print("❌ Erreur lors de la récupération des données :", e)
    raise  # Relève l'erreur pour que Actions la voie
