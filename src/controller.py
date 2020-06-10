import tkinter as tk
from .model import Model, Pizzeria
from .view import *

class Controller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PizzaApp")
        self.__model = Model()
        self.__pizzeria = Pizzeria()
        self.__frames = {}
        for F in (StartPage, CallPage, RegisterPage):
            page_name = F.__name__
            frame = F(self)
            self.__frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.startpage_func()


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.__frame = self.__frames[page_name]
        self.__frame.tkraise()


    def startpage_func(self):
        self.show_frame("StartPage")
        names = self.__model.fetch_all_users_names_from_db()
        self.__frame.set_dropdown_names(names)


    def dropdown_func(self, name):
        #if customer will choose one of the options from dropdown, callpage_func starts
        if not name=='--||--':
            selected_user = self.__model.fetch_selected_user_from_db(name)
            local_list = self.__pizzeria.get_closest_locals(selected_user['adress'])
            self.show_frame('CallPage')
            self.__frame.set_pizzeria_list(local_list)



    def back_to_pizzeria(self):
        self.__pizzeria.go_back()
        local_list = self.__pizzeria.get_local()
        self.__frame.destroy()
        self.__frames['CallPage'] = CallPage(self)
        self.__frames['CallPage'].grid(row=0, column=0, sticky="nsew")
        self.show_frame('CallPage')
        self.__frame.set_pizzeria_list(local_list)        


    def display_pizzeria_menu(self, pizzeria_count):
       pizzeria_menu = self.__pizzeria.get_restaurant_menu(pizzeria_count)
       self.__frame.set_menu_list(pizzeria_menu)       


    def add_product_to_order_func(self, product):
        self.__pizzeria.add_product_to_order(product)
        self.__frame.display_product_to_order(product)


    def register_func(self):
        customer_info = self.__frame.get_data_from_display()
        if customer_info:
            self.__model.set_account_data(customer_info)
            self.__model.save_account_to_db()
            self.startpage_func()

    
