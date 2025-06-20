import requests
from datetime import datetime

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

try:
    response = requests.get(url)
    response.raise_for_status()  # Vérifie si la requête a réussi
    data = response.json()
    prix_btc = data["bitcoin"]["usd"]
    print(f"💰 Le prix actuel du Bitcoin est de {prix_btc} $")

    # Débogage : Vérifie si le fichier s'ouvre
    try:
        with open("prix_btc_usd.txt", "a") as f:
            f.write(f"{datetime.now().isoformat()} - Prix BTC : {prix_btc} $\n")
        print("✅ Fichier prix_btc_usd.txt écrit avec succès.")
    except IOError as e:
        print(f"❌ Erreur d'écriture : {e}")
        raise

except requests.exceptions.RequestException as e:
    print("❌ Erreur réseau :", e)
    raise
except Exception as e:
    print("❌ Erreur inattendue :", e)
    raise
