from tkinter import Toplevel, ttk, Label, Frame
from tkinter.constants import X
from utlities import FONTTEXTCOLOR
from windows import set_dpi_awareness
from PIL import ImageTk, Image
import json

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
        self.iconbitmap("iconInPocket.ico")

        # Frames
        self.f1 = Frame(self, height=0.25 * 550)
        self.f1.pack(fill=X)

        self.f2 = Frame(self, height=0.50 * 550)
        self.f2.pack(fill=X)

        self.f3 = Frame(self, height=0.25 * 550)
        self.f3.pack(fill=X)

        # Heading Frame
        ## Opens image
        self.logo = Image.open("InPocketTransparent.png")
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
        self.greetUser.place(x=450, y=122)

        # Frame 2
        ## Add Transaction Button (button will launch new window, and terminate this window)

        ## View past transactions button (read add transaction button)

        # Frame 3
        ## Load in quotes
        ## Then show a RANDOM quote to display
