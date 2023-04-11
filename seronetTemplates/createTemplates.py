import tkinter as tk
import sys
import os
from Registry2ImmPort_basic import create_basic
from Registry2ImmPort_short import create_short
from PIL import Image, ImageTk

from argparse import ArgumentParser

parser = ArgumentParser(
             prog="createTemplate",
             description="Parse a SeroNet registry template into ImmPort templates and JSON")

parser.add_argument(
        '--Dev',
        '-d',
        required=False,
        help="Help with running batch scripts. It will bypass the GUI and run script"
    )

parser.add_argument(
        '--PMID',
        '-p',
        required=False,
        help="Enter Pubmed ID. This ID must have a Box folder with a naming format of \'PMID_xxxxxxxx\'"
    )


args = parser.parse_args()

if args.Dev:
   print(f"Doing Short Curation for: {args.PMID.strip()}")
   create_short(args.PMID.strip())

else:
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


   def select_on_focus(event):
       event.widget.select_range(0, tk.END) # Select all the text in the widget.

   entry1 = tk.Entry(root, highlightthickness=.7, bg= "#E8F4F3", 
                         highlightcolor=Hcolor, 
                         highlightbackground=Hcolor, 
                         borderwidth=.7) 
   entry1.focus_set()
   entry1.bind("<Button-1>", lambda e: entry1.delete(0, tk.END))
   entry1.insert(0, "Enter PMID here")

   canvas1.create_window(100, 140, window=entry1)
   entry1.place(x = CANVAS_W/2 - 90, y = CANVAS_H - 75)



   def runFullCuration(multiple=False):
      x1 = entry1.get()
      print(f"Doing Full Curation for: {x1}")
      root.destroy()
      create_short(x1.strip())

   def runBasicCuration(multiple=False):
      x1 = entry1.get()
      print(f"Doing Basic Curation for: {x1}")
      root.destroy()
      create_basic(x1.strip())

   def onclick(event):
      runFullCuration()
      
   borderColor = "White"


   CheckVar1 = tk.BooleanVar()
   # print(CheckVar1)
   C1 = tk.Checkbutton(root, text = "Multiple", variable = CheckVar1,
      highlightcolor=borderColor, 
      highlightbackground=borderColor,
      bg = borderColor,
      bd =  1, 
      onvalue = 1, offvalue = 0, height=2,
      width = 10)
   # print(CheckVar1)
       
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



   C1.place(x=CANVAS_W/2+128, y=CANVAS_H-49)

   root.bind('<Return>', onclick)

   root.mainloop()


