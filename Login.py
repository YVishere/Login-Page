from tkinter import *
import numpy as np
from tkinter import filedialog as fd

class loginSystem(Frame):
    def __init__(self, window):
        super().__init__(window)
        global b
        b=True
        self.vcmd = self.register(self.callback)
        self.filepath1 = "C:/Users/ADMIN/Documents/Username.txt"
        self.filepath2="C:/Users/ADMIN/Documents/Pass.txt"
        self.filepath3="C:/Users/ADMIN/Documents/autofill.txt"
        self.initToplevel()
        self.autoUpdate()
        self.registerUI()
        self.UI()

    def initToplevel(self):
        self.autofill=Toplevel(self, bg='Black')
        self.autofill.title("Autofill")
        self.autofill.resizable(False, False)

        self.autofill.overrideredirect(True)

        self.uplabel=Label(self.autofill, relief=RAISED, text="Username", fg='#F5FFFA', bg='Black')
        self.uplabel.pack(fill=X, expand=True, ipadx=20, ipady=5)

        self.autofill.withdraw()

    def callback(self, input):
        if input[-1:].isspace():
            return False
        elif input == "":
            return True
        else:
            return True

    def initFocus(self, e):
        self.autofill.withdraw()
        e.widget.focus_set()
        self.s="%s"%e.widget.focus_get()
        self.n=self.s.find("entry")
        if self.n==-1:
            self.username.configure(bg='Grey')
            self.password.configure(bg='Grey')
            self.enteruser.configure(bg='Grey')
            self.enterpass1.configure(bg='Grey')
            self.enterpass2.configure(bg='Grey')

    def charUserCount(self, e, *args):
        self.num=len(self.vars.get())
        if self.num<=10:
            if self.num==10:
                self.labelText2.configure(fg='Red')
            else:
                self.labelText2.configure(fg='#F5FFFA')
            self.labelText2.configure(text=f"Characters left: {10-self.num}")
        if self.num>10:
            decreased="".join(self.vars.get()[:10])
            self.vars.set(decreased)

    def charPassCount(self, e, *args):
        self.num=len(self.var.get())
        if self.num<=10:
            if self.num==10:
                self.labelText4.configure(fg='Red')
            else:
                self.labelText4.configure(fg='#F5FFFA')
            self.labelText4.configure(text=f"Characters left: {10-self.num}")
        if self.num>10:
            decreased="".join(self.var.get()[:10])
            self.var.set(decreased)

    def focuscheck(self, entry):
        self.enteruser.configure(bg='Grey')
        self.username.configure(bg='Grey')
        self.password.configure(bg='Grey')
        self.enterpass1.configure(bg='Grey')
        self.enterpass2.configure(bg='Grey')
        entry.configure(bg='White')

    def labelChange(self, n, event):
        if event:
            self.msgLabel.configure(text="")
            return
        if n==-1:
            self.msgLabel.configure(text="Incomplete fields", fg='Red')
        if n==0:
            self.msgLabel.configure(text="Incorrect username or password", fg='Red')
        if n==1:
            self.msgLabel.configure(text="Login successful", fg='#F5FFFA')

    def login(self, *args):
        if not b:
            return
        if self.password.get()=="" or self.username.get()=="":
            self.password.delete(0,END)
            self.username.delete(0,END)
            self.labelChange(-1,False)
            return
        with open(self.filepath1, mode='r', encoding='UTF-8') as user:
            n=-1
            m=-1
            st=user.read()
            wd=st.split()
            users=np.array(wd)
        for i in range(0,users.size):
            if users[i]==self.username.get():
                n=i
        if n==-1:
            self.password.delete(0, END)
            self.username.delete(0, END)
            self.labelChange(0,False)
            return
        with open(self.filepath2, mode='r', encoding='UTF-8') as pas:
            str=pas.read()
            w=str.split()
            passes=np.array(w)
            if passes[n]==self.password.get():
                m=1
        if m==-1:
            self.password.delete(0, END)
            self.username.delete(0, END)
            self.labelChange(0, False)
            return

        self.u=self.vars.get()
        self.p=self.var.get()

        self.labelChange(1,False)
        self.password.delete(0, END)
        self.username.delete(0, END)
        self.request()

    def autoUpdate(self):
        with open(self.filepath3, mode='r', encoding="utf-8") as fd:
            st=fd.read()
            wd=st.split()
            self.autofillArray=np.array(wd)

        for i in range(0, self.autofillArray.size, 2):
            butt = Button(self.autofill, text=f"{self.autofillArray[i]}", command=lambda i=i: self.details(i)
                          , relief=FLAT, bg='Black', fg='#F5FFFA', activeforeground='#F5FFFA'
                          , activebackground='Black', cursor="hand2")
            butt.pack(fill=X)

    def auto(self):
        self.autofill.deiconify()

    def details(self, n):
        self.vars.set(self.autofillArray[n])
        self.var.set(self.autofillArray[n+1])
        self.autofill.withdraw()

    def request(self):
        self.ask=Toplevel(self,bg="Black")
        self.ask.title("Confirmation")
        self.ask.resizable(False,False)

        self.ask.grab_set()
        self.ask.protocol("WM_DELETE_WINDOW", self.endRequest)

        for i in range(0,self.autofillArray.size, 2):
            if self.autofillArray[i]==self.u:
                self.endRequest()
                return

        self.askLabel=Label(self.ask, text="Do you want to save your details in autofill?", bg="Black", fg="#F5FFFA"
                            , font=("Times New Roman", 15))
        self.askLabel.pack(fill=X, expand=True, padx=50, pady=30)

        self.optionsFrame=Frame(self.ask, bg="Black")
        self.optionsFrame.pack(side=BOTTOM, fill=X, expand=True)
        self.yesOption=Button(self.optionsFrame, text="Yes", bg="Black", fg="#F5FFFA"
                              , relief=FLAT, cursor="hand2", activebackground='Black'
                              , activeforeground='#F5FFFA', command=self.fulfillRequest)
        self.yesOption.pack(side=RIGHT, padx=40)
        self.noOption = Button(self.optionsFrame, text="No", bg="Black", fg="#F5FFFA"
                                , relief=FLAT, cursor="hand2", activebackground='Black'
                              , activeforeground='#F5FFFA', command=self.endRequest)
        self.noOption.pack(side=LEFT, padx=40)

    def fulfillRequest(self, *args, **kwargs):
        with open(self.filepath3, mode='a', encoding="utf-8") as fd:
            fd.write(f"{self.u} {self.p} \n")

        for i in self.autofill.winfo_children():
            s = "%s" % i
            n = s.find("button")
            if not n == -1:
                i.destroy()

        self.autoUpdate()
        self.endRequest()

    def endRequest(self):
        self.ask.grab_release()
        self.ask.destroy()

    def capsON(self, *args):
        if not b:
            return
        self.capsLabel.pack()
        self.capsLabel21.pack(side=RIGHT)
        self.capsLabel22.pack(side=RIGHT)

    def capsOFF(self, *args):
        if not b:
            return
        self.capsLabel.pack_forget()
        self.capsLabel21.pack_forget()
        self.capsLabel22.pack_forget()

    def changeFrame(self, frame):
        frame.tkraise()

    def UI(self):
        self.configure(bg='White')
        self.pack(fill=BOTH, expand=True)
        self.mainframe=Frame(self, bg='#2C3539', relief=RAISED)
        self.mainframe.grid(row=0, column=0, sticky='nsew')

        self.mainframe.tkraise()

        self.loginText=Label(self.mainframe, text="Log in to your account", bg='#2C3539', fg='#F5FFFA', font=('Times New Roman', 25))
        self.loginText.pack(padx=20, pady=40, fill=X)

        self.userFrame=Frame(self.mainframe, bg='#2C3539')
        self.userFrame.pack(padx=20, pady=2, fill=X)
        self.labelText1=Label(self.userFrame, text="Enter your username", bg='#2C3539', fg='#F5FFFA', font=('Times New Roman', 8))
        self.labelText1.pack(side=LEFT, fill=X)
        self.labelText2=Label(self.userFrame, text="Characters Left: 10", bg='#2C3539', fg='#F5FFFA', font=('Times New Roman', 8))
        self.labelText2.pack(side=RIGHT, fill=X)
        self.vars=StringVar()
        self.vars.trace('w', self.charUserCount)
        self.username=Entry(self.mainframe, bg='Grey', textvariable=self.vars
                            , validate="key", validatecommand=(self.vcmd,'%P'))
        self.username.pack(padx=20, fill=X)

        self.passFrame = Frame(self.mainframe, bg='#2C3539')
        self.passFrame.pack(padx=20, pady=(30,2), fill=X)
        self.labelText3 = Label(self.passFrame, text="Enter your password", bg='#2C3539', fg='#F5FFFA', font=('Times New Roman', 8))
        self.labelText3.pack(side=LEFT, fill=X)
        self.labelText4 = Label(self.passFrame, text=f"Characters Left: 10", bg='#2C3539', fg='#F5FFFA', font=('Times New Roman', 8))
        self.labelText4.pack(side=RIGHT, fill=X)
        self.var = StringVar()
        self.var.trace('w', self.charPassCount)
        self.password = Entry(self.mainframe, bg='Grey', textvariable=self.var, show="*"
                              , validate="key", validatecommand=(self.vcmd,'%P'))
        self.password.pack(padx=20, pady=(0,20), fill=X)
        self.capsLabel=Label(self.passFrame, text="Caps lock is on", font=("Times New Roman", 8), fg='#F5FFFA'
                             , bg='#2C3539')

        self.autofillButton=Button(self.mainframe,text="Autofill", fg='Light Blue', bg='#2C3539'
                                , activeforeground='White', activebackground='#2C3539'
                                , relief=FLAT, font=("Times New Roman",10), command=self.auto
                                , cursor='hand2')
        self.autofillButton.pack(padx=20)

        self.loginButton=Button(self.mainframe, text="Login", bg='Light Blue', fg='Black'
                                , activeforeground='Black', activebackground='Light Blue'
                                , relief=FLAT, font=("Times New Roman",25), command=self.login
                                , cursor='hand2')
        self.loginButton.pack(ipadx=30, ipady=4, padx=20, pady=(25,4))

        self.msgLabel=Label(self.mainframe, bg='#2C3539', font=("Times New Roman", 8), fg='Red')
        self.msgLabel.pack(fill=X, padx=20, pady=(3, 4), expand=True)

        self.checkFrame=Frame(self.mainframe, bg='#2C3539')
        self.checkFrame.pack(pady=(0,10),padx=20, fill=X, expand=True)

        self.textFrame=Frame(self.checkFrame, bg='#2C3539')
        self.textFrame.pack(side=LEFT, fill=X, expand=True)
        self.alText=Label(self.textFrame, bg='#2C3539', fg='#F5FFFA', text="Don't Have an Account?")
        self.alText.pack(side=RIGHT)
        self.buttonFrame=Frame(self.checkFrame, bg='#2C3539')
        self.buttonFrame.pack(side=RIGHT, fill=X, expand=True)
        self.buttonText = Button(self.buttonFrame, bg='#2C3539', fg='Light Blue', text="Create an Account",
                                 activebackground='#2C3539', activeforeground='#F5FFFA', relief=FLAT
                                 , cursor="hand2", command=lambda: self.changeFrame(self.registerFrame))
        self.buttonText.pack(side=LEFT)

    def passCheck(self, *args, **kwargs):
        s1=self.S21.get()
        s2=self.S22.get()
        if s1==s2:
            return 1
        else:
            return 0

    def reglabelChange(self, n, b):
        self.msgLabel2.configure(fg="Red")
        if b:
            if n==1:
                self.msgLabel2.configure(text="Username too long")
            if n==2:
                self.msgLabel2.configure(text="Incomplete fields")
            if n==3:
                self.msgLabel2.configure(text="Username already exists")
        if not b:
            if n==1:
                self.msgLabel2.configure(text="Password too long")
            if n==2:
                self.msgLabel2.configure(text="Passwords do not match")

    def registe(self, *args, **kwargs):
        n=self.passCheck()

        if n==0:
            self.reglabelChange(2,False)
            self.enteruser.delete(0, END)
            self.enterpass1.delete(0, END)
            self.enterpass2.delete(0, END)
            return

        username=self.S1.get()
        passw=self.S21.get()

        if len(username)>10:
            self.reglabelChange(1,True)
            self.enteruser.delete(0, END)
            self.enterpass1.delete(0, END)
            self.enterpass2.delete(0, END)
            return
        if len(passw)>10:
            self.reglabelChange(1,False)
            self.enteruser.delete(0, END)
            self.enterpass1.delete(0, END)
            self.enterpass2.delete(0, END)
            return

        if username=="" or passw=="":
            self.reglabelChange(2,True)
            self.enteruser.delete(0, END)
            self.enterpass1.delete(0, END)
            self.enterpass2.delete(0, END)
            return

        with open(self.filepath1, mode='r', encoding="utf-8") as fd:
            st = fd.read()
            wd = st.split()
            user = np.array(wd)
        for i in range(0,user.size):
            if user[i]==username:
                self.reglabelChange(3, True)
                self.enteruser.delete(0, END)
                self.enterpass1.delete(0, END)
                self.enterpass2.delete(0, END)
                return

        with open (self.filepath1, mode='a', encoding="utf-8") as fd:
            fd.write(f"{username} \n")

        with open(self.filepath2, mode='a', encoding="utf-8") as fd:
            fd.write(f"{passw} \n")

        self.enteruser.delete(0,END)
        self.enterpass1.delete(0,END)
        self.enterpass2.delete(0,END)

        self.msgLabel2.configure(text="Successfully registered", fg='#F5FFFA')

    def registerUI(self):
        self.registerFrame= Frame(self,bg='#2C3539')
        self.registerFrame.grid(row=0,column=0,sticky='nsew')

        self.registerText = Label(self.registerFrame, text="Create a new account", bg='#2C3539', fg='#F5FFFA',
                               font=('Times New Roman', 25))
        self.registerText.pack(padx=20, pady=(25, 10), fill=X)

        self.enteruserFrame=Frame(self.registerFrame,bg='#2C3539')
        self.enteruserFrame.pack(padx=20, pady=2, fill=X)
        self.enteruserLabel=Label(self.enteruserFrame, text="Enter your username",bg='#2C3539', fg='#F5FFFA',
                               font=('Times New Roman', 8))
        self.enteruserLabel.pack(side=LEFT, fill=X)
        self.S1=StringVar()
        self.enteruser=Entry(self.registerFrame,bg='Grey', textvariable=self.S1
                             , validate="key", validatecommand=(self.vcmd,'%P'))
        self.enteruser.pack(fill=X, padx=20)

        self.instructions=Label(self.registerFrame, bg='#2C3539', fg='#F5FFFA',font=('Times New Roman', 8),
                                text="Username should be less than 10 characters long \n"
                                     "Username should not contain spaces \n"
                                     "Username can contain _ to separate words")
        self.instructions.pack(fill=X,pady=3, padx=20)

        self.enterpassFrame1 = Frame(self.registerFrame, bg='#2C3539')
        self.enterpassFrame1.pack(padx=20, pady=(0,2), fill=X)
        self.enterpassLabel1 = Label(self.enterpassFrame1, text="Enter your password", bg='#2C3539', fg='#F5FFFA',
                                     font=('Times New Roman', 8))
        self.enterpassLabel1.pack(side=LEFT, fill=X)
        self.capsLabel21 = Label(self.enterpassFrame1, text="Caps Lock is ON", bg='#2C3539', fg='#F5FFFA',
                                 font=('Times New Roman', 8))
        self.S21 = StringVar()
        self.enterpass1 = Entry(self.registerFrame, bg='Grey', textvariable=self.S21, show='*'
                                , validate="key", validatecommand=(self.vcmd,'%P'))
        self.enterpass1.pack(fill=X, padx=20, pady=(0,3))

        self.enterpassFrame2 = Frame(self.registerFrame, bg='#2C3539')
        self.enterpassFrame2.pack(padx=20, pady=2, fill=X)
        self.enterpassLabel2 = Label(self.enterpassFrame2, text="Confirm your password", bg='#2C3539', fg='#F5FFFA',
                                     font=('Times New Roman', 8))
        self.enterpassLabel2.pack(side=LEFT, fill=X)
        self.capsLabel22=Label(self.enterpassFrame2, text="Caps Lock is ON", bg='#2C3539', fg='#F5FFFA',
                                     font=('Times New Roman', 8))
        self.S22 = StringVar()
        self.enterpass2 = Entry(self.registerFrame, bg='Grey', textvariable=self.S22, show='*'
                                , validate="key", validatecommand=(self.vcmd,'%P'))
        self.enterpass2.pack(fill=X, padx=20)

        self.instructions2=Label(self.registerFrame, bg='#2C3539', fg='#F5FFFA',font=('Times New Roman', 8),
                                text="Password should be less than 10 characters long \n"
                                     "Both Passwords should match \n"
                                     "Passwords may not contain spaces")
        self.instructions2.pack(padx=20, fill=X, pady=(3,0))

        self.registerButton = Button(self.registerFrame, text="Register", bg='Light Blue', fg='Black'
                                  , activeforeground='Black', activebackground='Light Blue'
                                  , relief=FLAT, font=("Times New Roman", 25)
                                  , cursor='hand2', command=self.registe)
        self.registerButton.pack(ipadx=30, ipady=4, padx=20, pady=(15, 4))

        self.msgLabel2=Label(self.registerFrame, bg='#2C3539', font=("Times New Roman", 8), fg='Red')
        self.msgLabel2.pack(pady=(3,4), padx=20, fill=X, expand=True)

        self.checkFrame2=Frame(self.registerFrame, bg='#2C3539')
        self.checkFrame2.pack(fill=X, expand=True, pady=(0,10), padx=20)

        self.textFrame2=Frame(self.checkFrame2, bg='#2C3539')
        self.textFrame2.pack(fill=X, side=LEFT, expand=True)
        self.alText2=Label(self.textFrame2, bg='#2C3539', fg='#F5FFFA', text="Already Have an account?")
        self.alText2.pack(side=RIGHT)
        self.buttonFrame2=Frame(self.checkFrame2, bg='#2C3539')
        self.buttonFrame2.pack(fill=X, side=RIGHT, expand=True)
        self.buttonText2=Button(self.buttonFrame2, text="Login", bg='#2C3539', fg='Light Blue', cursor='hand2'
                                , relief=FLAT, activebackground='#2C3539', activeforeground='#F5FFFA'
                                , command=lambda: self.changeFrame(self.mainframe))
        self.buttonText2.pack(side=LEFT)

def main():
    root = Tk()
    root.title("Login")
    root.configure(bg='Black')
    root.resizable(False, False)
    login = loginSystem(root)
    login.username.bind("<Key>", lambda event: login.labelChange(-1, True))
    login.password.bind("<Key>", lambda event: login.labelChange(-1, True))
    login.username.bind("<Key>", lambda event: login.charUserCount(event.char))
    login.password.bind("<Key>", lambda event: login.charPassCount(event.char))
    root.bind("<Lock-KeyRelease>", login.capsON)
    root.bind("<Lock-KeyPress>", login.capsOFF)
    root.bind("<Return>", login.login)
    root.bind("<Return>", login.registe)
    root.bind("<Button-1>", lambda event: login.initFocus(event))
    login.username.bind("<Button-1>", lambda event: login.focuscheck(login.username))
    login.password.bind("<Button-1>", lambda event: login.focuscheck(login.password))
    login.enteruser.bind("<Button-1>", lambda event: login.focuscheck(login.enteruser))
    login.enterpass1.bind("<Button-1>", lambda event: login.focuscheck(login.enterpass1))
    login.enterpass2.bind("<Button-1>", lambda event: login.focuscheck(login.enterpass2))
    login.autofill.protocol("WM_DELETE_WINDOW",login.autofill.withdraw)
    login.mainloop()



if __name__ == '__main__':
    main()