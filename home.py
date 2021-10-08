import datetime
from tkinter import (
    Button,
    Toplevel,
    font,
    ttk,
    Label,
    Frame,
    Entry,
    messagebox,
    CENTER,
    E,
    VERTICAL,
    RIGHT,
    Scrollbar,
    Y,
    HORIZONTAL,
    BOTTOM,
)
import tkinter
from tkinter.constants import X
from utlities import FONTTEXTCOLOR, random_money_quotes, exp_income, type_of_trans
from windows import set_dpi_awareness
from PIL import ImageTk, Image
import json
import random
import sqlite3
from datetime import date
from pandas.io.sql import DatabaseError
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

con = sqlite3.connect("InPocket-Database.db")
cur = con.cursor()

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
            text=f"Current Balance: ${round(self.balance,2)}",
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
            self.f2,
            text="View Past Transactions",
            width=20,
            bd=4,
            font="Arial 16 bold",
            command=self.manageTrans,
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

    def manageTrans(self):
        view_trans = TransactionData()
        self.destroy()
        view_trans.lift()


class AddTransaction(Toplevel):
    """Shows the transaction page to add transaction"""

    def __init__(self):
        Toplevel.__init__(self)
        with open("accessed_user.json") as file:
            self.user = json.load(file)
        self.first_name = self.user[0]
        self.username = self.user[1]
        self.balance = float(self.user[3])
        self.today = date.today()

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
            width=22,
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
            width=19,
        )
        self.typeOfTransResponse.place(x=185, y=87)

        ### Description
        self.descriptionLbl = Label(
            self.f2,
            text="Description: ",
            fg=FONTTEXTCOLOR,
            font="Arial 11 bold",
        )
        self.descriptionLbl.place(x=2, y=145)
        self.description = Entry(self.f2, width=30, bd=4)
        self.description.place(x=117, y=147)

        ### Dollar entry
        self.dollarLbl = Label(
            self.f2, text="$", fg=FONTTEXTCOLOR, font="Arial 11 bold"
        )
        self.dollarLbl.place(x=85, y=195)
        self.dollarEntry = Entry(self.f2, width=12, bd=6)
        self.dollarEntry.insert(0, "00")
        self.dollarEntry.place(x=100, y=195)

        ### Cents entry
        self.centLbl = Label(self.f2, text=".", fg=FONTTEXTCOLOR, font="Arial 11 bold")
        self.centLbl.place(x=212, y=198)
        self.centEntry = Entry(self.f2, width=8, bd=6)
        self.centEntry.insert(0, "00")
        self.centEntry.place(x=230, y=195)

        ### Months entry
        self.monthLbl = Label(
            self.f2, text="MM", fg=FONTTEXTCOLOR, font="Arial 11 bold"
        )
        self.monthLbl.place(x=80, y=250)
        self.monthEntry = Entry(self.f2, width=3, bd=3)
        self.monthEntry.insert(0, self.today.month)
        self.monthEntry.place(x=120, y=250)

        ### Day entry
        self.dayLbl = Label(self.f2, text="DD", fg=FONTTEXTCOLOR, font="Arial 11 bold")
        self.dayLbl.place(x=145, y=250)
        self.dayEntry = Entry(self.f2, width=3, bd=3)
        self.dayEntry.insert(0, self.today.day)
        self.dayEntry.place(x=180, y=250)

        ### Year Entry
        self.yearLbl = Label(
            self.f2, text="YYYY", fg=FONTTEXTCOLOR, font="Arial 11 bold"
        )
        self.yearLbl.place(x=200, y=250)
        self.yearEntry = Entry(self.f2, width=6, bd=3)
        self.yearEntry.insert(0, self.today.year)
        self.yearEntry.place(x=260, y=250)

        ### Submit button
        submit = Button(
            self.f2,
            text="Submit",
            width=10,
            bd=2,
            font="Arial 11 bold",
            command=self.finalizeSubmission,
        )
        submit.place(x=142, y=300)

        ### Tips and tricks image
        self.ttImg = Image.open("Images/TransactionTips.png")
        self.ttImga = ImageTk.PhotoImage(self.ttImg)
        self.ttlImgLbl = Label(self.f2, image=self.ttImga)
        self.ttlImgLbl.place(x=400, y=5)

        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def onClosing(self):
        """Handles events when the window is being closed."""
        go_back_home = HomePage()
        self.destroy()
        go_back_home.lift()

    def finalizeSubmission(self):
        # Entry fields for database
        expen_incon_entry = self.expense_or_income.get()
        typeTrans = self.trans_type.get()
        descriptionOfficialEntry = self.description.get().strip()
        dollarOfficialEntry = self.dollarEntry.get().strip()
        centOfficialEntry = self.centEntry.get().strip()
        monthOfficialEntry = self.monthEntry.get().strip()
        dayOfficialEntry = self.dayEntry.get().strip()
        yearOfficialEntry = self.yearEntry.get().strip()

        if (
            expen_incon_entry
            and typeTrans
            and descriptionOfficialEntry
            and dollarOfficialEntry
            and centOfficialEntry
            and monthOfficialEntry
            and dayOfficialEntry
            and yearOfficialEntry != ""
        ):
            # Convert string to numerical
            try:
                dollarOfficialEntry = int(dollarOfficialEntry)
                # Takes the length (incase it's greater than base 10 ^ -2)
                divide_by = len(centOfficialEntry)
                # Converts cents to int
                centOfficialEntry = int(centOfficialEntry)
                # Divide the cents by the number
                exponent_raise = 10 ** (1 * divide_by)
                centOfficialEntry1 = round(centOfficialEntry / exponent_raise, 2)
                total_balance = dollarOfficialEntry + centOfficialEntry1
                if expen_incon_entry == "Expense":
                    total_balance = total_balance * -1
                # Calculate the users new balance
                self.balance = self.balance + total_balance
                # Update and load the new balance into the access_user and register_user files
                self.user[3] = self.balance
                try:
                    with open("accessed_user.json", "w") as file:
                        json.dump(self.user, file)

                    ## Update the information in the registered users
                    with open("registered_users.json") as file:
                        users_data = json.load(file)
                    list_of_usernames = users_data["username"]
                    list_of_balances = users_data["balance"]
                    index_of_items = list_of_usernames.index(self.username)

                    # Update the balance
                    list_of_balances[index_of_items] = self.balance
                    # Dump the new balance into the update usersdata
                    with open("registered_users.json", "w") as file:
                        json.dump(users_data, file, indent=4)
                except:
                    messagebox.showerror(
                        title="Error",
                        message="This is a technical error on our part.",
                    )

                try:
                    query = """
                    INSERT INTO 'transactions' (username, statement, transaction_type, description, amount, month, day, year) VALUES (?,?,?,?,?,?,?,?)
                    """
                    cur.execute(
                        query,
                        (
                            self.username,
                            expen_incon_entry,
                            typeTrans,
                            descriptionOfficialEntry,
                            total_balance,
                            monthOfficialEntry,
                            dayOfficialEntry,
                            yearOfficialEntry,
                        ),
                    )
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Successfully added to database!", icon="info"
                    )
                    self.open_view_transactions()
                except:
                    messagebox.showerror(
                        title="Error",
                        message="Can not add to the database! Either due to a error involving the date.",
                        icon="warning",
                    )

            except ValueError:
                messagebox.showerror(
                    title="Error In Dollar or Cent field",
                    message="Do not enter any characters or special symbols such as the $ sign.",
                    icon="warning",
                )
                self.dollarEntry.delete(0, "end")
                self.centEntry.delete(0, "end")

        else:
            # Show a error
            messagebox.showerror(
                title="Error While Saving",
                message="Text fields cannot be empty or either there is invalid data.",
                icon="warning",
            )
            self.answerExpInc.focus()

    def open_view_transactions(self):
        go_back_home = TransactionData()
        self.destroy()
        go_back_home.lift()


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

        self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def onClosing(self):
        """Handles events when the window is being closed."""
        go_back_home = HomePage()
        self.destroy()
        go_back_home.lift()

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

        self.viewTransScreen()

    def viewTransScreen(self):
        # Select certain information
        transInfoToShow = self.data[
            [
                "transaction_id",
                "statement",
                "transaction_type",
                "description",
                "amount",
                "month",
                "day",
                "year",
            ]
        ]
        # Convert the months-days-year to a standard date format
        transInfoToShow["YYYY-MM-DD"] = (
            transInfoToShow["year"]
            + "-"
            + transInfoToShow["month"]
            + "-"
            + transInfoToShow["day"]
        )
        # Remove certain columns
        columns_to_drop = ["year", "month", "day"]
        for column in columns_to_drop:
            del transInfoToShow[column]

        # Create the treeview
        my_tree = ttk.Treeview(self.transactionLog)

        # Set up the tree view
        ## Show colums (headings)
        my_tree["column"] = list(transInfoToShow.columns)
        my_tree["show"] = "headings"

        ## Loop throught column list for headers
        for column in my_tree["column"]:
            my_tree.heading(column, text=column, anchor=CENTER)

        # Add vertical scrollbar
        sb = Scrollbar(self.transactionLog, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)

        my_tree.config(yscrollcommand=sb.set)
        sb.config(command=my_tree.yview)

        # Add horizontal scrollbar
        sb_h = Scrollbar(self.transactionLog, orient=HORIZONTAL)
        sb_h.pack(side=BOTTOM, fill=X)

        my_tree.config(xscrollcommand=sb_h.set)
        sb_h.config(command=my_tree.xview)

        ## Put data in tree view
        data_rows = transInfoToShow.to_numpy().tolist()
        for row in data_rows:
            my_tree.insert("", "end", values=row)

        # Pack the tree view
        my_tree.pack(fill=Y)

        # Delete a transaction
        removeTransLbl = Label(
            self.transactionLog,
            text="Do you need to remove a transaction?",
            fg=FONTTEXTCOLOR,
        )

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
        plt.xlabel("Month's throughout all years")
        plt.legend()
        # Show the graphs
        plt.show()

    def errorScreen(self):
        self.title(f"{self.user[0]}'s Transaction Sheet")
        self.geometry("650x550+500+150")
        self.resizable(False, False)
        self.iconbitmap("images/iconInPocket.ico")
