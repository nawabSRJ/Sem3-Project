from tkinter import *
from tkinter import ttk
import csv
import os
import pywhatkit as p
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import mysql.connector
mydb = mysql.connector.connect(host = 'localhost',
                               user = 'root',
                               password = '123456',
                               database = 'MyApp')
cur = mydb.cursor()
currTable = 'match_1'
class LoginPage():
    def get_treeview_data(tree):
        overs = []
        runs = []

        for row_id in tree.get_children():
            row_data = tree.item(row_id)['values']
            overs.append(row_data[0])
            runs.append(row_data[1])
        dat = list(zip(overs, runs))

        
        try:
            with open('output.csv', 'x', newline='') as File:
                writer = csv.writer(File)
                writer.writerow(['overs', 'runs'])
                writer.writerows(dat)
        except FileExistsError:
            # Handle the case when the file already exists
            print("File 'output.csv' already exists. Skipping writing to the file.")
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")
            
    def show_welcome_frame(self,user):
        
        lf_bg = 'LightSkyBlue'  # Left Frame Background Color
        rtf_bg = 'DeepSkyBlue'  # Right Top Frame Background Color
        rbf_bg = 'DodgerBlue'  # Right Bottom Frame Background Color
        btn_hlb_bg = 'SteelBlue'  # Background color for Head Labels and Buttons

        lbl_font = ('Georgia', 13)  # Font for all labels
        entry_font = ('Times New Roman', 12)  # Font for all Entry widgets
        btn_font = ('Gill Sans MT', 13)
        
        
        self.img_label.destroy()

        # Create a new window or frame for the welcome message
        welcome_frame = Frame(self.root, width=800, height=240, bg='white')
        welcome_frame.place(x=260, y=20)

        welcome_label = Label(welcome_frame, text=f'Welcome {user.title()}', fg='Black', bg='white',
                            font=('Microsoft YaHei UI Light', 24, 'bold'))
        welcome_label.place(x=20, y=1)

        
        left_frame = Frame(self.root, bg=lf_bg)
        left_frame.place(x=0, y=20, width = 180, relheight=0.96)

        right_frame = Frame(self.root, bg=lf_bg)
        right_frame.place(x = 800 , y = 1)
        data_frame = Frame(self.root, width = 300 , height = 500 , bg = 'white')
        data_frame.place(x = 330 , y = 130)
        
         # * Label ~ Table Name
        tableName = 'Match_1'
        tname = Label(text = f'Table Name : {tableName}' , width = 25 , height = 2 , fg = 'black' , bg = 'white' , font=('Microsoft YaHei UI Light', 12, 'bold'))
        tname.place(x = 350 , y = 70)
        
        # * ---------- Button Functions ------------
        def update_table_data(table_name):
            # * Clear existing items in the tree
            for item in tree.get_children():
                tree.delete(item)

            over_data = f'SELECT * FROM {table_name}'
            cur.execute(over_data)
            res = cur.fetchall()

            for row in res:
                tree.insert('', 'end', values=row)
                
        def open_delete_window():
            new_window = Toplevel(self.root)
            new_window.title('Select Table to Delete')
            new_window.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_x()}+{self.root.winfo_y()}")

            table_list_label = Label(new_window, text='Select a Table to Delete:', font=('Microsoft YaHei UI Light', 12, 'bold'))
            table_list_label.pack(pady=10)

            # Fetch table names that start with 'match'
            cur.execute("SHOW TABLES LIKE 'match%'")
            tables = cur.fetchall()

            def delete_table(table_name):
                # Ask for confirmation before deleting
                permit = messagebox.askyesno("Confirmation", f"Do you want to delete the table '{table_name}'?")

                if permit:
                    # Construct the DROP TABLE query
                    drop_table_query = f"DROP TABLE {table_name}"

                    try:
                        cur.execute(drop_table_query)
                        mydb.commit()
                        messagebox.showinfo("Success", f"Table '{table_name}' deleted successfully.")
                        new_window.destroy()
                        # Optionally, update the table data and display a default table
                        update_table_data('default_table')  # Replace 'default_table' with the table you want to show
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred: {e}")
                else:
                    print("User clicked No. Deletion canceled.")

            for table in tables:
                table_name = table[0]
                delete_button = Button(new_window, text=f'Delete {table_name}', padx=10, pady=10, command=lambda tn=table_name: delete_table(tn))
                delete_button.pack()
                
        def open_new_window():
            new_window = Toplevel(self.root)
            new_window.title('Select Table')
            new_window.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_x()}+{self.root.winfo_y()}")

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
        def update_btn():
            new_window = Toplevel(self.root)
            new_window.title('Update Data')
            new_window.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_x()}+{self.root.winfo_y()}")

            table_list_label = Label(new_window, text='Enter Data:', font=('Microsoft YaHei UI Light', 12, 'bold'))
            table_list_label.grid(row=0, column=0, pady=10, columnspan=2)  # Use grid here

            data_entries = []  # List to store Entry widgets
            overs = []
            runs = []

            for row_id in tree.get_children():
                row_data = tree.item(row_id)['values']
                overs.append(row_data[0])
                runs.append(row_data[1])
            data = list(zip(overs, runs))
            

            for i, (over, runs) in enumerate(data):
                Label(new_window, text=f'Over {over}:').grid(row=i + 1, column=0, padx=5, pady=5)
                entry = Entry(new_window, width=10)
                entry.insert(0, runs)
                entry.grid(row=i + 1, column=1, padx=5, pady=5)
                data_entries.append(entry)
            
            
            def okay_action():
                # Retrieve entered data from Entry widgets
                entered_data = []

                for entry in data_entries:
                    try:
                        value = int(entry.get())
                        entered_data.append(value)
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid integers for runs.")
                        return
                permit = messagebox.askyesno("Confirmation", "Do you want to perform this operation?")
    
                if permit:
                    # Construct the UPDATE query
                    update_table_query = f"UPDATE {currTable} SET Runs = CASE "
                    for over, run in zip(overs, entered_data):
                        update_table_query += f"WHEN Overs = {over} THEN {run} "
                    update_table_query += "END"
                    
                    try:
                        cur.execute(update_table_query)
                        mydb.commit()
                        messagebox.showinfo("Success", "Data updated successfully.")
                        new_window.destroy()
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred: {e}")
                else:
                    print("User clicked No. Operation canceled.")
                    
                new_window.destroy()  # Close the Toplevel window
                # * End of Function
                
                
            okay_button = Button(new_window, text='Okay', command=okay_action)
            okay_button.grid(row=len(data) + 1, column=0, columnspan=2, pady=10)
                
                
        def new_data_window():
            new_window = Toplevel(self.root)
            new_window.title('Enter Data')
            new_window.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_x()}+{self.root.winfo_y()}")

            table_list_label = Label(new_window, text='Enter Data:', font=('Microsoft YaHei UI Light', 12, 'bold'))
            table_list_label.grid(row=0, column=0, pady=10, columnspan=2)  # Use grid here

            data_entries = []  # List to store Entry widgets

            # todo - Sample data, replace it with your actual data
            data = [(1, 10), (2, 15), (3, 8), (4, 20), (5, 12), (6, 18), (7, 25), (8, 16), (9, 22)]

            for i, (over, runs) in enumerate(data):
                Label(new_window, text=f'Over {over}:').grid(row=i + 1, column=0, padx=5, pady=5)
                entry = Entry(new_window, width=10)
                entry.insert(0, runs)
                entry.grid(row=i + 1, column=1, padx=5, pady=5)
                data_entries.append(entry)
            
            def okay_button_action():
            # Retrieve entered data from Entry widgets
                entered_data = []

                for entry in data_entries:
                    try:
                        value = int(entry.get())
                        entered_data.append(value)
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid integers for runs.")
                        return

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
                # * End of Function
                
            okay_button = Button(new_window, text='Okay', command=okay_button_action)
            okay_button.grid(row=len(data) + 1, column=0, columnspan=2, pady=10)  # setting the okay button bellow the data lis

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
            
        def predict_next_over():
            file_path = 'output.csv'
            if os.path.exists(file_path):
                data = pd.read_csv('output.csv')
            else :
                print('File exists error')
                   
            formula = LinearRegression()
            x = data.overs.values.reshape(-1,1)
            y = data.runs.values.reshape(-1,1)
           

            formula.fit(x, y)

            # Predict the next over's runs
            next_over = 10
            next_over_runs = formula.predict([[next_over]])
            print(int(next_over_runs))
            # Update the label with the prediction
            next_over_label.config(text=f'Next Over Prediction: {int(next_over_runs)} runs')  
              
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
        
        #  # * Add a Label for Next Over Prediction
        # prediction_frame = Frame(self.root, width=800, height=50, bg='black')
        # prediction_frame.place(x=100, y=400)

        next_over_label = Label(self.root, text="Next Over Prediction: {Next Over Runs}", fg='white', bg='black',
                                font=('Microsoft YaHei UI Light', 12, 'bold'))
        next_over_label.grid(row = 50 , column = 8)
        # next_over_label.pack(pady = 5)
        
        # * ---------- BUTTONS ------------
        select_data = Button(left_frame, text='Select Data', font=btn_font, bg=btn_hlb_bg, width=17 , command=open_new_window ).grid(row=40, column=1, padx=15, pady=20)
        add_data = Button(left_frame, text='Add Data', font=btn_font, bg=btn_hlb_bg, width=17 , command=new_data_window ).grid(row=50, column=1, padx=15, pady=20)
        delete_data = Button(left_frame, text='Delete Data', font=btn_font, bg=btn_hlb_bg, width=17 , command = open_delete_window ).grid(row = 60, column = 1, padx = 15, pady=20)
        update_data = Button(left_frame, text='Update Data', font=btn_font, bg=btn_hlb_bg, width=17 , command = update_btn ).grid(row = 70, column = 1, padx = 15, pady=20)
        
        predict_data = Button(left_frame, text='Predict Next', font=btn_font, bg=btn_hlb_bg, width=17,command = predict_next_over  ).grid(row = 80, column = 1, padx = 15, pady=20)
        
        show_data = Button(right_frame, width=20, pady=3, text='Plot Data', bg='black', fg='white', border=2, command=lambda: plot_data(currTable))
        show_data.grid(row=40, column=9, padx=15, pady=20)
        
    def authenticate(self):
        name = self.user.get().lower()
        lock = self.passwd.get()
        query1 = f"SELECT UNAME, PASSWORD from USERS where UNAME = '{name}' "
        # query2 = f"SELECT PASSWORD from USERS where Name = '{lock}' "
        cur.execute(query1)
        result = cur.fetchone()

        

        if result:
            print("USER FOUND")
            stored_password = result[1]  # Extract password from the tuple

            if lock == stored_password:
                print(f"Password for user {result[0]} is Correct")

                self.frame.destroy()
                
                self.show_welcome_frame(user = result[0])
            else:
              
                messagebox.showerror("Alert","Incorrect Password")

        else:
            messagebox.showerror("Alert","USER NOT FOUND")
           

    def __init__(self):
        self.root = Tk()
        self.root.title('Login')
        self.root.geometry('925x500+300+200')
        self.root.configure(bg='#fff')
        self.root.resizable(False, False)

        self.img = PhotoImage(file='NameLogo1.png')
        self.img_label = Label(self.root, image=self.img, bg='white')
        self.img_label.place(x=20, y=50)

        self.frame = Frame(self.root, width=350, height=350, bg='white')
        self.frame.place(x=480, y=70)
        # previous fg = '57a1f8'
        heading = Label(self.frame, text='Sign In', fg='green', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=135, y=5)

        # --------------------------------------- USERNAME ---------------------------------------
        def username_on_enter(e):
            self.user.delete(0, 'end')

        def username_on_leave(e):
            name = self.user.get()
            if name == '':
                self.user.insert(0, 'Enter Username')

        self.user = Entry(self.frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        self.user.place(x=30, y=80)
        self.user.insert(0, 'Enter Username')
        self.user.bind('<FocusIn>', username_on_enter)
        self.user.bind('<FocusOut>', username_on_leave)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=107)

        # --------------------------------------- PASSWORD ---------------------------------------
        def password_on_enter(e):
            self.passwd.delete(0, 'end')

        def password_on_leave(e):
            paswd = self.passwd.get()
            if paswd == '':
                self.passwd.insert(0, 'Enter Password')

        self.passwd = Entry(self.frame, width=25, fg='black', border=0, bg='white',
                            font=('Microsoft YaHei UI Light', 11))
        self.passwd.place(x=30, y=130)
        self.passwd.insert(0, 'Enter Password')
        self.passwd.bind('<FocusIn>', password_on_enter)
        self.passwd.bind('<FocusOut>', password_on_leave)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=157)

        # --------- Sign In Button -----------------
        Button(self.frame, width=39, pady=7, text='Sign in', bg='black', fg='white', border=0 ,command = self.authenticate).place(x=35, y=200)

        #forgot password
        def otp_command():
            
            def send_msg(self):
                number = self.pno.get()
                first = number[0:5]
                last = number[5::]
                p.sendwhatmsg(f"+91 {first} {last}", "Your OTP is 007")

                
            self.msgwindow = Toplevel(self.root)
            self.msgwindow.title('OTP WINDOW')
            self.msgwindow.geometry('425x320+30+20')
            self.msgwindow.resizable(False,False)
            self.pno = Entry(self.msgwindow , width = 25 ,fg = 'black' , bg = 'white' , border = 0 , font=('Microsoft YaHei UI Light', 11))
            self.pno.grid(row=15, column=50 , padx = 10 ,pady = 10)
            self.pno.insert(0, 'Enter Phone Number')
            self.otp_button = Button(self.msgwindow , bg = 'black' , fg = 'white',border = 0,text = 'generate OTP' , width = 15, command = send_msg)
            self.otp_button.grid(row = 20 , column = 55 , padx = 7 , pady = 7)

        fgpass = Button(self.frame , width = 20, pady = 4, text = 'Forgot Password', border = 0,fg = 'white',bg = 'black', command = otp_command).place(x = 30 , y = 240)
        # todo - use pywhatkit for OTP generation 
        self.root.mainloop()

myob = LoginPage()