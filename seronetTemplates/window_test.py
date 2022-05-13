
import tkinter as tk
  
# Top level window
frame = tk.Tk()
frame.title("TextBox Input")
frame.geometry('400x200')
# Function for getting Input
# from textbox and printing it 
# at label widget
  
def printInput():
    inp = inputtxt.get(1.0, "end-1c")
    lbl.config(text = "Provided Input: "+inp)
  
# TextBox Creation
inputtxt = tk.Text(frame, height = 3, width = 20)
inputtxt.grid(column=2, row=0)
  
# Button Creation
printButton = tk.Button(frame,
                        text = "Print", 
                        command = frame.destroy)

printButton2 = tk.Button(frame,
                        text = "Print3", 
                        command = frame.destroy)
printButton.grid(column=2, row=1)
printButton2.grid(column=3, row=1)
  
# Label Creation
lbl = tk.Label(frame, text = "")
# lbl.pack()
frame.mainloop()