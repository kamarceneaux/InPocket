import tkinter
from windows import set_dpi_awareness
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from utlities import information

set_dpi_awareness()


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

        # Buttons
        ## Login
        self.loginButton = Button(
            master=self.f2,
            text="    Login    ",  # 4 spaces on each side
            font="Arial 12",
            # command = self.loginScreenOpen,
            fg=information["titleText"],
            bd=5,
            width=25,
        )
        self.loginButton.place(x=195, y=75)

        ## Register
        self.loginButton = Button(
            master=self.f2,
            text="   Register   ",  # 3 spaces on each side
            font="Arial 12",
            # command = self.RegisterScreenOpen,
            fg=information["titleText"],
            bd=4,
            width=25,
        )
        self.loginButton.place(x=195, y=145)


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
