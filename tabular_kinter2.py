# * for entring data part of the app
from tkinter import *

root = Tk()
root.title('Score Predictor')
root.geometry('600x400')

# Sample Data
data = [(1, 10), (2, 15), (3, 8), (4, 20), (5, 12), (6, 18), (7, 25), (8, 16), (9, 22)]

# Create Labels and Entry Widgets
for i, (over, runs) in enumerate(data):
    Label(root, text=f'Over {over}:').grid(row=i, column=0, padx=5, pady=5)
    entry = Entry(root, width=10)
    entry.insert(0, runs)
    entry.grid(row=i, column=1, padx=5, pady=5)

root.mainloop()
