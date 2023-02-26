from tkinter import *
from tkinter import ttk
import AiPainter
root = Tk()
root.title("Labirints")
root.geometry("640x480")

for c in range(3): root.columnconfigure(index=c, weight=1)
for r in range(3): root.rowconfigure(index=r, weight=1)

photoimage=[]
for i in range(1,10):
    photo = PhotoImage(file=r"C:\Users\avmin\PycharmProjects\pythonProject1\Folder\q"+str(i)+".png")
    photoimage.append(photo.subsample(12, 12))


def click():
    AiPainter.example()
    print("Hello")

i=0
for r in range(3):
    for c in range(3):

        btn = ttk.Button(text=f"", command=click,image=photoimage[i])
        btn.grid(row=r, column=c, ipadx=6, ipady=6, padx=4, pady=4, sticky=NSEW)
        i=i+1

root.mainloop()