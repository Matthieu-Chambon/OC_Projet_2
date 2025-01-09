# Imports nécessaires au fonctionnement du programme
import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

print("Phase 1")

# f = open("article.txt", "w", encoding="utf-8")
# f.write(str(articles[1]))
# f.close()

file = "phase_1.csv"

# Suppression du fichier phase_1.csv s'il existe afin de le regénérer
if os.path.exists(file):
    os.remove(file)
    print(f"The file '{file}' has been deleted.")
else:
    print(f"The file '{file}' does not exist.")

# Création du fichier .csv avec chaque en-tête
with open(file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=";")
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


# Extrait tous les livres d'une catégorie
def get_categories(page):

    # Récupération de la page d'accueil du site "Books to Scrape"
    home_page = requests.get(page)
    home_page.encoding = 'utf-8'
    home_soup = BeautifulSoup(home_page.content, 'html.parser')

    # Récupération de l'url de chaque catégorie
    categories_tag = home_soup.find("ul", class_="nav-list").find("ul").find_all("a")
    categories_href = [urljoin("https://books.toscrape.com/index.html",a["href"]) for a in categories_tag]

    # Extraire chaque livre de chaque catégorie
    for category_url in categories_href :

        extract_all_books(category_url)



# Extrait tous les livres d'une catégorie
def extract_all_books(category_url):

    # Récupération du contenu HTML de la catégorie
    category_page = requests.get(category_url)
    category_page.encoding = 'utf-8'
    category_soup = BeautifulSoup(category_page.content, 'html.parser')

    # Récupération de chaque livre
    articles = category_soup.find_all("article", class_="product_pod")

    # Ouverture du CSV
    file = "phase_1.csv"
    with open(file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        # Extraire chaque livre de chaque catégorie
        for book in articles :

            # Ajouter le livre dans le CSV via son url complet
            append_book_to_csv(urljoin(category_url, book.find("h3").a["href"]), writer)

            
            
# Ecrit toutes les données de chaque livre dans un fichier CSV
def append_book_to_csv(book_url, writer):

    # Récupération de différentes données
    product_page_url = book_url

    book_page = requests.get(product_page_url)
    book_page.encoding = 'utf-8'
    book_soup = BeautifulSoup(book_page.content, 'html.parser')

    universal_product_code = book_soup.find("table", class_="table-striped").find_all("td")[0].text
    title = book_soup.find("h1").text
    print(title)
    price_including_tax = book_soup.find("table", class_="table-striped").find_all("td")[3].text
    price_excluding_tax = book_soup.find("table", class_="table-striped").find_all("td")[2].text
    number_available = book_soup.find("table", class_="table-striped").find_all("td")[5].text

    # Certains livres n'ont pas de descrition (ex : https://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html)
    try:
        product_description = book_soup.find("div", id="product_description").find_next_sibling().text
    except :
        product_description = ""

    category = book_soup.find("ul", class_="breadcrumb").find_all("a")[2].text
    review_rating = book_soup.find("p", class_="star-rating")["class"][1]
    image_url = urljoin(product_page_url, book_soup.find("div", class_=['item', 'active']).find("img").src)

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

page = "https://books.toscrape.com/index.html"
get_categories(page)