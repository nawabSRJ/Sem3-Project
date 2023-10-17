from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg = '#fff')
root.resizable(False,False)


img = PhotoImage(file = 'NameLogo1.png')
Label(root,image = img , bg = 'white').place(x = 50, y = 50)

frame = Frame(root, width = 350 , height = 350 , bg = 'white')
frame.place(x = 480 , y = 70)

heading = Label(frame, text = 'Sign In',fg='#57a1f8' , bg = 'white', font = ('Microsoft YaHei UI Light',23,'bold'))
heading.place(x = 100, y = 5)

#--------------------------------------- USERNAME ---------------------------------------

def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0,'Enter Username')




# border has been set to 0 , to give it a modern kinda look else the entry block will be visible

user = Entry(frame,width = 25, fg = 'black',border = 0, bg= 'white', font = ('Microsoft YaHei UI Light',11))
user.place(x = 30, y = 80)
user.insert(0,'Enter Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)

Frame(frame , width = 295 , height = 2, bg = 'black').place(x = 25,y = 107) # this line places an underline below username entry widget



#--------------------------------------- PASSWORD ---------------------------------------
def on_enter(e):
    passwd.delete(0,'end')

def on_leave(e):
    paswd = passwd.get()
    if paswd == '':
        passwd.insert(0,'Enter Password')
# border has been set to 0 , to give it a modern kinda look else the entry block will be visible

passwd = Entry(frame,width = 25, fg = 'black',border = 0, bg= 'white', font = ('Microsoft YaHei UI Light',11))
passwd.place(x = 30, y = 150)
passwd.insert(0,'Enter Password')
passwd.bind('<FocusIn>',on_enter)
passwd.bind('<FocusOut>',on_leave)


Frame(frame , width = 295 , height = 2, bg = 'black').place(x = 25,y = 177) # this line places an underline below username entry widget


# --------- Sign In Button -----------------

Button(frame , width = 39 , pady = 7,text = 'Sign in' , bg = 'black' , fg = 'white', border = 0).place(x = 35 , y = 204)


#label = Label(frame, text = "Don't Have an account?",fg = 'black' , bg = 'white', font = ('Microsoft YaHei UI Light',9))
#label.place(x = 75 , y = 270)      ~ leaving this part as of now!!!



# run the app
root.mainloop()

