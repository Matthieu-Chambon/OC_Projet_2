import requests
from bs4 import BeautifulSoup
import csv
import os
import shutil
from urllib.parse import urljoin


print("Début de l'exportation des données ...")

# Suppression du dossier "CSV files" s'il existe afin de le regénérer
csv_folder = "CSV files"

if os.path.exists(csv_folder):
    shutil.rmtree(csv_folder)

# Création du dossier contenant tous les CSV
os.makedirs(csv_folder)

# Suppression du dossier "Book images" s'il existe afin de le regénérer
img_folder = "Book images"

if os.path.exists(img_folder):
    shutil.rmtree(img_folder)

# Création du dossier contenant toutes les images
os.makedirs(img_folder)



# Parcourt chaque catégorie du site
def get_categories(page):

    # Récupération de la page d'accueil du site "Books to Scrape"
    home_page = requests.get(page)
    home_page.encoding = 'utf-8'
    home_soup = BeautifulSoup(home_page.content, 'html.parser')

    # Récupération de l'url de chaque catégorie
    categories_tag = home_soup.find("ul", class_="nav-list").find("ul").find_all("a")
    
    # Extraire chaque livre de chaque catégorie
    for index, category_tag in enumerate(categories_tag):

        category_href = urljoin(page,category_tag["href"])

        # Création d'un fichier .csv avec le nom de la catégorie
        with open(csv_folder + "\\" + category_tag.get_text(strip=True) + ".csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            
            # Ajout de chaque en-tête
            writer.writerow([
                "product_page_url",
                "universal_product_code",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url"])

            # Création du dossier image de la catégorie
            os.makedirs(f"{img_folder}\\{category_tag.get_text(strip=True)}")

            extract_all_books(category_href, writer)

            # Afficher l'état d'avancement du programme
            print("Catégorie " + category_tag.get_text(strip=True) + " exportée ~" + str(((index+1)*100)/len(categories_tag)) + "%")



# Extrait tous les livres d'une catégorie
def extract_all_books(category_url, writer):

    # Récupération du contenu HTML de la catégorie
    category_page = requests.get(category_url)
    category_page.encoding = 'utf-8'
    category_soup = BeautifulSoup(category_page.content, 'html.parser')

    # Récupération de chaque livre de la première page de la catégorie
    articles = category_soup.find_all("article", class_="product_pod")

    # Extraire chaque livre de chaque catégorie
    for book in articles :

        # Ajouter le livre dans le CSV via son url complet
        append_book_to_csv(urljoin(category_url, book.find("h3").a["href"]), writer)

    # Si un bouton "Next" existe, on extrait aussi les livres de la page suivante
    next_button = category_soup.find("li", class_="next")
    if next_button :
        extract_all_books(urljoin(category_url, next_button.find("a")["href"]), writer)       

# Ecrit toutes les données de chaque livre dans un fichier CSV
def append_book_to_csv(product_page_url, writer):

    # Récupération de différentes données
    book_page = requests.get(product_page_url)
    book_page.encoding = 'utf-8'
    book_soup = BeautifulSoup(book_page.content, 'html.parser')

    universal_product_code = book_soup.find("table", class_="table-striped").find_all("td")[0].text
    title = book_soup.find("h1").text
    price_including_tax = book_soup.find("table", class_="table-striped").find_all("td")[3].text
    price_excluding_tax = book_soup.find("table", class_="table-striped").find_all("td")[2].text
    
    number_available = book_soup.find("table", class_="table-striped").find_all("td")[5].text
    # Récupérer uniquement le nombre de livres disponibles
    number_available = int(''.join(filter(str.isdigit, number_available)))

    # Certains livres n'ont pas de descrition
    try:
        product_description = book_soup.find("div", id="product_description").find_next_sibling().text
    except :
        product_description = ""

    category = book_soup.find("ul", class_="breadcrumb").find_all("a")[2].text
    review_rating = book_soup.find("p", class_="star-rating")["class"][1]
    image_url = urljoin(product_page_url, book_soup.find("div", class_=['item', 'active']).find("img")["src"])

    # Ecriture de ces données dans le fichier .csv
    writer.writerow([
        product_page_url,
        universal_product_code,
        title,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_description,
        category,
        review_rating,
        image_url])
    
    # Récupération de l'image du livre
    img = requests.get(image_url)

    # Enregistrement de l'image du livre
    with open(f"{img_folder}\\{category}\\{os.path.basename(image_url)}", "wb") as image_file :
        image_file.write(img.content)



page = "https://books.toscrape.com/index.html"
get_categories(page)

print("Fin de l'exécution du programme !")