""" MAIN PROGRAM """

import func
import sqlite3 as db
from sqlite3 import Error

TABLE_CREATION = "CREATE TABLE product (name varchar(150), nutriscore char(1), category_name varchar(80), url text)"


if __name__ == "__main__":

    # Define the connexion
    with db.connect("alimentation.db") as cnx:

        # Store the cursor
        cursor = cnx.cursor()
        
        try:
            cursor.execute(TABLE_CREATION)
            print('Table Product is created')
            
        except Error:
            print('Table Product is already existing')
            
        # Load JSON from Openfoodfacts API
        func.load_data("fruits-secs", cursor)
        #func.load_data("produits-a-tartiner", cursor)
        #func.load_data("cones-et-batonnets-surgeles", cursor)
        #func.load_data("pizzas-et-tartes-surgelees", cursor)
        #func.load_data("jambons-de-paris", cursor)


        # Make sure to commit data to database
        cnx.commit()
        print('...........................................')
        print('Data from OpenFoodFact are now pushed on DB')
        print('...........................................')
        print('\n')
        print('...........................................')
        print('   Display the ten first elements in DB    ')
        print('...........................................')
        print('\n')       
        
        try:
            cursor.execute("SELECT product.name, product.nutriscore FROM product")

            for idx, row in enumerate(cursor):
                if idx < 10:
                    print(row)

        except Error as e:
            print("Error is the following: {}".format(e))