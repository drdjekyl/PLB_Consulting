""" module classes: which contain Product Class """

from sqlite3 import Error


ADD_QUERY = "insert into product values (?, ?, ?, ?)"


class Product():
    '''To enable the general use of the Product class
     for basic filling as well as for using the program,
     the constructor is empty and two functions are implemented
     add (fill in the base)'''

    def __init__(self):
        # Cronstuctor with empty attributes

        self.p_name = ""
        self.n_grade = ""
        self.cat_name = ""
        self.url = ""
        self._id = 0
        self.category_id = 0

    def add(self, p_name, n_grade, cat_name, url, cursor):
        '''Function used to fill database with add_product from queries module'''
        self.p_name = p_name
        self.n_grade = n_grade
        self.cat_name = cat_name
        self.url = url

        product_data = (self.p_name, self.n_grade, self.cat_name, self.url)

        
        try:   
            cursor.execute(ADD_QUERY, product_data)
            
            #cursor.execute(add_product, product_data)
        except Error as e:
            print("Error is the following: {}".format(e))
            pass
