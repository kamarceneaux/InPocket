import tkinter
from tkinter import font
from windows import set_dpi_awareness
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from utlities import information
from register import Register

set_dpi_awareness()

TEXT_COLOR = information["titleText"]


class Home(object):
    """Equal to the Main screen."""

    def __init__(self, master):
        """Master is equal to root here"""
        self.master = master

        # master.grid_rowconfigure(1, weight=1)
        # master.grid_columnconfigure(0, weight=1)

        # Create our frame(s)
        self.f1 = Frame(master, height=information["thirdOfFrame"])
        self.f1.pack(fill=X)

        self.sep = ttk.Separator(master, orient="horizontal")
        self.sep.pack(fill=X)

        self.f2 = Frame(master, height=0.6 * 500)
        self.f2.pack(fill=X)

        # Add some items into our top frame (f1)
        ## Opens image
        self.logo = Image.open("InPocketTransparent.png")
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
        self.entryUsername.insert(0, "Enter your username here.")
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
            command=self.printPassword,
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
        print("Registering account...")
        registration = Register()


# Runs the home page
def main():
    root = Tk()
    app = Home(root)
    root.title("InPocket -- Money Manager")
    root.geometry("650x550+400+100")
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
