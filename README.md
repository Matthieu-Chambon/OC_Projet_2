# Projet 2 - Utilisez les bases de Python pour l'analyse de marché

Le programme vise à parcourir chaque catégorie du site [Books to Scrape](https://books.toscrape.com/index.html) et à extraire les données suivantes de chaque livre :
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

Les données sont exportées (et triées par catégorie) dans des fichiers .csv contenus dans le dossier `CSV files`

Le programme enregistre également la couverture de chaque livre dans le dossier `Book images` (là aussi trié par catégorie)

## Lancement du programme :

```bash
cd "Chemin\complet\vers\le\dossier\du\projet"
git init
git pull https://github.com/Matthieu-Chambon/OC_Projet_2.git main
pip install -r requirements.txt
py .\projet_2.py
```

Il ne reste plus qu'à attendre que le programme se termine
