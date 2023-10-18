from tkinter import *
from tkinter import ttk
import logging 
from tkinter import simpledialog
from tkinter import messagebox
import matplotlib.pyplot as plt
import mysql.connector
mydb = mysql.connector.connect(host = 'localhost',
                               user = 'root',
                               password = '123456',
                               database = 'MyApp')
cur = mydb.cursor()
root = Tk()
root.title('Login')
root.geometry('980x540+300+200')
root.configure(bg = '#fff')
root.resizable(False,False)
img = PhotoImage(file = 'NameLogo1.png')
img_label = Label(root,image = img , bg = 'white')
img_label.place(x = 20, y = 65)
currTable = 'match_1'
frame = Frame(root,width = 990 , height = 375,bg = 'white')
frame.place(x = 520 , y = 55)
# frame = Frame(root, width=root.winfo_width(), height=root.winfo_height(), bg='red')
# frame.place(x = 520 , y = 55)
heading = Label(frame, text = 'Sign In',fg='Black' , bg = 'white', font = ('Microsoft YaHei UI Light',25,'bold'))
heading.place(x = 150, y = 7)


def show_welcome_frame(user):
   
    # img_label.config(state = 'disabled')
    img_label.destroy()

    # Create a new window or frame for the welcome message
    welcome_frame = Frame(root, width=800, height=240, bg='white')
    welcome_frame.place(x=260, y=20)

    welcome_label = Label(welcome_frame, text=f'Welcome {user.title()}', fg='Black', bg='white',
                        font=('Microsoft YaHei UI Light', 24, 'bold'))
    welcome_label.place(x=20, y=1)
    sidebar = Frame(root, height = 900 , width = 210, bg = 'white')
    sidebar.place(x = 1 , y = 5)

    data_frame = Frame(root, width = 300 , height = 500 , bg = 'white')
    data_frame.place(x = 330 , y = 130)

    rightbar = Frame(root, height = 900 , width = 210, bg = 'white')
    rightbar.place(x = 800 , y = 1)

    # * Label ~ Table Name
    tableName = 'Match_1'
    tname = Label(text = f'Table Name : {tableName}' , width = 25 , height = 2 , fg = 'black' , bg = 'white' , font=('Microsoft YaHei UI Light', 12, 'bold'))
    tname.place(x = 350 , y = 70)

    # * ------------------- some important functions -------------
    def update_table_data(table_name):
        # * Clear existing items in the tree
        for item in tree.get_children():
            tree.delete(item)

        over_data = f'SELECT * FROM {table_name}'
        cur.execute(over_data)
        res = cur.fetchall()

        for row in res:
            tree.insert('', 'end', values=row)
            
            
    def open_new_window():
        new_window = Toplevel(root)
        new_window.title('Select Table')
        new_window.geometry(f"{root.winfo_width()}x{root.winfo_height()}+{root.winfo_x()}+{root.winfo_y()}")

        table_list_label = Label(new_window, text='Select a Table:', font=('Microsoft YaHei UI Light', 12, 'bold'))
        table_list_label.pack(pady=10)

        # Fetch table names that start with 'match'
        cur.execute("SHOW TABLES LIKE 'match%'")
        tables = cur.fetchall()

        def use_table(table_name):
            global currTable
            tname.config(text=f'Table Name: {table_name}')
            currTable = table_name      # ! to store the current table name
            update_table_data(table_name)
            new_window.destroy()

        for table in tables:
            table_name = table[0]
            use_button = Button(new_window, text=f'{table_name}', padx = 10, pady = 10,command=lambda tn=table_name: use_table(tn))
            use_button.pack()


    # * ~~~~~~~~~~~ when add data is pressed :
    def new_data_window():
        new_window = Toplevel(root)
        new_window.title('Enter Data')
        new_window.geometry(f"{root.winfo_width()}x{root.winfo_height()}+{root.winfo_x()}+{root.winfo_y()}")

        table_list_label = Label(new_window, text='Enter Data:', font=('Microsoft YaHei UI Light', 12, 'bold'))
        table_list_label.grid(row=0, column=0, pady=10, columnspan=2)  # Use grid here

        data_entries = []  # List to store Entry widgets

        # Sample data, replace it with your actual data
        data = [(1, 10), (2, 15), (3, 8), (4, 20), (5, 12), (6, 18), (7, 25), (8, 16), (9, 22)]

        for i, (over, runs) in enumerate(data):
            Label(new_window, text=f'Over {over}:').grid(row=i + 1, column=0, padx=5, pady=5)
            entry = Entry(new_window, width=10)
            entry.insert(0, runs)
            entry.grid(row=i + 1, column=1, padx=5, pady=5)
            data_entries.append(entry)

        def okay_button_action():
        # Retrieve entered data from Entry widgets
            entered_data = [int(entry.get()) for entry in data_entries]

            # Ask for the new table name
            new_table_name = simpledialog.askstring("Input", "Enter a new table name:")

            # Create a new table in the database; AUTO-INCREMENTING the 'Overs' Column
            create_table_query = f"CREATE TABLE {new_table_name} (Overs INT AUTO_INCREMENT PRIMARY KEY, Runs INT NOT NULL)"
            cur.execute(create_table_query)

            # Insert the entered data into the new table
            insert_data_query = f"INSERT INTO {new_table_name} (Runs) VALUES (%s)"
            cur.executemany(insert_data_query, [(run,) for run in entered_data])
            mydb.commit()

            # Updating the table name and the table in the main window
            tname.config(text=f'Table Name: {new_table_name}')
            update_table_data(new_table_name)

            new_window.destroy()  # Close the Toplevel window



        
        okay_button = Button(new_window, text='Okay', command=okay_button_action)
        okay_button.grid(row=len(data) + 1, column=0, columnspan=2, pady=10)  


    # * when plot data is pressed 
    def plot_data(table_name):
        over_data = f'SELECT * FROM {table_name}'
        cur.execute(over_data)
        res = cur.fetchall()

        overs = []
        runs = []

        for row in res:
            overs.append(row[0])  # Assuming the first column is Overs
            runs.append(row[1])   # Assuming the second column is Runs

        # Plotting the data
        plt.figure(figsize=(8, 6))
        plt.plot(overs, runs, marker='o')
        plt.title(f'Data Plot for {table_name}')
        plt.xlabel('Overs')
        plt.ylabel('Runs')
        plt.grid(True)
        plt.show()


    # * ---------- BUTTONS ------------
    select_data = Button(sidebar, width=20, pady=3, text='Select Data', bg='black', fg='white', border=2, command=open_new_window)
    select_data.grid(row=40, column=1, padx=15, pady=20)

    add_data = Button(sidebar, width=20, pady=3, text='Add Data', bg='black', fg='white', border=2, command=new_data_window)
    add_data.grid(row=50, column=1, padx=15, pady=20)

    delete_data = Button(sidebar , width=20, pady=3, text='Delete Data', bg='black', fg='white', border=2)
    delete_data.grid(row = 60, column = 1, padx = 15, pady=20)

    update_data = Button(sidebar , width=20, pady=3, text='Update Data', bg='black', fg='white', border=2)
    update_data.grid(row = 70, column = 1, padx = 15, pady=20)

    show_data = Button(rightbar, width=20, pady=3, text='Plot Data', bg='black', fg='white', border=2, command=lambda: plot_data(currTable))
    show_data.grid(row=40, column=9, padx=15, pady=20)

    # * --------------------- TABULAR DATA --------------------

    over_data = 'SELECT * FROM MATCH_1'
    cur.execute(over_data)
    res = cur.fetchall()

    tree = ttk.Treeview(data_frame, columns=('Over', 'Runs'), show='headings', height=10)
    tree.heading('Over', text='Over No.')
    tree.heading('Runs', text='Runs Scored')
    # tree.place(x = 300 , y = 120)
    tree.pack(fill='both', expand=True)


    for row in res:
        tree.insert('', 'end', values=row)

    # todo - Adjust Column Widths

    tree.column('Over', width=100)
    tree.column('Runs', width=100)
    
    # * Add a Label for Next Over Prediction
    prediction_frame = Frame(root, width=800, height=50, bg='white')
    prediction_frame.place(x=100, y=490)

    next_over_label = Label(prediction_frame, text="Next Over Prediction: {Next Over Runs}", fg='black', bg='white',
                            font=('Microsoft YaHei UI Light', 12, 'bold'))
    next_over_label.pack()

# ! ------------------------------------------------------------------


def authenticate():
    name = username.get().lower()
    lock = passwd.get()
    query1 = f"SELECT UNAME, PASSWORD from USERS where UNAME = '{name}' "
    # query2 = f"SELECT PASSWORD from USERS where Name = '{lock}' "
    cur.execute(query1)
    result = cur.fetchone()

    # print("Result:", result)  # * Adding this line to see the result

    if result:
        print("USER FOUND")
        stored_password = result[1]  # Extract password from the tuple

        if lock == stored_password:
            print(f"Password for user {result[0]} is Correct")



            frame.destroy()
            
         
            # Show the welcome frame with the user's name
            show_welcome_frame(result[0])
        else:
            print("Incorrect Password")

    else:
        print("USER NOT FOUND")
        # log.info("User Not Found")

    

# * ----------------------- USERNAME , PASSWORD , BUTTON
def on_enter(e):
    username.delete(0,'end')
    
def on_leave(e):
    name = username.get()
    if name == '':
        username.insert(0,'Enter Username')
        
username = Entry(frame,width = 25, fg = 'black',border = 0, bg= 'white', font = ('Microsoft YaHei UI Light',12))
username.place(x = 100 , y = 100)
username.insert(0,'Enter Username')
username.bind('<FocusIn>', on_enter)
username.bind('<FocusOut>', on_leave)
Frame(frame , width = 295 , height = 2,border = 0, bg = 'black').place(x = 100,y = 127) # this line places an underline below username entry widget



passwd = Entry(frame , width = 25, border = 0, font = ('Microsoft YaHei UI Light',12), show = "*")
passwd.place(x = 100 , y = 150)
# passwd.insert(0,'Enter Password') # ! no need 
Frame(frame , width = 295 , height = 2, bg = 'black').place(x = 100,y = 177) # this line places an underline below username entry widget


Button(frame, width=23, pady=3, text='Sign in', bg='black', fg='white', border=0, command=authenticate).place(x=130, y=204)

root.mainloop()
