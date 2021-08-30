from tkinter import Toplevel, ttk, Label, Frame
from tkinter.constants import X
from windows import set_dpi_awareness
from PIL import ImageTk, Image
import json


class HomePage(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        with open("accessed_user.json") as file:
            self.user = json.load(file)
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
        self.logo_lbl = Label(self, image=self.new_logo)
        self.logo_lbl.place(x=50, y=5)
