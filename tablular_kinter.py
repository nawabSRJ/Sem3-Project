# * for sample data part of the app
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Score Predictor')
root.geometry('600x400')

# Create Treeview
tree = ttk.Treeview(root, columns=('Over', 'Runs'), show='headings', height=10)
tree.heading('Over', text='Over')
tree.heading('Runs', text='Runs')
tree.pack()

# * Sample Data ~ to be extracted from query 
data = [(1, 10), (2, 15), (3, 8), (4, 20), (5, 12), (6, 18), (7, 25), (8, 16), (9, 22)]

# Insert Data into Treeview
for row in data:
    tree.insert('', 'end', values=row)

# todo - Adjust Column Widths

tree.column('Over', width=70)
tree.column('Runs', width=70)

root.mainloop()
