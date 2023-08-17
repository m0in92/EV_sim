#  Copyright (c) 2023. Moin Ahmed. All Rights Reserved.
import os
import tkinter

from EV_sim.config import definations


# Global variables
doc_dir = os.path.join(definations.PROJ_DIR + '/README.md')
license_dir = os.path.join(definations.PROJ_DIR + '/LICENSE')
icon_dir = os.path.join(definations.ROOT_DIR, 'tkinter_gui', 'icon1.ico')


class MenuBarClass(tkinter.Menu):
    """Attributes and methods for the menubar."""

    def __init__(self, parent) -> None:
        super().__init__(parent)

        # option_menu = tkinter.Menu(self, tearoff="off")
        # option_menu.add_command(label="Show to two decimal")
        help_menu = tkinter.Menu(self, tearoff="off")
        help_menu.add_command(label="Documentation", command=self.show_doc_window)
        help_menu.add_command(label="Licence", command=self.show_licence_window)
        # self.add_cascade(label="Options", menu=option_menu)
        self.add_cascade(label="Help", menu=help_menu)

    def read_file(self, licence_file_dir) -> str:
        with open(licence_file_dir, 'r', encoding='utf8') as l_file:
            l_str = l_file.read()
            l_file.close()
        return l_str

    def show_licence_window(self) -> None:
        win_license = tkinter.Toplevel()
        win_license.iconbitmap(icon_dir)

        lblfme = tkinter.LabelFrame(win_license, text="Licence")
        tkinter.Label(lblfme, text=self.read_file(licence_file_dir=license_dir)).grid(row=0, column=0)

        lblfme.grid(row=0, column=0, sticky="news")

    def show_doc_window(self) -> None:
        """
        Opens a new window with the documentation.
        :return: None
        """
        # TODO: Add scroll bar.
        win_doc = tkinter.Toplevel()
        win_doc.iconbitmap(icon_dir)

        lblfme = tkinter.LabelFrame(win_doc, text="Documentation")
        tkinter.Label(lblfme, text=self.read_file(licence_file_dir=doc_dir)).grid(row=0, column=0)

        # Widget Placements
        lblfme.grid(row=0, column=0, sticky="news")