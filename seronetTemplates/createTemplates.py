import tkinter as tk
import sys
import os
from Registry2ImmPort_basic import create_basic
from Registry2ImmPort_full import create_full
from PIL import Image, ImageTk


root= tk.Tk()
root.eval('tk::PlaceWindow . center')
root.title("Creating a new Template")


CANVAS_W = int(950/2)
CANVAS_H = int(713/2)

canvas1 = tk.Canvas(root, width = CANVAS_W, height = CANVAS_H)
canvas1.pack()

# Create a photoimage object of the image in the path
image_path = os.path.join(".","1_0000_SeroNet_Diagram-3x4.jpg") #713, 950
img = ImageTk.PhotoImage(Image.open(image_path).resize((int(950/2),int(713/2))))


# Create a Label Widget to display the text or Image
label = tk.Label(canvas1, image = img, bg='White')
label.pack()

Hcolor = "Black"

entry1 = tk.Entry(root, highlightthickness=.7, bg= "#E8F4F3", 
                      highlightcolor=Hcolor, 
                      highlightbackground=Hcolor, 
                      borderwidth=.7) 
entry1.bind("<Button-1>", lambda e: entry1.delete(0, tk.END))
entry1.insert(0, "Enter PMID here")

canvas1.create_window(100, 140, window=entry1)
entry1.place(x = CANVAS_W/2 - 90, y = CANVAS_H - 75)


def runFullCuration():
   x1 = entry1.get()
   print(f"Doing Full Curation for: {x1}")
   root.destroy()
   create_full(x1)

def runBasicCuration():
   x1 = entry1.get()
   print(f"Doing Basic Curation for: {x1}")
   root.destroy()
   create_basic(x1)
   
borderColor = "White"
    
button1 = tk.Button(text='Full Curation', command=runFullCuration, fg = 'Black',
                      bg = '#001d26',
                      bd =  10, 
                      highlightthickness=4, 
                      highlightcolor=borderColor, 
                      highlightbackground=borderColor, 
                      borderwidth=4)
canvas1.create_window(100, 140, window=button1)
button1.place(x=CANVAS_W/2+5, y=CANVAS_H-50)

button2 = tk.Button(text='Basic Curation', command=runBasicCuration,fg = 'Black',
                      bg = '#001d26',
                      bd =  10, 
                      highlightthickness=4, 
                      highlightcolor=borderColor, 
                      highlightbackground=borderColor, 
                      borderwidth=4)

canvas1.create_window(100, 140, window=button2)
button2.place(x=CANVAS_W/2-130, y=CANVAS_H-50)

root.mainloop()


