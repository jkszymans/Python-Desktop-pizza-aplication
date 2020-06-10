import sqlite3
from .settings import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait

class Model:
    def __init__(self):
        self.__data_dict=None
        self.__conn = sqlite3.connect(os.path.join(DATABASES, 'pizzaapp.db'))
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.__conn.row_factory = dict_factory
        self.__c = self.__conn.cursor()
        self.__c.execute("""CREATE TABLE IF NOT EXISTS Users (
                        name text,
                        second_name text,
                        email text,
                        phone text,
                        adress text)""")

    
    def __del__(self):
        self.__conn.close()


    def set_account_data(self, data):
        #This method sets data(which is dict) as a class field in order to
        #allow get_account_data method to easily get needed value
        self.__data_dict = data


    def get_account_data(self, param=None):
        #This method returns value from data dict based on passed param
        if param:
            return self.__data_dict[param]
        return self.__data_dict

    def save_account_to_db(self):
        #Saves dict format data
        data = [(self.get_account_data('name'), self.get_account_data('second_name'),
                self.get_account_data('email'), self.get_account_data('phone'),
                self.get_account_data('adress')),]
        self.__c.executemany('INSERT INTO Users VALUES (?,?,?,?,?)', data)
        self.__conn.commit()

    
    def fetch_selected_user_from_db(self, name):
        data_name = (name,)
        self.__c.execute("SELECT * FROM Users WHERE name=(?)", data_name)
        data = self.__c.fetchone()
        # self.set_account_data(data)
        return data


    def fetch_all_users_names_from_db(self):
        self.__c.execute("SELECT name FROM Users")
        data = self.__c.fetchall()
        names = [name['name'] for name in data]
        return names





class Pizzeria(webdriver.Firefox):
    def __init__(self):
        super().__init__(executable_path=os.path.join(GECKODRIVER, 'geckodriver.exe'))
        self.maximize_window()
        self.implicitly_wait(5)
        self.get(r'https://pizzaportal.pl')
        cookie_popup = self.find_elements(By.XPATH, r"//button[@class='button-close']")
        if cookie_popup:
            cookie_popup[0].click()


    def go_back(self):
        self.back()

    def get_closest_locals(self, adress):
        adress_form = self.find_element(By.XPATH, r"//input[@placeholder='Wpisz adres']")
        adress_form.send_keys(adress)
        adress_sugestions = self.find_elements(By.XPATH, r"//li[@class='pp_address-suggestion-item']")
        adress_sugestions[0].click()
        self.find_element(By.XPATH, r"//button[@class='accept-button']").click()
        popup = self.find_elements(By.XPATH, r"//button[@class='negative-button']")
        if popup:
            popup[0].click()
        self.__local_list = self.find_elements(By.XPATH, r"//div[@class='restaurant-list-item' and not(@class='restaurant-closed')]//descendant::h2")
        return self.__local_list

    def get_local(self):
        #this method allows to get locals based on actual url without passing adress
        self.__local_list = self.find_elements(By.XPATH, r"//div[@class='restaurant-list-item' and not(@class='restaurant-closed')]//descendant::h2")
        return self.__local_list



    def get_restaurant_menu(self, restaurant_number):
        self.__local_list[restaurant_number].click()
        product_name = self.find_elements(By.XPATH, r"//h3[@class='restaurant-menu-product-name']")
        product_description = self.find_elements(By.XPATH, r"//p[@class='restaurant-menu-product-description']")
        product_price = self.find_elements(By.XPATH, r"//div[@class='restaurant-menu-product-price']")
        product_button = self.find_elements(By.XPATH, r"//button[@class='restaurant-menu-product-button-add']")
        zipped = zip(product_name, product_description, product_price, product_button)
        data = tuple(zipped)
        return data


    def add_product_to_order(self, product):
        product[3].click()
        pop_up = self.find_elements(By.XPATH, r"//button[@class='button-add']")
        if pop_up:
            pop_up[0].click()


    def make_order(self):
        #TOO DANGEROUS :)))))))))))))))))))
        pass
