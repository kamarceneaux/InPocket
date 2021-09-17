from home import HomePage
from tkinter import font
from windows import set_dpi_awareness
from tkinter import ttk, Frame, Label, Entry, Tk, Button, X, messagebox
from PIL import ImageTk, Image
from utlities import information
from register import Register
import json

set_dpi_awareness()

TEXT_COLOR = information["titleText"]


class Home(object):
    """Equal to the Main screen."""

    def __init__(self, master):
        """Master is equal to root here"""
        self.master = master
        self.destroy_page = False

        # master.grid_rowconfigure(1, weight=1)
        # master.grid_columnconfigure(0, weight=1)

        # Create our frame(s)
        self.f1 = Frame(master, height=information["thirdOfFrame"])
        self.f1.pack(fill=X)

        self.sep = ttk.Separator(master, orient="horizontal")
        self.sep.pack(fill=X)

        self.f2 = Frame(master, height=0.6 * 550)
        self.f2.pack(fill=X)

        # Add some items into our top frame (f1)
        ## Opens image
        self.logo = Image.open("images/InPocketTransparent.png")
        self.resized_logo = self.logo.resize((130, 130), Image.ANTIALIAS)
        self.new_logo = ImageTk.PhotoImage(self.resized_logo)
        self.logo_lbl = Label(master, image=self.new_logo)
        self.logo_lbl.place(x=50, y=5)

        ## Title section
        self.title = Label(
            master,
            text="In Pocket -- Money Manager",
            font="Arial 20",
            fg=information["titleText"],
        )
        self.title.place(x=190, y=50)

        # Entry Fields
        ## Username section
        self.lbl_username = Label(
            self.f2,
            text="Username: ",
            font="Arial 15 bold",
            fg=TEXT_COLOR,
        )
        self.lbl_username.place(x=125, y=50)
        self.entryUsername = Entry(self.f2, width=30, bd=4)
        self.entryUsername.place(x=290 - 25, y=55)
        self.entryUsername.focus()

        ## Password Section
        self.lbl_password = Label(
            self.f2, text="Password: ", font="Arial 15 bold", fg=TEXT_COLOR
        )
        self.lbl_password.place(x=125, y=100)
        self.entryPassword = Entry(self.f2, width=30, bd=4, show="*")
        self.entryPassword.place(x=290 - 25, y=105)

        # Submit Button
        submit = Button(
            self.f2,
            text="Submit",
            font="Arial 13 bold",
            command=self.verify_access,
            bd=4,
            width=15,
        )  # for now command will be to print password
        submit.place(x=220, y=155)

        # Create a account button/menus (f3)
        # Create a account label
        self.newAccountLbl = Label(
            self.f2, text="Don't have a account?", font="Arial 11 bold", fg=TEXT_COLOR
        )
        self.newAccountLbl.place(x=80, y=227)

        # New account button
        registerBtn = Button(
            self.f2,
            text="Register",
            width=20,
            bd=4,
            font="Arial 11 bold",
            command=self.register,
        )
        registerBtn.place(x=295, y=218)

    def printPassword(self):
        print(self.entryPassword.get())

    def register(self):
        registration = Register()

    def open_homepage(self):
        homepage = HomePage()

    def verify_access(self):
        """Takes the users inputted password and makes sure it's credentials are right for access into their account"""

        """
        #1) Make sure a users fields isn't empty
            #3) Save the data to variables
            #4) try loading the data in
                #6) cycle throught username column and find index where users username is equal to the username found in the json
                #7) if username is found
                    #10) return index
                    #11) Make sure the password is correct
                        #12) If password is correct launch next screen
                        #15) Dump correct information into a user accessed file
                    #13) If password doesn't match username
                        #14) launch error message
                #8) if user is not found
                    #9) error message
            #5) except: error box saying no data could be found
        #2) If empty: prompt error message
        """

        typed_username = self.entryUsername.get().lower()
        typed_password = self.entryPassword.get()

        if typed_username and typed_password != "":
            try:
                with open("registered_users.json") as file:
                    users_data = json.load(file)
                list_of_usernames = users_data["username"]
                list_of_passwords = users_data["password"]
                list_of_balances = users_data["balance"]
                list_of_firstname = users_data["first_name"]
                list_of_startingbalances = users_data['starting_balance']

                try:
                    index_of_items = list_of_usernames.index(typed_username)
                    set_password = list_of_passwords[index_of_items]

                    if typed_password == set_password:
                        accessed_information = []

                        accessed_information.append(list_of_firstname[index_of_items])
                        accessed_information.append(list_of_usernames[index_of_items])
                        accessed_information.append(set_password)
                        accessed_information.append(list_of_balances[index_of_items])
                        accessed_information.append(list_of_startingbalances[index_of_items])

                        with open("accessed_user.json", "w") as file:
                            json.dump(accessed_information, file)

                        self.open_homepage()
                        self.entryUsername.delete(0, "end")
                        self.entryPassword.delete(0, "end")

                    else:
                        messagebox.showerror(
                            title="Invalid Credentials",
                            message="One or both fields is incorrect. Please try again.",
                            icon="warning",
                        )
                        self.entryUsername.delete(0, "end")
                        self.entryPassword.delete(0, "end")
                        self.entryUsername.focus()

                except ValueError:
                    messagebox.showerror(
                        title="Invalid Credentials",
                        message="One or both fields is incorrect. Please try again.",
                        icon="warning",
                    )
                    self.entryUsername.delete(0, "end")
                    self.entryPassword.delete(0, "end")
                    self.entryUsername.focus()

            except FileNotFoundError:
                messagebox.showerror(
                    title="Error",
                    message="There is no account's registered. Make sure you've registered and SUBMITED a account. NOTE: Account's are not able to be transferred between computers at this time.",
                )
        else:
            messagebox.showerror(
                title="Error While Authenticating",
                message="Text fields cannot be empty!",
                icon="warning",
            )


# Runs the home page
def main():
    root = Tk()
    app = Home(root)
    root.title("InPocket -- Money Manager")
    root.geometry("650x550+400+100")
    root.resizable(False, False)
    root.iconbitmap("images/iconInPocket.ico")
    root.mainloop()


if __name__ == "__main__":
    main()
