import time
from bs4 import BeautifulSoup
import requests
# import redis
from flask import Flask, jsonify

app = Flask(__name__)
# cache = redis.Redis(host='redis', port=6379)

# def get_hit_count():
#     retries = 5
#     while True:
#         try:
#             return cache.incr('hits')
#         except redis.exceptions.ConnectionError as exc:
#             if retries == 0:
#                 raise exc
#             retries -= 1
#             time.sleep(0.5)

@app.route('/')
def hello():
    return jsonify(Products=scrap_mercadolivre_best_deals())

def scrap_mercadolivre_best_deals():
    list_of_products = []
    list_of_urls = [
        'https://ofertas.mercadolivre.com.br/ofertas-da-semana',
        'https://lista.mercadolivre.com.br/_Desde_49_Deal_ofertas-da-semana',
        'https://lista.mercadolivre.com.br/_Desde_97_Deal_ofertas-da-semana'
    ]
    for url in list_of_urls:
        requested_url = requests.get(url)
        soup = BeautifulSoup(requested_url.text, "html.parser")
        all_products = soup.find_all('li', class_="results-item") 

        for item in all_products:
            separated_products = {}
            products_titles = item.find_all('h2', {'class':'item__title list-view-item-title'})

            for title in products_titles:
                product_name = title.find('span', {'class':"main-title"})
                product_name = product_name.text.replace('\n', "").strip()
                separated_products["product-name"] = product_name

            prices = item.find_all('div', {'class':'item__price'})

            for price in prices:
                price_product = price.find('span', {'class':'price__fraction'})
                price_product = price_product.text.replace('\n', "").strip()
                separated_products["price"] = "R$ "+price_product

            for link in all_products:
                link_product = link.find('a', {'class':'item__info-link'})
                link_product = str(link_product.get('href'))
                print(link_product)
                separated_products["links"] = link_product

            list_of_products.append(separated_products)
    
    return list_of_products

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
