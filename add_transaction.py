from tkinter import Toplevel, ttk, Frame, Label
import json
from tkinter.constants import X
from PIL import Image, ImageTk

# Imports to add
# SQLite, Pillow


class AddTransaction(Toplevel):
    """Shows the transaction page to add transaction"""

    def __init__(self):
        Toplevel.__init__()
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

        # Frame 2
