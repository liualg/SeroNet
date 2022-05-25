import tkinter as tk
import sys

root= tk.Tk()
root.title("Please Input PMID")


CANVAS_W = 300
CANVAS_H = 150

canvas1 = tk.Canvas(root, width = CANVAS_W, height = CANVAS_H)
canvas1.pack()

entry1 = tk.Entry(root) 
canvas1.create_window(100, 140, window=entry1)
entry1.place(x = CANVAS_W/5, y = CANVAS_H/2 )


def runFullCuration():
   x1 = entry1.get()
   print(f"Doing Full Curation for: {x1}")

   root.destroy()

def runBasicCuration():
   x1 = entry1.get()
   print(f"Doing Basic Curation for: {x1}")
   
   root.destroy()

    
button1 = tk.Button(text='Full Curation', command=runFullCuration)
canvas1.create_window(100, 140, window=button1)
button1.place(x=CANVAS_W/2+10, y=CANVAS_H-40)

button2 = tk.Button(text='Basic Curation', command=runBasicCuration)
canvas1.create_window(100, 140, window=button2)
button2.place(x=CANVAS_W/10+10, y=CANVAS_H-40)

root.mainloop()