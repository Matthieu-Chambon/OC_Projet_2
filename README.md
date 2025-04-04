# 📚 Projet 2 - Utilisez les bases de Python pour l'analyse de marché

Ce programme scrappe le site [Books to Scrape](https://books.toscrape.com/index.html) pour extraire, organiser et sauvegarder des données sur les livres en vente.

## 📊 Données extraites
Le script collecte les informations suivantes pour chaque livre :

✅ `product_page_url`  
✅ `universal_product_code (UPC)`  
✅ `title`  
✅ `price_including_tax`  
✅ `price_excluding_tax`  
✅ `number_available`  
✅ `product_description`  
✅ `category`  
✅ `review_rating`  
✅ `image_url`  

📂 **Les données sont enregistrées dans** :
- Des fichiers `.csv` triés par catégorie (dossier `CSV files`)
- Des images de couverture des livres (dossier `Book images`, trié par catégorie)

## 📥 Installation et exécution

1️⃣ **Cloner le projet**  

```sh
cd "Chemin\complet\vers\le\dossier\du\projet"
git clone https://github.com/Matthieu-Chambon/OC_Projet_2
cd OC_Projet_2
```

2️⃣ **Installer les dépendances**

```sh
pip install -r requirements.txt
```

2️⃣ **Exécuter le script**

```sh
py .\projet_2.py
```

## 🔄 Pipeline ETL : Extraction, Transformation, Chargement
Ce projet suit une approche ETL (Extract, Transform, Load) pour traiter les données efficacement :

🏗️ **Extraction (Extract) :**

- Le programme envoie des requêtes HTTP au site Books to Scrape
- Il récupère les pages HTML et extrait les données pertinentes

⚙️ **Transformation (Transform) :**

- Nettoyage et structuration des données (extraction des nombres, formatage des prix, tri par catégorie)
- Conversion des données en un format exploitable (CSV)

🚚 **Chargement (Load) :**

- Les données sont enregistrées dans des fichiers CSV organisés par catégorie
- Les images des livres sont téléchargées et stockées