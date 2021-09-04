from tkinter import ttk, messagebox, Toplevel, Frame, X, Label, Entry, Button
from PIL import ImageTk, Image
from utlities import information
import json

TEXT_COLOR = information["titleText"]


class Register(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Register")
        self.geometry("650x550+600+250")
        self.resizable(False, False)
        self.iconbitmap("Images\InPocketTransparent.png")
        self.profilesRegistered = []

        # Create our frame(s)
        self.f1 = Frame(self, height=information["thirdOfFrame"])
        self.f1.pack(fill=X)

        self.sep = ttk.Separator(self, orient="horizontal")
        self.sep.pack(fill=X)

        self.f2 = Frame(self, height=0.6 * 500)
        self.f2.pack(fill=X)

        self.f1.grid_columnconfigure(0, weight=1)
        self.f2.grid_rowconfigure(0, weight=1)

        # Add some items into our top frame (f1)
        ## Opens image
        self.logo = Image.open("images/InPocketTransparent.png")
        self.resized_logo = self.logo.resize((130, 130), Image.ANTIALIAS)
        self.new_logo = ImageTk.PhotoImage(self.resized_logo)
        self.logo_lbl = Label(self, image=self.new_logo)
        self.logo_lbl.place(x=50, y=5)

        ## Title section
        self.title = Label(
            self,
            text="In Pocket -- Money Manager",
            font="Arial 20",
            fg=information["titleText"],
        )
        self.title.place(x=190, y=50)

        # Frame 2
        ## Inputs
        self.firstNamelbl = Label(
            self.f2, text="First Name: ", fg=TEXT_COLOR, font="Arial 16 bold"
        )
        self.firstName = Entry(self.f2, width=25, bd=4)
        self.usernamelbl = Label(
            self.f2, text="Username: ", fg=TEXT_COLOR, font="Arial 16 bold"
        )
        self.username = Entry(self.f2, width=25, bd=4)
        self.passwordLbl = Label(
            self.f2, text="Password: ", fg=TEXT_COLOR, font="Arial 16 bold"
        )
        self.password = Entry(self.f2, width=25, bd=4)
        self.balanceLbl = Label(
            self.f2, text="Balance:    $", fg=TEXT_COLOR, font="Arial 16 bold"
        )
        self.balance = Entry(self.f2, width=25, bd=4)

        ## Row 1
        self.firstNamelbl.place(x=140, y=30)
        self.firstName.place(x=310, y=32)

        ## Row 2
        self.usernamelbl.place(x=140, y=70)
        self.username.place(x=310, y=72)

        ## Row 3
        self.passwordLbl.place(x=140, y=110)
        self.password.place(x=310, y=112)

        ## Row 4
        self.balanceLbl.place(x=140, y=150)
        self.balance.place(x=310, y=152)

        ## Submit Button Row
        submit = Button(
            self.f2,
            text="Submit",
            width=14,
            bd=4,
            font="Arial 16 bold",
            command=self.completeRegistration,
        )
        submit.place(x=210, y=215)

    def completeRegistration(self):
        """Submit and completely register a user, if all the fields are met."""
        first_name = self.firstName.get()
        username = self.username.get()
        password = self.password.get()
        balance = self.balance.get()
        if first_name and username and password and balance != "":
            try:
                balance_split = balance.split(".")
                nondecimal = balance_split[0]
                if len(balance_split) > 1:
                    decimal = balance_split[1]
                    full_string = f"{nondecimal}.{decimal}"
                    complete_balance = round(float(full_string), 2)
                else:
                    complete_balance = int(nondecimal)

                try:
                    with open("registered_users.json") as file:
                        users_data = json.load(file)
                        usernames_in_list = users_data["username"]

                    if username in usernames_in_list:

                        self.username.delete(0, "end")

                        messagebox.showerror(
                            title="Error involving registration",
                            message=f"The username '{username}', already exists. Please select a new one.",
                        )
                    else:
                        users_data["first_name"].append(first_name.title())
                        users_data["username"].append(username)
                        users_data["password"].append(password)
                        users_data["balance"].append(complete_balance)

                        with open("registered_users.json", "w") as file:
                            json.dump(users_data, file, indent=4)

                        messagebox.showinfo(
                            title="Success",
                            message=f"{first_name}, your account was succesfully created! This window will now close.",
                            icon="info",
                        )

                        self.destroy()

                except FileNotFoundError:
                    users = {}
                    users["first_name"] = [first_name]
                    users["username"] = [username]
                    users["password"] = [password]
                    users["balance"] = [balance]
                    with open("registered_users.json", "w") as file:
                        json.dump(users, file, indent=4)

                    messagebox.showinfo(
                        title="Success",
                        message=f"{first_name}, your account was succesfully created! This window will now close.",
                        icon="info",
                    )

                    self.destroy()

            except ValueError:
                messagebox.showerror(
                    title="Error",
                    message="'Balance' only takes numerical values. Do not enter any symbols or other characters (this includes the dollar sign ($). You can include the decimal point if it is properly placed.",
                    icon="warning",
                )
        else:
            messagebox.showerror(
                title="Error", message="Fields cannot be empty.", icon="warning"
            )

    def uploadInformation(self):
        pass
