import tkinter as tk

class App:
    def __init__(self):
        root=tk.Tk()
        root.title("Rock Paper Scissors")
        root.geometry("420x200")
        self.text=Text(root)
        self.text.grid(row=1,columnspan=5)
        tk.Button(root,text="Rock",command=self.Rock).grid(row=0,column=1,padx=10)
        tk.Button(root,text="Paper",command=self.Paper).grid(row=0,column=2)
        tk.Button(root,text="Scissors",command=self.Scissors).grid(row=0,column=3,padx=10)
        root.mainloop()

    def Rock(self):
        text="Paper!"
        self.text.delete(0,END) #delete everything from the Text
        self.text.insert(0,text) #put the text in

    def Paper(self):
        text="Scissors!"
        self.text.delete(0,END) #delete everything from the Text
        self.text.insert(0,text) #put the text in

    def Scissors(self):
        text="Rock!"
        self.text.delete(0,END) #delete everything from the Text
        self.text.insert(0,text) #put the text in

if __name__=='__main__':
    App()