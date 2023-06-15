#  Copyright (c) 2023. Moin Ahmed. All Rights Reserved.

"""
Contains everything relevant to the Inputs section (leftmost frame) of the GUI.
"""
import tkinter
from tkinter import ttk
from gui import InputAndDisplayFrames, InputsDisplay



class InputsOnInputFrame(ttk.Frame):
    """
    Contains attributes and methods pertaining to the Input Frame on the Input Display.
    """
    # class variables
    lstbox_inputs_choices = ["EV", "Drive Cycle", "External Conditions"]  # all main choices in the input section

    input_display_heading1 = f"{lstbox_inputs_choices[0]}"
    input_display_heading2 = f"{lstbox_inputs_choices[1]}"
    input_display_heading3 = f"{lstbox_inputs_choices[2]}"

    def __init__(self, parent) -> None:
        """
        Class constructor
        :param parent: (InputAndDisplayFrames) InputAndDisplayFrames instance.
        """
        if isinstance(parent, InputAndDisplayFrames):
            self.parent = parent
        else:
            raise TypeError("parent needs to be InputAndDisplay Object instance.")

        super().__init__(parent)

        # Instance variables
        self.var_lstbox_inputs_choices = tkinter.StringVar()
        self.var_lstbox_inputs_choices.set(InputsOnInputFrame.lstbox_inputs_choices)

        ttk.Label(self, text="Inputs", font=VehicleDynamicsApp.heading_style).grid(row=0, column=0, sticky="news")
        self.lstbox_inputs = tkinter.Listbox(self, width=50, listvariable=self.var_lstbox_inputs_choices,
                                             selectmode="single", exportselection=False,
                                             height=len(self.lstbox_inputs_choices))

        self.lstbox_inputs.bind('<<ListboxSelect>>', self.set_lstbox_input_user_choice)

        self.lstbox_inputs.grid(row=1, column=0, sticky="news")
        self.grid(row=0, column=0)

    def set_lstbox_input_user_choice(self, event) -> None:
        user_choice = self.lstbox_inputs.get(self.lstbox_inputs.curselection())
        InputsDisplay(self.parent.fme_display, text=user_choice, parent_obj=self.parent)