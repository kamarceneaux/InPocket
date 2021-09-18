import io
from tkinter import *
from tkinter import ttk, messagebox
import json
import sqlite3

from pandas.io.sql import DatabaseError
from windows import set_dpi_awareness
from utlities import FONTTEXTCOLOR, color
import pandas as pd

set_dpi_awareness()

con = sqlite3.connect("InPocket-Database.db")
cur = con.cursor()

""" 
Goals
1) setup basic (blank) screen ✅
2) import in the users data (such as data from using data from database and acc_user) ✅
3) filter the transactions to the data that equals the current user ✅
4) setup the notebook pages ✅
5) work on the 'Statistics' tab  ✅ 
    #Make sure we are using the grid layout
    6) Add a tab that shows the net percentage increase ✅ 
        6a) Number showing net percentage increase (r0, c0) ✅ 
        6b) Text saying net percentage increase (r0, c1, columnspan = 2) ✅ 
    7) Show Current balance ✅
        7a) follow same format as previous tab
    8) Show biggest income ✅ 
    9) Show biggest expense ✅ 
    10) Show most common types of transactions✅
    11) Show Graphs
        12) Net Income/Expense per month
        13) Histogram of price range for incomes
        14) Histogram for price range of expenses
        15) Bar Graph for types of transactions
        16) Line graph showing relationship between types of trans and amount distributed
18) Work on 'Transaction History' tab ✅
    19) Show table specifically viewing users information
    20) Add scroll functionality and filter by time submitted.

"""


class TransactionData(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        # Access the current users data
        with open("accessed_user.json") as file:
            self.user = json.load(file)
        # Return username and current balance for future use
        self.username = self.user[1]
        self.balance = float(self.user[3])
        self.starting_balance = float(self.user[4])
        # Load in SQL Database
        try:
            query = f"SELECT * FROM transactions WHERE username ='{self.username}'"
            self.data = pd.read_sql_query(query, con)
            self.primaryScreen()
        except DatabaseError:
            # Means a user can not view the screen
            self.errorScreen()
            messagebox.showerror(
                "Error Involving Data", message="No information found in the database."
            )

    def primaryScreen(self):
        """Showing the actual screen."""
        self.title(f"{self.user[0]}'s Transaction Sheet")
        self.geometry("650x550+500+150")
        self.resizable(False, False)
        self.iconbitmap("images/iconInPocket.ico")

        # Creates the literal notebook
        self.primaryNotebook = ttk.Notebook(self)
        self.primaryNotebook.pack()

        self.statisticsFrame = Frame(self.primaryNotebook, width=650, height=550)
        self.statisticsFrame.pack(fill="both", expand=1)
        self.statisticsFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.transactionLog = Frame(self.primaryNotebook, width=650, height=550)
        self.transactionLog.pack(fill="both", expand=1)

        self.primaryNotebook.add(self.statisticsFrame, text="Statistics")
        self.primaryNotebook.add(self.transactionLog, text="Transaction Log")

        # Statistics frame
        ## Calculate net percentage
        starting_balance = self.starting_balance
        new_balance = self.balance
        if new_balance > starting_balance:
            increase = new_balance - starting_balance
            net_percentage = round((increase / starting_balance) * 100, 2)
        else:
            decrease = new_balance - starting_balance
            net_percentage = round((decrease / starting_balance) * 100, 2)
        self.netPercNum = Label(
            self.statisticsFrame,
            text=f"{net_percentage}%",
            font="Arial 25 bold",
            fg=FONTTEXTCOLOR,
        )
        self.netPercNum.grid(row=0, column=0)

        ### The net percentage description
        self.netPercDescr = Label(
            self.statisticsFrame,
            text="<- Percent Increase/Decrease from starting balance",
            font="Arial 11",
            fg=FONTTEXTCOLOR,
        )
        self.netPercDescr.grid(row=0, column=1, columnspan=2)

        ## Select largest trans
        largest_balance = self.data["amount"].max()
        self.largeTransLbl = Label(
            self.statisticsFrame,
            text=f" ${largest_balance}",
            font="Arial 25 bold",
            fg=FONTTEXTCOLOR,
        )
        self.largeTransLbl.grid(row=1, column=2, sticky=E)

        ### Description of largest single trans
        self.largeTransDesc = Label(
            self.statisticsFrame,
            text="      Largest Amount of Income --> ",
            font="Arial 11",
            fg=FONTTEXTCOLOR,
        )
        self.largeTransDesc.grid(row=1, column=1)

        ## Select largest expense
        largest_expense = self.data["amount"].min()
        self.largeExpenLbl = Label(
            self.statisticsFrame,
            text=f"${largest_expense}",
            font="Arial 25 bold",
            fg=FONTTEXTCOLOR,
        )
        self.largeExpenLbl.grid(row=2, column=0)

        ### Description of largest single expense
        self.largeTransDesc = Label(
            self.statisticsFrame,
            text="  <-- Largest Expense/Smallest Purchase",
            font="Arial 11",
            fg=FONTTEXTCOLOR,
        )
        self.largeTransDesc.grid(row=2, column=1)

        ## Show current balance
        self.showCurrentBal = Label(
            self.statisticsFrame,
            text=f"Current Balance: ${round(self.balance,2)}",
            fg=FONTTEXTCOLOR,
            font="Arial 12",
        )
        self.showCurrentBal.grid(row=3, column=1, pady=10)

        ## Show most common transaction type
        common_trans_type = self.data["transaction_type"].mode()[0]
        self.showCommonTrans = Label(
            self.statisticsFrame,
            text=f"Most Common Trans: {common_trans_type}",
            fg=FONTTEXTCOLOR,
            font="Arial 12",
        )
        self.showCommonTrans.grid(row=4, column=1, pady=10)

    def errorScreen(self):
        self.title(f"{self.user[0]}'s Transaction Sheet")
        self.geometry("650x550+500+150")
        self.resizable(False, False)
        self.iconbitmap("images/iconInPocket.ico")
