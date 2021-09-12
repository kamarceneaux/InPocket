import io
from tkinter import *
from tkinter import ttk, messagebox
import json
import sqlite3

from pandas.io.sql import DatabaseError
from windows import set_dpi_awareness
from utlities import FONTTEXTCOLOR
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
    6) Add a tab that shows the next percentage increase
        6a) Number showing net percentage increase (r0, c0)
        6b) Text saying net percentage increase (r0, c1, columnspan = 2)
    7) Show Current balance
        7a) follow same format as previous tab
    8) Show biggest income
    9) Show biggest expense
    10) Show most common types of transactions
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
        #Access the current users data
        with open("accessed_user.json") as file:
            self.user = json.load(file)
        #Return username and current balance for future use
        self.username = self.user[1]
        self.balance = float(self.user[3])
        # Load in SQL Database
        try:
            query = f"SELECT * FROM transactions WHERE username ='{self.username}'"
            data = pd.read_sql_query(query, con)
            print(data)
            self.primaryScreen()
        except DatabaseError:
            self.errorScreen()
            messagebox.showerror("Error Involving Data", message="No information found in the database.")
        
        
    def primaryScreen(self):
        """Showing the actual screen."""
        self.title(f"{self.user[0]}'s Transaction Sheet")
        self.geometry("650x550+500+150")
        self.resizable(False, False)
        self.iconbitmap("images/iconInPocket.ico")
        
        self.primaryNotebook = ttk.Notebook(self)
        self.primaryNotebook.pack()
        
        self.statisticsFrame = Frame(self.primaryNotebook,width=650, height=550)
        self.statisticsFrame.pack(fill='both', expand=1)
        
        self.transactionLog = Frame(self.primaryNotebook, width=650, height=550)
        self.transactionLog.pack(fill='both', expand=1)
        
        self.primaryNotebook.add(self.statisticsFrame, text='Statistics')
        self.primaryNotebook.add(self.transactionLog, text="Transaction Log")
        
    def errorScreen(self):
        self.title(f"{self.user[0]}'s Transaction Sheet")
        self.geometry("650x550+500+150")
        self.resizable(False, False)
        self.iconbitmap("images/iconInPocket.ico")
        
    


