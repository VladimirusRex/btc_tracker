# Bitcoin Price Tracker

Script Python lancé chaque jour par GitHub Actions (8h UTC) :
- récupère le prix du Bitcoin (API CoinGecko) et l'indice Fear & Greed (alternative.me) ;
- les enregistre dans `prix_btc_usd.txt` ;
- les jours de **Fear** ou **Extreme Fear**, envoie une alerte Telegram « jour d'achat » et ajoute une ligne à `achats_dca.csv`.

Stratégie : acheter à chaque jour de peur, ne jamais vendre.

## Configuration
Dans *Settings → Secrets and variables → Actions*, créer les secrets :
- `TELEGRAM_BOT_TOKEN` : token du bot (via @BotFather) ;
- `TELEGRAM_CHAT_ID` : identifiant de la conversation qui reçoit les alertes ;
- `DCA_AMOUNT_USD` (optionnel) : montant affiché dans l'alerte.

Aucun secret dans le code : les logs d'un dépôt public sont publics.

## Lancer en local
```bash
pip install requests
TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... python btc_price_usd.py
```
