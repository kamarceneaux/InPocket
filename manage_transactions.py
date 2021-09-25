import io
from tkinter import *
from tkinter import ttk, messagebox
import json
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
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

        ## Add a seperator
        self.sep = ttk.Separator(self.statisticsFrame, orient="horizontal")
        self.sep.grid(row=5, column=0, columnspan=3, sticky="EW")

        # Get Into Showing the Graphs
        ## Line graph showing the spending and etc
        self.spendingButton = Button(
            self.statisticsFrame,
            text="Spending History Graph",
            command=self.spending_graph,
        )
        self.spendingButton.grid(row=6, column=1, pady=15)

        ## Show distribution of each transaction type
        self.distTranTypeButton = Button(
            self.statisticsFrame,
            text="Pie Chart of Trans Type",
            command=self.common_typeTrans_graph,
        )
        self.distTranTypeButton.grid(row=7, column=1, pady=15, columnspan=1)

        ##Show distribution of each amount for each transaction
        self.distAmtBtn = Button(
            self.statisticsFrame,
            text="Histogram of Money",
            command=self.range_of_source,
        )
        self.distAmtBtn.grid(row=8, column=1, pady=15, columnspan=1)

        ## Revenue and expense
        self.revenue_expenseBtn = Button(
            self.statisticsFrame,
            text="Revenue and Expense",
            command=self.expense_revenue_graphs,
        )
        self.revenue_expenseBtn.grid(row=9, column=1, pady=15)

    def spending_graph(self):
        only_spending_amounts = list(self.data["amount"])
        # Showing accurate spending amounts now
        y_values = [self.starting_balance]
        new_index = 0
        for v in only_spending_amounts:
            new_balance = round(y_values[new_index] + v, 2)
            y_values.append(new_balance)
            new_index += 1

        # Creates the x values which marks the occurence of when the balance was spent
        x_values = [x for x in range(len(y_values))]
        plt.plot(x_values, y_values)
        plt.title("Balance Increase/Decrease for Each Transaction")
        plt.xlabel("Occurence of Transaction")
        plt.xticks(x_values)
        plt.ylabel("Balance")
        plt.show()

    def common_typeTrans_graph(self):
        # Counts for each type
        counts_typeTrans = dict(self.data["transaction_type"].value_counts())
        labels = list(counts_typeTrans.keys())
        values = list(counts_typeTrans.values())
        # Convert the values to percentages since it's a sample
        perc_values = []
        total_counts_of_labels = sum(values)
        for v in values:
            # Converts each value to a percent
            percentage = round((v / total_counts_of_labels) * 100, 2)
            # Adds to the percent list
            perc_values.append(percentage)

        plt.pie(perc_values, labels=labels)
        plt.legend()
        plt.show()

    def range_of_source(self):
        income_columns = self.data["amount"][self.data["amount"] >= 0]
        expense_columns = self.data["amount"][self.data["amount"] < 0]
        ticks = [x for x in range(12) if x % 2 == 0]
        x_ticks = [-100, -75, -50, -25, 0, 25, 50, 75, 100]

        # Shows both columns
        plt.hist(income_columns, x_ticks)
        plt.hist(expense_columns, x_ticks)
        plt.xlabel("Dollar amounts")
        # plt.xticks(x_ticks)
        plt.ylabel("Frequency")
        plt.show()

    def expense_revenue_graphs(self):
        """Generate a graph showing revenue/expense values per month"""
        column_selection = self.data[["amount", "month"]]
        uniq_months = list(column_selection["month"].unique())
        # Values we will select for the graph
        bar_graph_values = []

        for month in uniq_months:
            # Select values in the data frame where the month is equal to the unique months
            values_in_certain_months = column_selection[
                column_selection["month"] == month
            ]
            # Select the rows in the dataframe
            # Add certain values to the chart
            expensePerMonth = []
            revenuePerMonth = []
            for index, row in values_in_certain_months.iterrows():
                value = row["amount"]
                if value >= 0:
                    revenuePerMonth.append(value)
                else:
                    value = abs(value)
                    expensePerMonth.append(value)

            # Add up the sums
            sum_of_expenses = sum(expensePerMonth)
            sum_of_revenues = sum(revenuePerMonth)

            # Add to the bar graph values
            # First index equals the month, second one is income/revenue, third is expenses
            month_to_add = [month, sum_of_revenues, sum_of_expenses]
        bar_graph_values.append(month_to_add)

        # Select Month values
        x_months = []
        y_income = []
        y_expense = []

        for item in bar_graph_values:
            x_months.append(item[0])
            y_income.append(item[1])
            y_expense.append(item[2])

        print(bar_graph_values)

        # Actual Graphing Now
        ## Graphing income per a month
        plt.subplot(2, 1, 1)
        plt.bar(x_months, y_income, color="green", label="Income")
        plt.xticks([], [])
        plt.ylabel("Absolute Value of Income in USD ($)")
        plt.legend()
        ## Graphing expenses per a month
        plt.subplot(2, 1, 2)
        plt.bar(x_months, y_expense, color="red", label="Expense")
        plt.xticks(rotation=45, horizontalalignment="right")
        plt.ylabel("Absolute Value of Expense in USD ($)")
        plt.legend()
        # Show the graphs
        plt.show()

    def errorScreen(self):
        self.title(f"{self.user[0]}'s Transaction Sheet")
        self.geometry("650x550+500+150")
        self.resizable(False, False)
        self.iconbitmap("images/iconInPocket.ico")
