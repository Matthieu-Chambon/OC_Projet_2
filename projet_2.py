# Imports nécessaires au fonctionnement du programme
import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

print("Phase 1")

# Récupération de la page d'accueil du site "Books to Scrape" (Science Fiction)
home_url = "https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html"
home_page = requests.get(home_url)
home_page.encoding = 'utf-8'
home_soup = BeautifulSoup(home_page.content, 'html.parser')

# Récupération de chaque livre
articles = home_soup.find_all("article", class_="product_pod")

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

# Ajout des en-têtes
csv_headline = [
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"]

# Création du fichier .csv
with open(file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(csv_headline)

    # Pour chaque livre (element <article>)
    for article in articles :

        # Récupération de différentes données
        relative_url = article.find("h3").a["href"]
        product_page_url = urljoin(home_url, relative_url)

        book_page = requests.get(product_page_url)
        book_page.encoding = 'utf-8'
        book_soup = BeautifulSoup(book_page.content, 'html.parser')

        universal_product_code = book_soup.find("table", class_="table-striped").find_all("td")[0].text
        title = book_soup.find("h1").text
        price_including_tax = book_soup.find("table", class_="table-striped").find_all("td")[3].text
        price_excluding_tax = book_soup.find("table", class_="table-striped").find_all("td")[2].text
        number_available = book_soup.find("table", class_="table-striped").find_all("td")[5].text
        product_description = book_soup.find("div", id="product_description").find_next_sibling().text
        category = book_soup.find("table", class_="table-striped").find_all("td")[1].text
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
