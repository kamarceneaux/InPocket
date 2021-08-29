from tkinter import Toplevel, ttk
from windows import set_dpi_awareness
import json


class HomePage(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Homepage")
        self.geometry("650x550+400+100")
        self.resizable(False, False)
        self.iconbitmap("iconInPocket.ico")
