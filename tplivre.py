import requests
from bs4 import BeautifulSoup
import pandas as pd

# Définir la fonction pour extraire les informations d'une page spécifique
def extract_books_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []

    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        rating = book.p['class'][1]
        price = book.find('p', class_='price_color').text
        rating_value = convert_rating_to_number(rating)
        
        books.append({
            'title': title,
            'rating': rating_value,
            'price': price
        })

    return books

# Convertir le rating en nombre
def convert_rating_to_number(rating):
    ratings = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    return ratings.get(rating, 0)

# Extraire les informations des 10 premières pages
def scrape_books(base_url, num_pages):
    all_books = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}catalogue/page-{page}.html"
        books_on_page = extract_books_from_page(url)
        all_books.extend(books_on_page)

    return all_books

# Filtrer les livres ayant au moins 3 étoiles
def filter_books_by_rating(books, min_rating=3):
    return [book for book in books if book['rating'] >= min_rating]

# URL de base du site
base_url = 'https://books.toscrape.com/'

# Scrapper les livres
all_books = scrape_books(base_url, 10)
filtered_books = filter_books_by_rating(all_books)

# Convertir les résultats en DataFrame et sauvegarder en CSV
df_books = pd.DataFrame(filtered_books)
df_books.to_csv('filtered_books.csv', index=False)

print("Scraping terminé. Les résultats sont enregistrés dans 'filtered_books.csv'.")
