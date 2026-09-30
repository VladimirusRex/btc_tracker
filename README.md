# Bitcoin Price Tracker

Script Python lancé chaque jour par GitHub Actions (8h UTC) :
- récupère le prix du Bitcoin (API CoinGecko) et l'indice Fear & Greed (alternative.me) ;
- les enregistre dans `prix_btc_usd.txt` ;
- les jours de peur extrême (score ≤ 25), envoie une alerte Telegram avec un montant d'achat conseillé et ajoute une ligne à `achats_dca.csv`.

Stratégie : acheter dans la peur extrême, ne jamais vendre.

| Score F&G | Achat conseillé |
|---|---|
| < 10 | 800 $ |
| 10-19 | 500 $ |
| 20-25 | 300 $ |

## Configuration
Dans *Settings → Secrets and variables → Actions*, créer les secrets :
- `TOKEN_DU_BOT` : token du bot (via @BotFather) ;
- `CHAT_ID` : identifiant de la conversation qui reçoit les alertes ;

Aucun secret dans le code : les logs d'un dépôt public sont publics.

## Lancer en local
```bash
pip install requests
TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... python btc_price_usd.py
```
