from tkinter import *
from utlities import information
import json


class Register(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("InPocket -- Money Manager")
        self.geometry("650x550+600+250")
        self.resizable(False, False)
        self.mainloop()
