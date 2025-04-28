import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style()
style.configure('Rounded.TButton', borderwidth=0, relief='solid', borderradius=10)

button = ttk.Button(root, text='Click me', style='Rounded.TButton')
button.pack()

root.mainloop()