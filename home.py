from tkinter import Button, Toplevel, font, ttk, Label, Frame, Entry, messagebox
import tkinter
from tkinter.constants import X
from utlities import FONTTEXTCOLOR, random_money_quotes, exp_income, type_of_trans
from windows import set_dpi_awareness
from PIL import ImageTk, Image
import json
import random
from add_transaction import AddTransaction
import sqlite3

set_dpi_awareness()


class HomePage(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        with open("accessed_user.json") as file:
            self.user = json.load(file)
        self.first_name = self.user[0]
        self.balance = float(self.user[3])
        self.title(f"{self.user[0]}'s Homepage")
        self.geometry("650x550+400+100")
        self.resizable(False, False)
        self.iconbitmap("images/iconInPocket.ico")

        # Frames
        self.f1 = Frame(self, height=0.25 * 550)
        self.f1.pack(fill=X)

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill=X)

        self.f2 = Frame(self, height=0.55 * 550)
        self.f2.pack(fill=X)

        self.sep2 = ttk.Separator(self, orient="horizontal")
        self.sep2.pack(fill=X)

        self.f3 = Frame(self, height=0.20 * 550)
        self.f3.pack(fill=X)

        # Heading Frame
        ## Opens image
        self.logo = Image.open("images/InPocketTransparent.png")
        self.resized_logo = self.logo.resize((130, 130), Image.ANTIALIAS)
        self.new_logo = ImageTk.PhotoImage(self.resized_logo)
        self.logo_lbl = Label(self.f1, image=self.new_logo)
        self.logo_lbl.place(x=40, y=5)

        ## Show current balance
        self.balanceLbl = Label(
            self,
            text=f"Current Balance: ${self.balance}",
            fg=FONTTEXTCOLOR,
            font="Arial 16 bold",
        )
        ## Show user's name
        self.greetUser = Label(
            self,
            text=f"Hello {self.first_name.title()}!",
            fg=FONTTEXTCOLOR,
            font="Arial 11 bold",
        )

        self.balanceLbl.place(x=165, y=60)
        self.greetUser.place(x=450, y=110)

        # Frame 2
        ## Add Transaction Button (button will launch new window, and terminate this window)
        add_transaction = Button(
            self.f2,
            text="Add Transaction",
            width=20,
            bd=4,
            font="Arial 16 bold",
            command=self.add_transaction,
        )
        add_transaction.place(x=150, y=80)
        ## View past transactions button (read add transaction button)
        view_transactions = Button(
            self.f2, text="View Past Transactions", width=20, bd=4, font="Arial 16 bold"
        )
        view_transactions.place(x=150, y=160)
        # Frame 3
        ## Load in quotes
        money_quotes = random_money_quotes
        display_quote = random.choice(money_quotes)
        ## Then show a RANDOM quote to display
        self.showQuote = Label(self.f3, text=display_quote, font="Arial 8 underline")
        self.showQuote.pack(side="bottom")

    def add_transaction(self):
        addTransactionPage = AddTransaction()
        # Eventually kill the homepage
        self.destroy()
        addTransactionPage.lift()


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
        self.answerExpInc.place(x=160, y=27)

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
        self.typeOfTransResponse.place(x=178, y=87)

        ### Description
        self.descriptionLbl = Label(
            self.f2,
            text="Description: ",
            fg=FONTTEXTCOLOR,
            font="Arial 11 bold",
        )
        self.descriptionLbl.place(x=2, y=145)
        self.description = Entry(self.f2, width=28, bd=4)
        self.description.place(x=117, y=147)

        ### Dollar entry
        self.dollarLbl = Label(
            self.f2, text="$", fg=FONTTEXTCOLOR, font="Arial 11 bold"
        )
        self.dollarLbl.place(x=85, y=205)
        self.dollarEntry = Entry(self.f2, width=6, bd=6)
        self.dollarEntry.insert(0, "00")
        self.dollarEntry.place(x=100, y=205)

        ### Cents entry
        self.centLbl = Label(self.f2, text=".", fg=FONTTEXTCOLOR, font="Arial 11 bold")
        self.centLbl.place(x=163, y=208)
        self.centEntry = Entry(self.f2, width=6, bd=6)
        self.centEntry.insert(0, "00")
        self.centEntry.place(x=180, y=205)

        ### Submit button
        submit = Button(
            self.f2,
            text="Submit",
            width=12,
            bd=4,
            font="Arial 16 bold",
            command=self.finalizeSubmission,
        )
        submit.place(x=80, y=250)

    def finalizeSubmission(self):
        # Entry fields for database
        expen_incon_entry = self.expense_or_income.get()
        typeTrans = self.trans_type.get()
        descriptionOfficialEntry = self.description.get()
        dollarOfficialEntry = self.dollarEntry.get()
        centOfficialEntry = self.centEntry.get()

        if (
            expen_incon_entry
            and typeTrans
            and descriptionOfficialEntry
            and dollarOfficialEntry
            and centOfficialEntry != ""
        ):
            # Convert string to numerical
            try:
                dollarOfficialEntry = int(dollarOfficialEntry)
                print(dollarOfficialEntry)
            except ValueError:
                messagebox.showerror(
                    title="Error In Dollar or Cent field",
                    message="Do not enter any characters or special symbols such as the $ sign.",
                    icon="warning",
                )
                self.dollarEntry.delete(0, "end")

        else:
            # Show a error
            messagebox.showerror(
                title="Error While Saving",
                message="Text fields cannot be empty!",
                icon="warning",
            )
