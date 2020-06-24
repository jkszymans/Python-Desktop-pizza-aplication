import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import re
from .model import Model
from .settings import *

class StartPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.__controller = master
        self.__names = []
        self.__set_view()


    def __set_view(self):
        def set_background_photo():
            self.background_photo = ImageTk.PhotoImage(Image.open(os.path.join(MEDIA, 'pizza.png')))
            background_label = tk.Label(self, image=self.background_photo, height=434, width=960)
            background_label.grid(row=0, column=0, columnspan=20, rowspan=10)
        
        
        def set_buttons_labels_entries():
            tk.Label(self, text='Your name!', background='#FF9966').grid(row=7, column=14)
            tk.Label(self, text='First time here? Sign in!', background='#FF9966').grid(row=8, column=14)     
            first_view_button = tk.Button(self, text='Register', background='#FF9966', width=15, command=lambda: self.__controller.show_frame("RegisterPage"))
            first_view_button.grid(row=8, column=16)


        def set_dropdown():
            self.customer_value = tk.StringVar()
            self.customer_value.set('Select your name')
            self.__names.append('--||--')
            self.drop_down = tk.OptionMenu(self, self.customer_value, *self.__names, command=self.__controller.dropdown_func)
            self.drop_down.grid(row=7, column=16)

        set_background_photo()
        set_buttons_labels_entries()
        set_dropdown()


    def set_dropdown_names(self, names):
        self.__names = names
        self.__names.append('--||--')
        #update
        menu = self.drop_down["menu"]
        menu.delete(0, "end")
        for string in self.__names:
            menu.add_command(label=string, command=lambda value=string: self.__controller.dropdown_func(value))

        







class CallPage(tk.Frame):

    limit_of_pizzerias_on_page = 5
    limit_of_products_on_page = 5
    
    def __init__(self, parent):
        super().__init__(parent)        
        self.__controller = parent
        self.__pizzeria_list = None
        self.__order_list = []
        self.__menu_list = None
        self.__displayed_products_list = []
        self.__order_product_label_list = []
        self.__order_product_count = 1
        self.__actual_pizzerias_page = 1
        self.__actual_menu_page = 1
        self.__total_cost = 0.0

        self.__pizzerias_frame = tk.Frame(self)
        self.__order_frame = tk.LabelFrame(self, width=300, height=460, background='#FF9900')
        self.__menu_frame = tk.Frame(self, bg='')
        self.__background_photo = ImageTk.PhotoImage(Image.open(os.path.join(MEDIA, 'callpizza.png')))
        background_label = tk.Label(self.__pizzerias_frame, image=self.__background_photo, height=434, width=730)
        background_label.grid(row=0, column=0, columnspan=4, rowspan=10)
        self.__background_photo_2 = ImageTk.PhotoImage(Image.open(os.path.join(MEDIA, 'bla.png')))
        background_label = tk.Label(self.__menu_frame, image=self.__background_photo_2, height=434, width=730)
        background_label.grid(row=0, column=0, columnspan=4, rowspan=10)

        self.__menu_frame.grid(row=0, column=0, sticky = "nsew")
        self.__pizzerias_frame.grid(row=0, column=0, sticky = "nsew")
        self.__pizzerias_frame.tkraise()
        self.__order_frame.grid(row=0, column=1, sticky = "nsew")
            


        def set_buttons_labels_entries():
            self.__next_page_pizzeria_button = tk.Button(self.__pizzerias_frame, text='Next Page', background='#FF9966', width=15, command=self.__next_pizzeria_page_func)
            self.__next_page_pizzeria_button.grid(row=8,column=3, rowspan=3, sticky = "nsew")
            self.__previous_page_pizzeria_button = tk.Button(self.__pizzerias_frame, text='Previous Page', state=tk.DISABLED, background='#FF9966', width=15, command=self.__previous_pizzeria_page_func)
            self.__previous_page_pizzeria_button.grid(row=8,column=2, rowspan=3, sticky = "nsew")

            self.__next_page_menu_button = tk.Button(self.__menu_frame, text='Next Page', background='#FF9966', width=15, command=self.__next_menu_page_func)
            self.__next_page_menu_button.grid(row=8,column=3, rowspan=3, sticky = "nsew")
            self.__previous_page_menu_button = tk.Button(self.__menu_frame, text='Previous Page', state=tk.DISABLED, background='#FF9966', width=15, command=self.__previous_menu_page_func)
            self.__previous_page_menu_button.grid(row=8,column=2, rowspan=3, sticky = "nsew")

            tk.Label(self.__order_frame, text='Twoje zamówienie', font='Helvetica 18 bold', background='#FF9900').grid(row=0, column=0, columnspan=2)
            make_order_button = tk.Button(self.__order_frame, text='Eat Pizza!', state=tk.DISABLED, command=self.__make_order, background='#CC6600')
            make_order_button.grid(column=0, row=9, columnspan=2, rowspan=3, sticky = "nsew")

            back_to_pizzeria_button = tk.Button(self.__menu_frame, text='Choose different local', background='#FF9966', command=self.__controller.back_to_pizzeria)
            back_to_pizzeria_button.grid(column=0, row=8, columnspan=2, rowspan=3, sticky = "nsew")

            title_label = tk.Label(self.__menu_frame, text='Nazwa', font='Helvetica 18 bold').grid(column=0, row=0, sticky = "nsew", rowspan=2)
            description_label = tk.Label(self.__menu_frame, text='Opis', font='Helvetica 18 bold').grid(column=1, row=0, sticky = "nsew", rowspan=2)
            price_label = tk.Label(self.__menu_frame, text='Cena', font='Helvetica 18 bold').grid(column=2, row=0, sticky = "nsew", rowspan=2)
            button_label = tk.Label(self.__menu_frame, text='Przycisk', font='Helvetica 18 bold').grid(column=3, row=0, sticky = "nsew", rowspan=2)

            name_of_pizzeria_label = tk.Label(self.__pizzerias_frame, text='Wybierz Lokal', font='Helvetica 18 bold', background='#FF9966').grid(row=0, column=0, sticky = "nsew", rowspan=2, columnspan=2)

        def set_weight_frame():
            for r in range(1):
                self.rowconfigure(r, weight=1)  
            for c in range(2):
                self.columnconfigure(c, weight=1)

            for r in range(10):
                self.__menu_frame.rowconfigure(r, weight=1)  
                self.__pizzerias_frame.rowconfigure(r, weight=1)    
                self.__order_frame.rowconfigure(r, weight=1)  
            for c in range(4):
                self.__menu_frame.columnconfigure(c, weight=1)
                self.__pizzerias_frame.columnconfigure(c, weight=1)
            for c in range(2):
                self.__order_frame.columnconfigure(c, weight=1)
                
        
        set_buttons_labels_entries()
        set_weight_frame()


    def set_pizzeria_list(self, pizzeria_list):
        self.__pizzeria_list = pizzeria_list
        pizzeria_objects = len(self.__pizzeria_list)
        self.max_pizzeria_page = pizzeria_objects // (CallPage.limit_of_pizzerias_on_page)
        if (pizzeria_objects % CallPage.limit_of_pizzerias_on_page) >= 1: self.max_pizzeria_page += 1
        self.__display_pizzeria_list()


    def set_menu_list(self, menu):
        self.__menu_list = menu
        menu_objects = len(self.__menu_list)
        self.max_menu_page = menu_objects // (CallPage.limit_of_products_on_page)
        if (menu_objects % CallPage.limit_of_products_on_page) >= 1: self.max_menu_page += 1
        self.__display_menu()
        self.__menu_frame.tkraise()


    def __previous_menu_page_func(self):
        self.__actual_menu_page -= 1
        for product in self.__displayed_products_list:
            product[0].destroy()
            product[1].destroy()
            product[2].destroy()
            product[3].destroy()    
    
        if self.__actual_menu_page == 1:
            self.__previous_page_menu_button.config(state=tk.DISABLED)
        else:
            self.__previous_page_menu_button.config(state=tk.NORMAL)
        if self.max_menu_page == self.__actual_menu_page:
            self.__next_page_menu_button.config(state=tk.DISABLED)
        else:
            self.__next_page_menu_button.config(state=tk.NORMAL)

        self.__display_menu()


    def __next_menu_page_func(self):
        self.__actual_menu_page += 1
        for product in self.__displayed_products_list:
            product[0].destroy()
            product[1].destroy()
            product[2].destroy()
            product[3].destroy() 

        if self.__actual_menu_page == 1:
            self.__previous_page_menu_button.config(state=tk.DISABLED)
        else:
            self.__previous_page_menu_button.config(state=tk.NORMAL)
        if self.max_menu_page == self.__actual_menu_page:
            self.__next_page_menu_button.config(state=tk.DISABLED)
        else:
            self.__next_page_menu_button.config(state=tk.NORMAL)

        self.__display_menu()


    def __previous_pizzeria_page_func(self):
        self.__actual_pizzerias_page -= 1
        for button in self.__pizzeria_button_list:
            button.destroy()
        self.__display_pizzeria_list()
        if self.__actual_pizzerias_page == 1:
            self.__previous_page_pizzeria_button.config(state=tk.DISABLED)
        else:
            self.__previous_page_pizzeria_button.config(state=tk.NORMAL)
        if self.max_pizzeria_page == self.__actual_pizzerias_page:
            self.__next_page_pizzeria_button.config(state=tk.DISABLED)
        else:
            self.__next_page_pizzeria_button.config(state=tk.NORMAL)



    def __next_pizzeria_page_func(self):
        self.__actual_pizzerias_page += 1
        for button in self.__pizzeria_button_list:
            button.destroy()
        if self.__actual_pizzerias_page == 1:
            self.__previous_page_pizzeria_button.config(state=tk.DISABLED)
        else:
            self.__previous_page_pizzeria_button.config(state=tk.NORMAL)
        if self.max_pizzeria_page == self.__actual_pizzerias_page:
            self.__next_page_pizzeria_button.config(state=tk.DISABLED)
        else:
            self.__next_page_pizzeria_button.config(state=tk.NORMAL)
        self.__display_pizzeria_list()



    def display_product_to_order(self, product):
        def calculate_price():
            single_product_price = ""
            # it can be for example 20 zł\n15zł\n-20%discount
            li = product[2].text.split('zł')
            # we want price in the middle for example 15
            for char in li[-2]:
                if char.isdigit():
                    single_product_price += char
                elif char == ',':
                    single_product_price += '.'

            return float(single_product_price)
        
        product_price = calculate_price()
        self.__total_cost += product_price
        self.__order_list.append(product)
        order_product_label = tk.Label(self.__order_frame, text=self.__order_list[-1][0].text, background='#FF9900')
        order_product_label.grid(row=self.__order_product_count, column=0, columnspan=2)
        
        full_price_label = tk.Label(self.__order_frame, text=f"Całkowity koszt: {self.__total_cost}zł", background='#FF9900')
        full_price_label.grid(row=8, column=0, columnspan=2, sticky = "ew")
        self.__order_product_label_list.append(order_product_label)
        self.__order_product_label_list.append(full_price_label)
        self.__order_product_count += 1


                  
    def __display_pizzeria_list(self):
        self.__pizzeria_button_list = []
        row_count = 2
        for i in range(self.__actual_pizzerias_page * CallPage.limit_of_pizzerias_on_page - CallPage.limit_of_pizzerias_on_page, self.__actual_pizzerias_page * CallPage.limit_of_pizzerias_on_page):
            if len(self.__pizzeria_list) > i:
                button = tk.Button(self.__pizzerias_frame, text=self.__pizzeria_list[i].text, command=lambda i=i: self.__controller.display_pizzeria_menu(i), background='#FF6633')
                button.grid(row=row_count, column=1, columnspan=2)
                self.__pizzeria_button_list.append(button)
                row_count += 1



    def __display_menu(self):
    #((name1, description1, price1, button1),(name2, description2, price2, button2)...)
        row = 2
        self.__displayed_products_list = []
        for i in range(self.__actual_menu_page * CallPage.limit_of_products_on_page - CallPage.limit_of_products_on_page, self.__actual_menu_page * CallPage.limit_of_products_on_page):
            if len(self.__menu_list) > i:
                product_title = tk.Label(self.__menu_frame, text=self.__menu_list[i][0].text, wraplength=250, background='#FF9966')
                product_description = tk.Label(self.__menu_frame, text=self.__menu_list[i][1].text, wraplength=300, background='#FF9966')
                product_price = tk.Label(self.__menu_frame, text=self.__menu_list[i][2].text, background='#FF9966')
                product_button = tk.Button(self.__menu_frame, text='Dodaj', command=lambda i=i: self.__controller.add_product_to_order_func(self.__menu_list[i]), background='#FF9966')
                product_title.grid(row=row, column=0)
                product_description.grid(row=row, column=1)
                product_price.grid(row=row, column=2)
                product_button.grid(row=row, column=3)
                product_tuple = (product_title, product_description, product_price, product_button)
                self.__displayed_products_list.append(product_tuple)
                row += 1



    def __make_order(self):
        #THIS METHOD WILL ORDER PIZZA
        #I WON'T IMPLEMENT IT, BECAUSE IT'S TOO DANGEROUS
        pass


class RegisterPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__controller = parent
        self.__setbackground()
        self.__customerinfo()
        register_button = tk.Button(self, text='Register', command=self.__controller.register_func,
                                         background='#FF9966')
        register_button.grid(row=9, column=2)
        back_button = tk.Button(self, text='Back', command=self.__controller.startpage_func,
                                 background='#FF9966')
        back_button.grid(row=9, column=1)
        self.error_label=None


    def __setbackground(self):
        self.background_photo = ImageTk.PhotoImage(Image.open(os.path.join(MEDIA, 'pizzaregister.png')))
        background_label = tk.Label(self, image=self.background_photo,
                                     height=434, width=960)
        background_label.grid(row=0, column=0, columnspan=10, rowspan=10)


    def __makeentry(self, parent, caption, labelrow, labelcolumn, width=None, **options):
        tk.Label(self, text=caption, background='#FF9966').grid(row=labelrow, column=labelcolumn)
        entry = tk.Entry(parent, **options)
        if width:
            entry.config(width=width)
        entry.grid(row=labelrow, column=labelcolumn+1)
        return entry


    def __customerinfo(self):
        self.name_entry = self.__makeentry(self, "First Name", 1, 1)
        self.second_name_entry = self.__makeentry(self, "Second Name", 2, 1)
        self.email_entry = self.__makeentry(self, "Email", 3, 1)
        self.phone_entry = self.__makeentry(self, "Phone number", 4, 1)
        self.adress_entry = self.__makeentry(self, "Adress", 5, 1)


    def __validate_data(self):
        def name_validation(name):
            if not re.match(r"^[A-Z][a-z]+$", name):
                raise ValueError("Invalid name")

        def second_name_validation(second_name):
            if not re.match(r"^[A-Z][a-z]+$", second_name):
                raise ValueError("Invalid second name")            
        
        def email_validation(email):
            if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]+$", email):
                raise ValueError("Invalid email :: blabla123@gmail.com")

        def phone_validation(phone):
            if not re.match(r"^\d{9}$", phone):
                raise ValueError("Invalid telephone number :: 654236123")

#         def adress_validation(adress):
#             if not re.match(r"^[a-zA-Z1-9\ \,\.-]+$", adress):
#                 raise ValueError("Invalid adress")


        if self.error_label:
            self.error_label.destroy()
        try:
            name_validation(self.name_entry.get())
            second_name_validation(self.second_name_entry.get())
            email_validation(self.email_entry.get())
            phone_validation(self.phone_entry.get())
#             adress_validation(self.adress_entry.get())

        except ValueError as err:
            self.error_label = tk.Label(self, text=err, background='#FF9966')
            self.error_label.grid(row=6, column=1, columnspan=4)
            return False
        else:
            return True


    def get_data_from_display(self):
        if self.__validate_data():
            customer_info = {}
            customer_info['name']=self.name_entry.get()
            customer_info['second_name']=self.second_name_entry.get()
            customer_info['email']=self.email_entry.get()
            customer_info['phone']=self.phone_entry.get()
            customer_info['adress']=self.adress_entry.get()
            return customer_info




