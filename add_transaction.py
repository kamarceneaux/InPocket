from tkinter import Tk, Toplevel, ttk, Frame, Label
import json
import tkinter
from tkinter.constants import X
from PIL import Image, ImageTk
import sqlite3
from windows import set_dpi_awareness
from utlities import type_of_trans, FONTTEXTCOLOR

set_dpi_awareness()

con = sqlite3.connect("InPocket-Database.db")
cur = con.cursor()


class AddTransaction(Toplevel):
    """Shows the transaction page to add transaction"""

    def __init__(self):
        Toplevel.__init__(self)
        with open("accessed_user.json") as file:
            self.user = json.load(file)
        self.first_name = self.user[0]
        self.username = self.user[1]
        self.balance = float(self.user[3])
        self.title(f"Add Transaction")
        self.geometry("650x550+400+100")
        self.resizable(False, False)
        self.iconbitmap("images/iconInPocket.ico")

        # Frames
        self.f1 = Frame(self, height=0.25 * 550)
        self.f1.pack(fill=X)

        self.f2 = Frame(self, height=0.75 * 550)
        self.f2.pack(fill=X)

        # Frame 1
        self.logo = Image.open("images/InPocketTransparent.png")
        self.resized_logo = self.logo.resize((130, 130), Image.ANTIALIAS)
        self.new_logo = ImageTk.PhotoImage(self.resized_logo)
        self.logo_lbl = Label(self.f1, image=self.new_logo)
        self.logo_lbl.place(x=50, y=5)

        self.balanceLbl = Label(
            self,
            text=f"Current Balance: ${self.balance}",
            fg=FONTTEXTCOLOR,
            font="Arial 22 bold",
        )
        self.balanceLbl.place(x=175, y=50)

        # Frame 2
        ## Empty Variables
        self.trans_type = tkinter.StringVar()

        ## User Input Section
        ### Type of transaction (DROPDOWN)
        self.typeTransLbl = Label(
            self.f2, text="Transaction Type:", fg=FONTTEXTCOLOR, font="Arial 11 bold"
        )
        self.typeTransLbl.place(x=13, y=25)
        self.typeOfTransaction = ttk.Combobox(
            self.f2,
            values=type_of_trans,
            state="readonly",
            textvariable=self.trans_type,
        )
        self.typeOfTransaction.place(x=180, y=27)
