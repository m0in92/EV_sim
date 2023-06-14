#  Copyright (c) 2023. Moin Ahmed. All Rights Reserved.

from tkinter import ttk


class Ribbon(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(text="Ribbon").grid(row=0, column=0)
        self.grid(row=0, column=0)

