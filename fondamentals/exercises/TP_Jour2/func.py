""" module func: which contains function to load data from API and write on SQLite3 """

import requests
from sqlite3 import Error

from wow.classes import Product


def load_data(category, cursor):
    """Function which take a category from Open Food Facts in parameter
    and load data in an Product table for each page of the category"""

    url_begin = 'https://fr.openfoodfacts.org/categorie'
    nb_page = 1
    url_end = 'json'

    while nb_page <= 4:
        # format url
        url = "{}/{}/{}.{}".format(url_begin, category, nb_page, url_end)

        response = requests.get(url)
        products = response.json()

        p_name = ""
        n_grade = ""
        cat_name = ""
        product = Product()

        # iterate through the json request
        # p is each product we get from API
        for p in products["products"]:

            # try to collect infos, we need ..
            try:
                p_name = p["product_name_fr"]
                n_grade = p["nutrition_grades"]
                cat_name = p["pnns_groups_2"]
                url = p["url"]
                
            # to avoid empty field
            except KeyError:
                pass

            # Use methods of the Product Class to write in DB
            product.add(p_name, n_grade, cat_name, url, cursor)

        nb_page = nb_page + 1