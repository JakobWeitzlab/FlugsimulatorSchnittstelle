#from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font, ttk
import tkinter
import customtkinter

#To do: Remove
'''OUTPUT_PATH = Path(__file__).papiprent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)'''
   


window = Tk()
window.geometry("800x280")
window.configure(bg = "#FFFFFF")
window.attributes('-fullscreen', False)
window.resizable(False, False)

#Canvas Settings
canvas = Canvas(
                window,
                bg = "#FFFFFF",
                height = 480,
                width = 800,
                bd = 0,
                highlightthickness = 0,
                relief = "ridge")
#init Canvas
canvas.place(x = 0, y = 0)

#FONTS
title = tkinter.font.Font(family = "LEMONMILK", 
                                size = 20, 
                                weight = "bold")

kategories = tkinter.font.Font(family = "LEMONMILK", 
                                size = 15, 
                                weight = "bold")
                                
#Is connected? Rect
canvas.create_rectangle(
    3.0,
    3.0,
    797.0000610351562,
    477.0,
    fill="red",
    outline="red",
    width=10)
#main right rect
canvas.create_rectangle(
    154.0,
    3.0,
    797.0,
    477.0,
    fill="#FAFBFC",
    outline=""
)
#main left rect
canvas.create_rectangle(
    3.0,
    3.0,
    190.0,
    477.0,
    fill="#4685FF",
    outline=""
)
#connection rect
canvas.create_rectangle(
    158.0,
    3.0,
    191.0,
    477.0,
    fill="#FAFBFC",
    outline="")
#Battery Status
canvas.create_text(
    169.0,
    70.0,
    anchor="nw",
    text="Battery Status",
    fill="#4685FF",
    font=("LEMONMILK Bold", 20 * -1)
)
#calibration
canvas.create_text(
    478.0,
    193.0,
    anchor="nw",
    text="Calibration",
    fill="#4685FF",
    font=("LEMONMILK Bold", 20 * -1)
)
#title
canvas.create_text(
    14.0,
    24.0,
    anchor="nw",
    text="FS-Simpro\ndev-gui",
    fill="#FFFFFF",
    font=title
)
#flight-log
canvas.create_text(
    169.0,
    193.0,
    anchor="nw",
    text="Flight-log",
    fill="#4685FF",
    font=("LEMONMILK Bold", 20 * -1)
)
#dashboard button
customtkinter.CTkButton(master= window, bg_color="#4685FF", fg_color="#4685FF", hover_color="#FAFBFC", text_color="#FAFBFC", corner_radius=15, text="Dashboard", text_font=("LEMON MILK",13), width=154).place(x=4,y=110)
#imagefile = PhotoImage(file=r"C:\Users\jakob\OneDrive - HTL Weiz\Diplomarbeit\Skripten\_Repository\FlugsimulatorSchnittstelle\images\button.png")
#tkinter.Button(window, image=imagefile, text="Dashboard").place(x=4, y=110)
#battery
canvas.create_text(
    25.0,
    164.0,
    anchor="nw",
    text="Battery",
    fill="#FAFBFC",
    font=kategories
)
#flight
canvas.create_text(
    25.0,
    138.0,
    anchor="nw",
    text="Flight",
    fill="#FAFBFC",
    font=kategories
)
#sensor 1
canvas.create_text(
    169.0,
    113.0,
    anchor="nw",
    text="Sensor 1:",
    fill="#000000",
    font=("LEMONMILK Regular", 18 * -1)
)
#time left sensor 1
canvas.create_text(
    312.0,
    117.0,
    anchor="nw",
    text="Time-left:",
    fill="#000000",
    font=("LEMONMILK Regular", 12 * -1)
)
#time left sensor 2
canvas.create_text(
    313.0,
    148.0,
    anchor="nw",
    text="Time-left:",
    fill="#000000",
    font=("LEMONMILK Regular", 12 * -1)
)
#time left sensor 3
canvas.create_text(
    621.0,
    117.0,
    anchor="nw",
    text="Time-left:",
    fill="#000000",
    font=("LEMONMILK Regular", 12 * -1)
)
#time left sensor 4
canvas.create_text(
    622.0,
    148.0,
    anchor="nw",
    text="Time-left:",
    fill="#000000",
    font=("LEMONMILK Regular", 12 * -1)
)
#sensor 2
canvas.create_text(
    169.0,
    144.0,
    anchor="nw",
    text="Sensor 2:",
    fill="#000000",
    font=("LEMONMILK Regular", 18 * -1)
)
#sensor 3
canvas.create_text(
    477.0,
    113.0,
    anchor="nw",
    text="Sensor 3:",
    fill="#000000",
    font=("LEMONMILK Regular", 18 * -1)
)
#sensor 4
canvas.create_text(
    477.0,
    144.0,
    anchor="nw",
    text="Sensor 4:",
    fill="#000000",
    font=("LEMONMILK Regular", 18 * -1)
)
#error log
canvas.create_text(
    25.0,
    190.0,
    anchor="nw",
    text="Error-log",
    fill="#FAFBFC",
    font=kategories
)
#help center
canvas.create_text(
    25.0,
    216.0,
    anchor="nw",
    text="help-center",
    fill="#FAFBFC",
    font=kategories
)
#straight line top
canvas.create_rectangle(
    158.0,
    62.0,
    797.0,
    62.0,
    fill="#FFFFFF",
    outline="")
#straight line middle
canvas.create_rectangle(
    158.0,
    185.0,
    797.0,
    185.0,
    fill="#FFFFFF",
    outline="")
#straight line divider
canvas.create_rectangle(
    460.0,
    184.0,
    460.0,
    477.0,
    fill="#FFFFFF",
    outline="")
#search box
canvas.create_rectangle(
    191.0,
    17.0,
    436.0,
    47.0,
    fill="#C4C4C4",
    outline="")

window.mainloop()
