# Bitcoin Price Tracker

Ce projet est un script Python simple qui récupère le prix actuel du Bitcoin en USD via l'API CoinGecko et l'enregistre dans un fichier texte avec un horodatage.

## Fonctionnalités
- Récupère le prix du Bitcoin en USD en temps réel via l'API CoinGecko.
- Enregistre chaque prix avec un horodatage au format ISO dans un fichier `prix_btc_usd.txt`.
- Gère les erreurs réseau et d'écriture de fichier avec des messages clairs.

## Prérequis
- Python 3.x
- Bibliothèque `requests` (installable via `pip install requests`)

## Installation
1. Clonez ou téléchargez ce dépôt.
2. Installez la dépendance nécessaire :
   ```bash
   pip install requests
