from tkinter import *
from tkinter import messagebox
import pywhatkit as p

class LoginPage():
    
    def welcome_window(self):
        self.img_label.destroy()
        self.welcome_frame = Frame(self.root, width=900, height=320, bg='white')
        self.welcome_frame.place(x=260, y=20)

        self.welcome_label = Label(self.welcome_frame, text=f'Welcome Srajan', fg='Black', bg='white',
                        font=('Microsoft YaHei UI Light', 24, 'bold'))
        self.welcome_label.place(x=20, y=1)
    
    
    def __init__(self):
        self.root = Tk()
        self.root.title('Login')
        self.root.geometry('925x500+300+200')
        self.root.configure(bg='#fff')
        self.root.resizable(False, False)

        self.img = PhotoImage(file='NameLogo1.png')
        self.img_label = Label(self.root, image=self.img, bg='white').place(x=20, y=50)

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
        Button(self.frame, width=39, pady=7, text='Sign in', bg='black', fg='white', border=0 , command = self.welcome_window).place(x=35, y=200)

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
