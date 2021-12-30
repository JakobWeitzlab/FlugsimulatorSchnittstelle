#from pathlib import Path
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font, ttk
import customtkinter


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

    def createCanvas(self):
        canvas = tk.Canvas(self.master, bg="#FFFFF6")
        
master = tk.Tk()
#master Settings
master.title("FS-Simpro")
master.geometry("800x200")
master.configure(bg="#FFFFFF")
master.attributes("-fullscreen", False)
master.resizable(False, False)

#Create Application Obeject
application = Application(master=master)

#Create Canvas
canvas = application.createCanvas()

if __name__ == "__main__":
    application = Application()
    application.mainloop()