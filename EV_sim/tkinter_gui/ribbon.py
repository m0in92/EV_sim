#  Copyright (c) 2023. Moin Ahmed. All Rights Reserved.
import tkinter
from tkinter import ttk


class Ribbon(ttk.Frame):
    dict_bttn_text = {'EV': ['Add EV'], 'DriveCycle': ['Add Drivecycle'],
                      'External Conditions': ['Edit External Conditions']}

    def __init__(self, parent):
        super().__init__(parent)

        # Instance variables
        self.user_bbtn_choice = tkinter.StringVar()
        self.user_bbtn_choice.set(list(self.dict_bttn_text.keys())[0]) # initialize user selection of the main menu to
        # the first available choice.

        # Widgets
        fme_top_menu = ttk.Frame(self)
        dict_bttn = {}
        for col_num, text_ in enumerate(self.dict_bttn_text.keys()):
            dict_bttn[f'bttn_{text_}'] = ttk.Button(fme_top_menu, text=text_,
                                                    command=lambda text=text_: self.show_sub_menu(text))
            dict_bttn[f'bttn_{text_}'].grid(row=0, column=col_num, sticky='news')
        self.show_sub_menu(text=self.user_bbtn_choice.get())

        # grid layout
        fme_top_menu.grid(row=0, column=0, columnspan=len(self.dict_bttn_text.keys()))
        self.grid(row=0, column=0, sticky='news')

    def show_sub_menu(self, text):
        fme_sub_menu = ttk.Frame(self, width=100)
        if not isinstance(text, str):
            raise TypeError('submenu needs a input of string type.')
        for col_num, sub_menu_bttn_ in enumerate(self.dict_bttn_text[text]):
            ttk.Button(fme_sub_menu, width=25, text=sub_menu_bttn_, command=lambda text=sub_menu_bttn_: self.sub_menu_cmd(text))\
                .grid(row=1, column=col_num)
        fme_sub_menu.grid(row=1, column=0, columnspan=len(self.dict_bttn_text[text]))

    def sub_menu_cmd(self, text):
        print(text)

