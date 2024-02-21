import requests
from bs4 import BeautifulSoup
import csv
import os

def scrap(url1):
    x=0
    # URL de la página web
    url = "https://books.toscrape.com/catalogue/"

    # Realizar una solicitud GET a la página web
    
    response = requests.get(url1)


    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        # Crear un objeto BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar todos los elementos de libro
        books = soup.find_all("article", class_="product_pod")

        # Crear un archivo CSV para escribir los datos
        with open("sample.csv", "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Título", "Precio", "Rating", "Disponibilidad", "UPC", "Descripcion"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')

            # Comprobar si el archivo está vacío antes de escribir la cabecera
            if os.stat("sample.csv").st_size == 0:
                writer.writeheader()

            writer.writeheader()

            for book in books:
                # Extraer el título del libro
                title = book.find("h3").find("a")["title"]

                # Buscar el precio del libro
                price_element = book.find("p", class_="price_color")
                price = price_element.text if price_element else "Precio no disponible"

                # Extraer el rating del libro
                rating_element = book.find("p", class_="star-rating")
                rating = rating_element["class"][1] if rating_element else "Rating no disponible"

                # Acceder a la URL del libro para obtener la descripción del producto
                book_url = url + book.find("h3").find("a")["href"]
                book_response = requests.get(book_url)

                #book_soup = None
                if book_response.status_code == 200:
                    x=x+1
                    print(x)
                    book_soup = BeautifulSoup(book_response.text, "html.parser")
                    product_description = book_soup.find("meta", {"name": "description"})["content"]

                else:
                    product_description = "F"
                # Buscar la disponibilidad del libro
                availability_element = book_soup.find("th", string="Availability")
                availability = availability_element.find_next("td").get_text() if availability_element else "Disponibilidad no disponible"

                upc_element = book_soup.find("th", string="UPC")
                upc = upc_element.find_next_sibling("td").text if upc_element else "UPC no disponible"
                # Escribir los detalles del libro en el archivo CSV
                writer.writerow({
                    "Título": title,
                    "Precio": price,
                    "Rating": rating,
                    "Disponibilidad": availability,
                    "UPC":upc,
                    "Descripcion": product_description
                })

        print("Los datos se han guardado en libros.csv")
    else:
        print("Error al acceder a la página web")



for i in range(1, 2):
    url = f'https://books.toscrape.com/catalogue/page-{i}.html'
    print("Scraping: "+url)
    scrap(url)
    
