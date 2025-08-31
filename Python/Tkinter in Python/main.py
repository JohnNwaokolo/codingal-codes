from tkinter import *

window = Tk()

window.title("Sample window")

window.geometry("300x300")

greeting_label = Label(text="Hello world", fg="white", bg="black")

greeting_label.pack()
button = Button(text="Click me", fg="white", bg="red")
button.pack()
entry= Entry(fg="green", bg="white")
entry.pack()

frame= Frame(master= window, bg="red", height=100, width= 100, borderwidth= 5)
frame.pack()

window.mainloop()