from tkinter import *
from tkinter import messagebox


root = Tk()
root.title('Login')
root.geometry('980x540+300+200')
root.configure(bg = '#fff')
root.resizable(False,False)

img = PhotoImage(file = 'NameLogo1.png')
Label(root,image = img , bg = 'white').place(x = 20, y = 65)

frame = Frame(root,width = 400 , height = 375,bg = 'white')
frame.place(x = 520 , y = 55)

heading = Label(frame, text = 'Sign In',fg='Black' , bg = 'white', font = ('Microsoft YaHei UI Light',25,'bold'))
heading.place(x = 150, y = 7)

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



Button(frame , width = 23 , pady = 3,text = 'Sign in' , bg = 'black' , fg = 'white', border = 0).place(x = 130 , y = 204)

root.mainloop()
