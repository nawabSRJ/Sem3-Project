from tkinter import *
import logging 
from tkinter import messagebox
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
# img = PhotoImage(file = 'NameLogo1.png')
# Label(root,image = img , bg = 'white').place(x = 20, y = 65)

frame = Frame(root,width = 400 , height = 375,bg = 'white')
frame.place(x = 520 , y = 55)

heading = Label(frame, text = 'Sign In',fg='Black' , bg = 'white', font = ('Microsoft YaHei UI Light',25,'bold'))
heading.place(x = 150, y = 7)


def show_welcome_frame(user):
    # Create a new window or frame for the welcome message
    welcome_frame = Frame(root, width=800, height=240, bg='white')
    welcome_frame.place(x=260, y=20)

    welcome_label = Label(welcome_frame, text=f'Welcome {user.title()}', fg='Black', bg='white',
                          font=('Microsoft YaHei UI Light', 25, 'bold'))
    welcome_label.place(x=20, y=7)
    sidebar = Frame(root, height = 900 , width = 70, bg = 'black')
    data_frame = Frame(root, width = 500 , height = 600 , bg = 'red')
    data_frame.place(x = 300 , y = 21)


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
