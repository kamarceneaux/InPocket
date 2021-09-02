from tkinter import Entry, Tk, Toplevel, ttk, Frame, Label
import json
import tkinter
from tkinter.constants import X
from PIL import Image, ImageTk
import sqlite3
from windows import set_dpi_awareness
from utlities import *

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
        self.expense_or_income = tkinter.StringVar()
        self.trans_type = tkinter.StringVar()

        ## User Input Section
        ### Expense/Income (DROPDOWN)
        self.expInc = Label(
            self.f2, text="Expense/Income:", fg=FONTTEXTCOLOR, font="Arial 11 bold"
        )
        self.expInc.place(x=2, y=25)
        self.answerExpInc = ttk.Combobox(
            self.f2,
            values=exp_income,
            state="readonly",
            textvariable=self.expense_or_income,
        )
        self.answerExpInc.focus()
        self.answerExpInc.place(x=180, y=27)

        ### Type of trans
        self.type_of_transaction = Label(
            self.f2,
            text="Type of transaction: ",
            fg=FONTTEXTCOLOR,
            font="Arial 11 bold",
        )
        self.type_of_transaction.place(x=1, y=85)
        self.typeOfTransResponse = ttk.Combobox(
            self.f2,
            values=type_of_trans,
            state="readonly",
            textvariable=self.trans_type,
        )
        self.typeOfTransResponse.place(x=190, y=87)

        ### Description
        self.descriptionLbl = Label(
            self.f2, text="Description: ", fg=FONTTEXTCOLOR, font="Arial 11 bold"
        )
        self.descriptionLbl.place(x=2, y=145)
        self.description = Entry(self.f2, width=28, bd=4)
        self.description.place(x=117, y=147)

        ### Dollar entry
        self.dollarLbl = Label(
            self.f2, text="$", fg=FONTTEXTCOLOR, font="Arial 11 bold"
        )
        self.dollarLbl.place(x=2, y=205)
        self.dollarEntry = Entry(self.f2, width=6, bd=4)
        self.dollarEntry.insert(0, "00")
        self.dollarEntry.place(x=20, y=207)
