import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
import flirimageextractor

def open_file():
    f_types = [('Jpg', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    if filename:
        process_and_display_image(filename)

def process_and_display_image(filename):
    
    flir = flirimageextractor.FlirImageExtractor()
    flir.process_image(filename)
    thermal_data = flir.get_thermal_np()

    temperature_celsius = thermal_data / 100 - 273.15

    global fig, ax, img
    fig, ax = plt.subplots()
    img = ax.imshow(temperature_celsius, cmap='jet', interpolation='nearest')
    ax.set_title('FLIR Thermal Image')
    fig.colorbar(img, ax=ax)

    cid = fig.canvas.mpl_connect('button_press_event', lambda event: mouse_event(event, thermal_data, ax))

    plt.show()

def mouse_event(event, thermal_data, ax):
    if event.xdata is not None and event.ydata is not None:
        x = int(event.xdata)
        y = int(event.ydata)

        if 0 <= x < thermal_data.shape[1] and 0 <= y < thermal_data.shape[0]:
            temperature_at_cursor = thermal_data[y, x]   

            print(f"Temperature at cursor position ({x}, {y}): {temperature_at_cursor:.2f} °C")

            
            ax.annotate(f"{temperature_at_cursor:.2f} °C", (x, y), color='white', weight='bold', fontsize=8, ha='center')

            
            fig.canvas.draw()

root = Tk()
root.geometry("700x500")
label_main = Label(root, text="Karkat Nirnay Yantra").pack()

open_button = Button(root, text="Open FLIR Image", command=open_file)
open_button.pack()

root.mainloop()
