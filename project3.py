from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
from tkinter.ttk import Combobox,Scrollbar,Treeview,Style
import sqlite3
from datetime import datetime

con=sqlite3.connect(database="RSB_bank.sqlite")
cur=con.cursor()
table1="create table accounts(account_no integer primary key autoincrement,account_name text,account_pass text,account_email text,account_mob text,account_type text,account_bal float,account_open_date text,pin integer)"
table2="create table txn(txn_account_no int,txn_amt float,txn_update_bal float,txn_date text,txn_type text, foreign key(txn_account_no) references accounts(account_no))"
try:
    cur.execute(table1)
    cur.execute(table2)
    print("Tables created")
except:
    pass
con.commit()
con.close()

win=Tk()
win.state("zoomed")
win.resizable(False,False)
win.title("RSB Bank")
win.iconbitmap("iconbank.ico")
win.configure(bg="#ffffff")

img=Image.open("newlogo2.png").resize((170,122))
imgtk=ImageTk.PhotoImage(img,master=win)

logo=Label(win,image=imgtk)
logo.place(relx=0,rely=0)

lbl_txt=Label(win,text="RSB Bank",font=("Arial",38,"bold","italic"),fg="#004f71",bg="white")
lbl_txt.place(relx=0.4,rely=0.032)
lbl_slogan=Label(win,text="your money matters...",font=("Arial",15,"italic"),fg="#004f71",bg="white")
lbl_slogan.place(relx=0.45,rely=0.093)

lbl_txt=Label(win,text=" ",font=("Arial",38,"bold","italic"),fg="#004f71",bg="white",width=1,height=2)
lbl_txt.pack(side="left",anchor=N,padx=160)

def login_page():

    scvalue1=StringVar()
    scvalue2=StringVar()
    
    def signin():
        global acnsign
        acnsign=ent_acn_no.get()
        pwd=ent_acn_pass.get()

        if(acnsign=="" and pwd==""):
            return
        elif(acnsign=="" or pwd==""):
            if(not(acnsign=="")):
                messagebox.showwarning("Warning","Please, Enter Password")
                return
            else:
                messagebox.showwarning("Warning","Please, Enter Account number")
                return

        for i in acnsign:
                index=acnsign.index(i)
                value=ord(acnsign[index])
                
                if(value<48 or value>57):
                    messagebox.showwarning("Warning","Account number must be numberic")
                    return

        con=sqlite3.connect(database="RSB_bank.sqlite")
        cur=con.cursor()
        cur.execute(f"select account_no,account_pass from accounts where account_no=? and account_pass=?",(acnsign,pwd))
        tup=cur.fetchone()
        con.commit()
        con.close()

        iacn=int(acnsign)
        if(tup==None):
            con=sqlite3.connect(database="RSB_bank.sqlite")
            cur=con.cursor()
            cur.execute(f"select account_no from accounts where account_no=?",(acnsign,))
            tup2=cur.fetchone()
            con.commit()
            con.close()

            if(tup2==None):
                messagebox.showerror("Input Error","Invalid details")
                reset()
                return
            else:
                messagebox.showerror("Input Error","Your Password is incorrect")
                return
     
        elif(tup[0]==iacn and tup[1]==pwd):
            frame_login.destroy()
            next_page()
            
    def signup():
        frame_login.destroy()
        signup_page()

    def forgetpage():
        frame_login.destroy()
        forgot_page()

    def reset():
        global acn,password
        acn=""
        password=""
        scvalue1.set(acnsign)
        scvalue2.set(password)

    frame_login=Frame(win)
    frame_login.config(bg="#0f3d52")
    frame_login.place(relx=0,rely=.15,relwidth=1,relheight=1)

    subframe_login=Frame(frame_login)
    subframe_login.config(bg="#004f71",bd=10)
    subframe_login.place(relx=0.2,rely=0,relwidth=0.6,relheight=1)

    lbl_login=Label(subframe_login,text="Please, Sign in-",font=("high tower",26,"bold","italic"),bg="#004f71",fg="white")
    lbl_login.place(relx=.18,rely=0.08)

    lbl_acn_no=Label(subframe_login,text="Account Number ",font=("high tower",21),bg="#004f71",fg="black")
    lbl_acn_no.place(relx=.18,rely=0.2)
    lbl_=Label(subframe_login,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    lbl_.place(relx=.43,rely=0.2)
    ent_acn_no=Entry(subframe_login,bd=1,font=('Arial',20),textvariable=scvalue1)
    ent_acn_no.focus()
    ent_acn_no.place(relx=.48,rely=0.2)


    lbl_acn_pass=Label(subframe_login,text="Password ",font=("high tower",21),bg="#004f71",fg="black")
    lbl_acn_pass.place(relx=.18,rely=0.3)
    lbl_=Label(subframe_login,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    lbl_.place(relx=.43,rely=0.3)
    ent_acn_pass=Entry(subframe_login,bd=1,font=('Arial',20),show="*",textvariable=scvalue2)
    ent_acn_pass.place(relx=.48,rely=0.3)

    btn_sumit=Button(subframe_login,text="Sign in",font=("high tower",18),bg="#0f3d52",bd=1,fg="white",command=signin,width=7)
    btn_sumit.place(relx=.36,rely=.4)

    btn_reset=Button(subframe_login,text="Reset",font=("high tower",18),bg="#0f3d52",bd=1,fg="white",command=reset,width=7)
    btn_reset.place(relx=.512,rely=.4)

    btn_forget=Button(subframe_login,text="Forget Password",font=("high tower",18),command=forgetpage,bg="#0f3d52",bd=1,fg="white",width=17)
    btn_forget.place(relx=.36,rely=.49)

    btn_signup=Button(subframe_login,text="Sign up, to create a new account",font=("high tower",15,"italic"),bg="#004f71",bd=0,fg="white",command=signup)
    btn_signup.place(relx=.324,rely=.56)


def signup_page():

    scvalue1=StringVar()
    scvalue2=StringVar()
    scvalue3=StringVar()
    scvalue4=StringVar()
    scvalue5=StringVar()

    def back():
        frame_signup.destroy()
        login_page()

    def reset():
        global acn,password
        name=""
        email=""
        password=""
        mob=""
        typ="Saving"
        scvalue1.set(name)
        scvalue2.set(password)
        scvalue3.set(email)
        scvalue4.set(mob)
        scvalue5.set(typ)

    def next():
        global name,pwd,email,mob,typ,bal,opendt
        name=signup_name_ent.get()
        pwd=signup_pass_ent.get()
        email=signup_email_ent.get()
        mob=signup_mob_ent.get()
        opendt=datetime.now().date()
        typ=singup_typ.get()
        if(typ=="Saving"):
            bal=0
        else:
            bal=1000

        if(name=="" and pwd=="" and email=="" and mob==""):
            return

        elif(name=="" or pwd=="" or email=="" or mob==""):
                if(not(mob=="") and not(pwd=="") and not(email=="")):
                    messagebox.showwarning("Warning","Please, Enter Name")
                    return
                elif(not(name=="") and not(mob=="") and not(email=="")):
                    messagebox.showwarning("Warning","Please, Enter Password")
                    return
                elif(not(name=="") and not(mob=="") and not(pwd=="")):
                    messagebox.showwarning("Warning","Please, Enter Email address")
                    return
                elif(not(name=="") and not(pwd=="") and not(email=="")):
                    messagebox.showwarning("Warning","Please, Enter Mobile number")
                    return
                else:
                    messagebox.showwarning("Warning","Please, Enter all details")
                    return

        elif(("@gmail.com" in email)==False):
            messagebox.showwarning("Warning","Please, Enter valid email address")
            return
        else:
            for i in mob:
                    index=mob.index(i)
                    value=mob[index]
                    digit=ord(value)
                    if(digit<48 or digit>57):
                        messagebox.showwarning("Warning","Mobile number must be numberic")
                        return

            if( not(mob[0]=='9' or mob[0]=='8' or mob[0]=='7' or mob[0]=='6') or len(mob)<10 or len(mob)>10):
                    messagebox.showwarning("Warning","Please, Enter valid Mobile number")
                    return
            elif(len(pwd)<4):
                    messagebox.showwarning("Warning","Password should contain 4 characters or more")
                    return

            else:
                def done_db():
                    pin=signup2_PIN_ent.get()
                    
                    if(pin==""):
                        messagebox.showwarning("Warning","PIN can't be Empty")
                        return

                    for i in pin:
                        index=pin.index(i)
                        value=ord(pin[index])

                        if(value<48 or value>57):
                            messagebox.showwarning("Warning","PIN must be numberic")
                            return
                    
                    if(len(pin)>4 or len(pin)<4):
                        messagebox.showwarning("Warning","Enter 4 digit PIN")
                        return

                    else:
                        ipin=int(pin)
                        con=sqlite3.connect("RSB_bank.sqlite")
                        cur=con.cursor()
                        cur.execute("insert into Accounts (account_name,account_pass,account_email,account_mob,account_type,account_bal,account_open_date,pin)values(?,?,?,?,?,?,?,?)",(name,pwd,email,mob,typ,bal,opendt,ipin))
                        cur.execute("select account_name,max(account_no) from accounts")
                        tup=cur.fetchone()
                        con.commit()
                        con.close()
                        messagebox.showinfo("Success",f"Congratulation {tup[0]}, Your Account number is {tup[1]}")
                        subframe2_signup.destroy()
                        login_page()

                subframe_signup.destroy()
                subframe2_signup=Frame(frame_signup)
                subframe2_signup.config(bg="#004f71",bd=10)
                subframe2_signup.place(relx=0.2,rely=0,relwidth=0.6,relheight=1)

                signup2_acn_no=Label(subframe2_signup,text="Please create your 4 digit PIN",font=("high tower",23,"bold"),bg="#004f71",fg="white")
                signup2_acn_no.place(relx=.25,rely=0.1)

                signup2_PIN_lbl=Label(subframe2_signup,text="PIN",font=("high tower",21),bg="#004f71",fg="black")
                signup2_PIN_lbl.place(relx=.208,rely=0.27)
                signup2_=Label(subframe2_signup,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
                signup2_.place(relx=.39,rely=0.27)
                signup2_PIN_ent=Entry(subframe2_signup,bd=1,font=('Arial',20))
                signup2_PIN_ent.place(relx=.44,rely=0.27)

                signup2_note=Label(subframe2_signup,text="• PIN makes your transcations secure,Please don't share your PIN and Password",font=("high tower",12,"bold"),bg="#004f71",fg="#151922")
                signup2_note.place(relx=.208,rely=0.34)

                singup2_btn_sumit=Button(subframe2_signup,text="Done",font=("high tower",18),bg="#0f3d52",bd=1,fg="white",command=done_db,width=7)
                singup2_btn_sumit.place(relx=.445,rely=.5)

    
        
    frame_signup=Frame(win)
    frame_signup.config(bg="#0f3d52")
    frame_signup.place(relx=0,rely=.15,relwidth=1,relheight=1)

    subframe_signup=Frame(frame_signup)
    subframe_signup.config(bg="#004f71",bd=10)
    subframe_signup.place(relx=0.2,rely=0,relwidth=0.6,relheight=1)

    btn_back=Button(frame_signup,text="←",font=("Arial",26,"bold"),fg="white",bg="#0f3d52",command=back,bd=0)
    btn_back.place(relx=0,rely=0)

    signup_acn_no=Label(subframe_signup,text="Welcome to ",font=("high tower",26,"bold"),bg="#004f71",fg="white")
    signup_acn_no.place(relx=.266,rely=0.05)

    signup_acn_no=Label(subframe_signup,text="RSB BANK",font=("high tower",26,"bold","italic"),bg="#004f71",fg="white")
    signup_acn_no.place(relx=.502,rely=0.05)

    signup_name_lbl=Label(subframe_signup,text="Name",font=("high tower",21),bg="#004f71",fg="black")
    signup_name_lbl.place(relx=.208,rely=0.17)
    signup_=Label(subframe_signup,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    signup_.place(relx=.39,rely=0.17)
    signup_name_ent=Entry(subframe_signup,bd=1,font=('Arial',20),textvariable=scvalue1)
    signup_name_ent.focus()
    signup_name_ent.place(relx=.44,rely=0.17)

    signup_pass_lbl=Label(subframe_signup,text="Password",font=("high tower",21),bg="#004f71",fg="black")
    signup_pass_lbl.place(relx=.208,rely=0.27)
    signup_=Label(subframe_signup,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    signup_.place(relx=.39,rely=0.27)
    signup_pass_ent=Entry(subframe_signup,bd=1,font=('Arial',20),textvariable=scvalue2,show="*")
    signup_pass_ent.place(relx=.44,rely=0.27)

    signup_email_lbl=Label(subframe_signup,text="Email ID",font=("high tower",21),bg="#004f71",fg="black")
    signup_email_lbl.place(relx=.208,rely=0.37)
    signup_=Label(subframe_signup,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    signup_.place(relx=.39,rely=0.37)
    signup_email_ent=Entry(subframe_signup,bd=1,font=('Arial',20),textvariable=scvalue3)
    signup_email_ent.place(relx=.44,rely=0.37)

    signup_mob_lbl=Label(subframe_signup,text="Mobile no.",font=("high tower",21),bg="#004f71",fg="black")
    signup_mob_lbl.place(relx=.208,rely=0.47)
    signup_=Label(subframe_signup,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    signup_.place(relx=.39,rely=0.47)
    signup_mob_ent=Entry(subframe_signup,bd=1,font=('Arial',20),textvariable=scvalue4)
    signup_mob_ent.place(relx=.44,rely=0.47)
    
    signup_mob_lbl=Label(subframe_signup,text="Acn. type",font=("high tower",21),bg="#004f71",fg="black")
    signup_mob_lbl.place(relx=.208,rely=0.57)
    signup_=Label(subframe_signup,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    signup_.place(relx=.39,rely=0.57)
    singup_typ=Combobox(subframe_signup,values=["Saving","Current"],font=("high tower",19),width=20,textvariable=scvalue5)
    singup_typ.current(0)
    singup_typ.place(relx=.44,rely=.57)

    singup_btn_sumit=Button(subframe_signup,text="Next",font=("high tower",18),bg="#0f3d52",bd=1,fg="white",command=next,width=7)
    singup_btn_sumit.place(relx=.375,rely=.69)

    sign_btn_reset=Button(subframe_signup,text="Reset",font=("high tower",18),bg="#0f3d52",bd=1,fg="white",command=reset,width=7)
    sign_btn_reset.place(relx=.52165,rely=.69)

def next_page():

    con=sqlite3.connect("RSB_bank.sqlite")
    cur=con.cursor()
    cur.execute("select account_name,account_no,account_pass,pin,account_bal,account_email,account_mob from accounts where account_no=?",(acnsign,))
    tup=cur.fetchone()
    con.commit()
    con.close()

    def logout():
        def back(event):
            logoutframe.destroy()
            next_page()
            
        def exit():
            pwd=logout_pass_ent.get()
            
            if(pwd==""):
                return

            elif(tup[2]==pwd):
                logoutframe.destroy()
                login_page()
            else:
                messagebox.showerror("Input Error","Wrong Password")
                return

        logoutframe=Frame(subframe_next)
        logoutframe.config(bg ="#0f3d52",highlightthickness=2,highlightbackground="#002230",highlightcolor="#002230")
        logoutframe.place(relx=0.15,rely=.15,relwidth=0.7,relheight=0.6)
        lbl_welcome.config(text="Enter your Password to log-out",font=("high tower",22),fg="white")
        lbl_welcome.place(relx=.278,rely=.06)

        lbl_cross=Label(logoutframe,text="X",bg="#0f3d52",fg="black",font=("high tower",15),width=1,height=1)
        lbl_cross.place(relx=.963,rely=.01)
        lbl_cross.bind("<Button>",back)

        logout_pass_lbl=Label(logoutframe,text="Password",font=("high tower",21),bg="#0f3d52",fg="black")
        logout_pass_lbl.place(relx=.13,rely=0.29)
        logout_pass_ent=Entry(logoutframe,bd=1,font=('Arial',20))
        logout_pass_ent.place(relx=.40,rely=0.29)
        logout_pass_ent.focus()

        btn_logout=Button(logoutframe,text="Log-out",font=("Arial",17,"bold"),fg="white",bg="#0f3d52",command=exit,bd=1)
        btn_logout.place(relx=.42,rely=.49)
    
    def checkbal():

        def back(event):
            checkframe.destroy()
            next_page()

        def check():
            def back(event):
                checkframe2.destroy()
                next_page()

            pin=checkframe_pin_ent.get()
            if(pin==""):
                return

            ipin=int(pin)

            if(tup[3]==ipin):
                    checkframe.destroy()
                    checkframe2=Frame(subframe_next)
                    checkframe2.config(bg ="#0f3d52",highlightthickness=2,highlightbackground="#002230",highlightcolor="#002230")
                    checkframe2.place(relx=0.15,rely=.15,relwidth=0.7,relheight=0.6)
                    lbl_welcome.config(text="Your Current balance",font=("high tower",22),fg="white")
                    lbl_welcome.place(relx=.362,rely=.06)
                    lbl_cross=Label(checkframe2,text="X",bg="#0f3d52",fg="black",font=("high tower",15),width=1,height=1)
                    lbl_cross.place(relx=.963,rely=.01)
                    lbl_cross.bind("<Button>",back)

                    lbl_bal_name=Label(checkframe2,text="Name         -",bg="#0f3d52",fg="black",font=("high tower",23))
                    lbl_bal_name.place(relx=.24,rely=.32)
                    lbl_bal_namer=Label(checkframe2,text=f"{tup[0]}",bg="#0f3d52",fg="white",font=("high tower",23))
                    lbl_bal_namer.place(relx=.54,rely=.32)

                    lbl_bal_acn=Label(checkframe2,text="Account no -",bg="#0f3d52",fg="black",font=("high tower",23))
                    lbl_bal_acn.place(relx=.24,rely=.42)
                    lbl_bal_acnr=Label(checkframe2,text=f"{ tup[1]}",bg="#0f3d52",fg="white",font=("high tower",23))
                    lbl_bal_acnr.place(relx=.54,rely=.42)

                    lbl_bal_bal=Label(checkframe2,text="Balance      -",bg="#0f3d52",fg="black",font=("high tower",23))
                    lbl_bal_bal.place(relx=.24,rely=.52)
                    lbl_bal_balr=Label(checkframe2,text=f"{tup[4]}",bg="#0f3d52",fg="white",font=("high tower",23))
                    lbl_bal_balr.place(relx=.54,rely=.52)
            else:
                messagebox.showerror("Input Error","Incorrect PIN")
                return

        checkframe=Frame(subframe_next)
        checkframe.config(bg ="#0f3d52",highlightthickness=2,highlightbackground="#002230",highlightcolor="#002230")
        checkframe.place(relx=0.15,rely=.15,relwidth=0.7,relheight=0.6)
        lbl_welcome.config(text="Enter PIN number",font=("high tower",22),fg="white")
        lbl_welcome.place(relx=.385,rely=.06)
        lbl_cross=Label(checkframe,text="X",bg="#0f3d52",fg="black",font=("high tower",15),width=1,height=1)
        lbl_cross.place(relx=.963,rely=.01)
        lbl_cross.bind("<Button>",back)

        checkframe_pin_lbl=Label(checkframe,text="PIN",font=("high tower",21),bg="#0f3d52",fg="black")
        checkframe_pin_lbl.place(relx=.15,rely=0.29)
        checkframe_pin_ent=Entry(checkframe,bd=1,font=('Arial',20))
        checkframe_pin_ent.place(relx=.39,rely=0.29)
        checkframe_pin_ent.focus()

        btn_check=Button(checkframe,text="Check",font=("Arial",17,"bold"),fg="white",bg="#0f3d52",command=check,bd=1)
        btn_check.place(relx=.44,rely=.49)


    def deposit_db():
        def back(event):
            depositframe.destroy()
            next_page()

        def Done():
            acn=tup[1]
            pin=ent_pin.get()
            amt=ent_amt.get()
            txn_typ="Credit"
            txn_dt=str(datetime.now())

            if(amt=="" and pin==""):
                return
            elif(amt=="" and pin!=""):
                messagebox.showwarning("Warning","Enter Amount")
                return
            elif(amt!="" and pin==""):
                for i in amt:
                    index=amt.index(i)
                    value=ord(amt[index])
                    if(value<48 or value>57):
                        messagebox.showwarning("Warning","Enter Amount")
                        return
                messagebox.showwarning("Warning","Enter PIN")
                return
                
            try:
                ipin=int(pin) 
                iamt=float(amt)
                if(ipin==tup[3]):
                    con=sqlite3.connect("RSB_bank.sqlite")
                    cur=con.cursor()
                    cur.execute("update accounts set account_bal =account_bal+? where account_no=? and pin=?",(iamt,acn,ipin))
                    con.commit()
                    con.close()

                    con=sqlite3.connect("RSB_bank.sqlite")
                    cur=con.cursor()
                    cur.execute("select account_bal from accounts where account_no=?",(acn,))
                    tup2=cur.fetchone()
                    con.commit()
                    con.close()

                    up_bal=tup2[0]

                    con=sqlite3.connect("RSB_bank.sqlite")
                    cur=con.cursor()
                    cur.execute("insert into txn values(?,?,?,?,?)",(acn,iamt,up_bal,txn_dt,txn_typ))
                    con.commit()
                    con.close()

                    messagebox.showinfo("Success","Amount Deposit successfully")
                    depositframe.destroy()
                    next_page()
                else:
                    messagebox.showerror("Input Error","Incorrect PIN number")
                    return
            except:
                messagebox.showerror("Input Error","Incorrect PIN number")
                return

        depositframe=Frame(subframe_next)
        depositframe.config(bg ="#0f3d52",highlightthickness=2,highlightbackground="#002230",highlightcolor="#002230")
        depositframe.place(relx=0.15,rely=.15,relwidth=0.7,relheight=0.6)
        lbl_welcome.config(text="Deposit",font=("high tower",22),fg="white")
        lbl_welcome.place(relx=.43,rely=.06)
        lbl_cross=Label(depositframe,text="X",bg="#0f3d52",fg="black",font=("high tower",15),width=1,height=1)
        lbl_cross.place(relx=.963,rely=.01)
        lbl_cross.bind("<Button>",back)

        lbl_bal_name=Label(depositframe,text="Enter amount  ",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_bal_name.place(relx=.13,rely=.27)
        ent_amt=Entry(depositframe,bd=1,font=('Arial',19))
        ent_amt.place(relx=.45,rely=0.27)
        ent_amt.focus()

        lbl_pin=Label(depositframe,text="PIN number    ",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_pin.place(relx=.13,rely=.42)
        ent_pin=Entry(depositframe,bd=1,font=('Arial',19))
        ent_pin.place(relx=.45,rely=0.42)

        btn_done=Button(depositframe,text="Done",font=("Arial",17,"bold"),fg="white",bg="#0f3d52",command=Done,bd=1)
        btn_done.place(relx=.44,rely=.6)

    def Withdrawal_db():
        def back(event):
            withdrawalframe.destroy()
            next_page()

        def Done():
            acn=tup[1]
            pin=ent_pin.get()
            amt=ent_amt.get()
            txn_typ="Debit"
            txn_dt=str(datetime.now())

            if(amt=="" and pin==""):
                return
            elif(amt=="" and pin!=""):
                messagebox.showwarning("Warning","Enter Amount")
                return
            elif(amt!="" and pin==""):
                for i in amt:
                    index=amt.index(i)
                    value=ord(amt[index])
                    if(value<48 or value>57):
                        messagebox.showwarning("Warning","Enter Amount")
                        return
                messagebox.showwarning("Warning","Enter PIN")
                return
                
            try:
                ipin=int(pin) 
                iamt=float(amt)
                if(ipin==tup[3]):
                    con=sqlite3.connect("RSB_bank.sqlite")
                    cur=con.cursor()
                    cur.execute("update accounts set account_bal =account_bal-? where account_no=? and pin=?",(iamt,acn,ipin))
                    con.commit()
                    con.close()

                    con=sqlite3.connect("RSB_bank.sqlite")
                    cur=con.cursor()
                    cur.execute("select account_bal from accounts where account_no=?",(acn,))
                    tup3=cur.fetchone()
                    con.commit()
                    con.close()

                    up_bal=tup3[0]

                    con=sqlite3.connect("RSB_bank.sqlite")
                    cur=con.cursor()
                    cur.execute("insert into txn values(?,?,?,?,?)",(acn,iamt,up_bal,txn_dt,txn_typ))
                    con.commit()
                    con.close()

                    messagebox.showinfo("Success","Amount Withdrawal successfully")
                    withdrawalframe.destroy()
                    next_page()
                else:
                    messagebox.showerror("Input Error","Incorrect PIN number")
                    return
            except:
                messagebox.showerror("Input Error","Incorrect PIN number")
                return

        withdrawalframe=Frame(subframe_next)
        withdrawalframe.config(bg ="#0f3d52",highlightthickness=2,highlightbackground="#002230",highlightcolor="#002230")
        withdrawalframe.place(relx=0.15,rely=.15,relwidth=0.7,relheight=0.6)
        lbl_welcome.config(text="Withdrawal",font=("high tower",22),fg="white")
        lbl_welcome.place(relx=.42,rely=.06)
        lbl_cross=Label(withdrawalframe,text="X",bg="#0f3d52",fg="black",font=("high tower",15),width=1,height=1)
        lbl_cross.place(relx=.963,rely=.01)
        lbl_cross.bind("<Button>",back)

        lbl_bal_name=Label(withdrawalframe,text="Enter amount  ",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_bal_name.place(relx=.13,rely=.27)
        ent_amt=Entry(withdrawalframe,bd=1,font=('Arial',19))
        ent_amt.place(relx=.45,rely=0.27)
        ent_amt.focus()

        lbl_pin=Label(withdrawalframe,text="PIN number    ",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_pin.place(relx=.13,rely=.42)
        ent_pin=Entry(withdrawalframe,bd=1,font=('Arial',19))
        ent_pin.place(relx=.45,rely=0.42)

        btn_done=Button(withdrawalframe,text="Done",font=("Arial",17,"bold"),fg="white",bg="#0f3d52",command=Done,bd=1)
        btn_done.place(relx=.44,rely=.6)


    def update_db():
        def back(event):
            updateframe.destroy()
            next_page()

        def Done_db():
            acn=tup[1]
            name=ent_amt.get()
            pwd=ent_pass.get()
            email=ent_email.get()
            mob=ent_mob.get()
            pin=ent_pin.get()

            if(name=="" or pwd=="" or email=="" or mob=="" or pin==""):
                return
            elif(name=="" and pwd=="" and email=="" and mob=="" and pin==""):
                return
        
            con=sqlite3.connect("RSB_bank.sqlite")
            cur=con.cursor()
            cur.execute("update accounts set account_name=?,account_pass=?,account_email=?,account_mob=?,pin=? where account_no=?",(name,pwd,email,mob,pin,acn))
            con.commit()
            con.close()
            messagebox.showinfo("Success","Profile Updated")
            updateframe.destroy()
            next_page()
               

        updateframe=Frame(subframe_next)
        updateframe.config(bg ="#0f3d52",highlightthickness=2,highlightbackground="#002230",highlightcolor="#002230")
        updateframe.place(relx=0.15,rely=.15,relwidth=0.7,relheight=0.6)
        lbl_welcome.config(text="Update your profile",font=("high tower",22),fg="white")
        lbl_welcome.place(relx=.37,rely=.06)
        lbl_cross=Label(updateframe,text="X",bg="#0f3d52",fg="black",font=("high tower",15),width=1,height=1)
        lbl_cross.place(relx=.963,rely=.01)
        lbl_cross.bind("<Button>",back)

        lbl_bal_name=Label(updateframe,text="Name",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_bal_name.place(relx=.13,rely=.15)
        ent_amt=Entry(updateframe,bd=1,font=('Arial',19))
        ent_amt.place(relx=.45,rely=0.15)
        ent_amt.focus()
        ent_amt.insert(0,tup[0])

        lbl_pass=Label(updateframe,text="Password",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_pass.place(relx=.13,rely=.28)
        ent_pass=Entry(updateframe,bd=1,font=('Arial',19))
        ent_pass.place(relx=.45,rely=0.28)
        ent_pass.insert(0,tup[2])

        lbl_email=Label(updateframe,text="Email",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_email.place(relx=.13,rely=.41)
        ent_email=Entry(updateframe,bd=1,font=('Arial',19))
        ent_email.place(relx=.45,rely=0.41)
        ent_email.insert(0,tup[5])
    

        lbl_mob=Label(updateframe,text="Mobile",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_mob.place(relx=.13,rely=.54)
        ent_mob=Entry(updateframe,bd=1,font=('Arial',19))
        ent_mob.place(relx=.45,rely=0.54)
        ent_mob.insert(0,tup[6])

        lbl_pin=Label(updateframe,text="PIN",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_pin.place(relx=.13,rely=.67)
        ent_pin=Entry(updateframe,bd=1,font=('Arial',19))
        ent_pin.place(relx=.45,rely=0.67)
        ent_pin.insert(0,tup[3])

        btn_done=Button(updateframe,text="Done",font=("Arial",17,"bold"),fg="white",bg="#0f3d52",command=Done_db,bd=1)
        btn_done.place(relx=.44,rely=.82)

    def transfer():
        def back(event):
            transframe.destroy()
            next_page()
        def next():
            def back(event):
                transframe2.destroy()
                transfer()

            def transfer_db():
                pin=transframe2_pin_ent.get()
                if(pin==""):
                    return

                ipin=int(pin)

                if(tup[3]==ipin):

                        amt=ent_amt.get()
                        acn2=ent_to_acn.get()
                        iacn2=int(acn2)
                        iamt=float(amt)
                        acn1=tup[1]
                        acn_txntype="Debit"
                        acn2_txntype="Credit"
                        dt=str(datetime.now())

                        con=sqlite3.connect("RSB_bank.sqlite")
                        cur=con.cursor()
                        cur.execute("select * from accounts where account_no=?",(acn2,))
                        row=cur.fetchone()
                        con.close()

                        if(row==None):
                            messagebox.showerror("Input Error","Account does not found")
                            return
                        else:
                            con=sqlite3.connect("RSB_bank.sqlite")
                            cur=con.cursor()
                            cur.execute("select account_bal from accounts where account_no=?",(acn1,))
                            bal=cur.fetchone()[0]
                            con.close()

                            con=sqlite3.connect("RSB_bank.sqlite")
                            cur=con.cursor()
                            cur.execute("select account_bal from accounts where account_no=?",(acn2,))
                            bal2=cur.fetchone()[0]
                            con.close()

                            if(bal>=iamt):
                                con=sqlite3.connect("RSB_bank.sqlite")
                                cur=con.cursor()

                                cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(iamt,acn2))
                                cur.execute("update accounts set account_bal=account_bal-? where account_no=?",(iamt,acn1))
                                cur.execute("insert into txn values(?,?,?,?,?)",(acn1,iamt,bal-iamt,dt,acn_txntype))
                                cur.execute("insert into txn values(?,?,?,?,?)",(iacn2,iamt,bal2+iamt,dt,acn2_txntype))
                                con.commit()
                                con.close()

                                messagebox.showinfo("Success","Amount Tranfered")
                                transframe2.destroy()
                                next_page()
                            else:
                                messagebox.showerror("Transfer","Insufficient balance")
                                return

                else:
                    messagebox.showerror("Input Error","Incorrect PIN")
                    return

            transframe2=Frame(subframe_next)
            transframe2.config(bg ="#0f3d52",highlightthickness=2,highlightbackground="#002230",highlightcolor="#002230")
            transframe2.place(relx=0.15,rely=.15,relwidth=0.7,relheight=0.6)
            lbl_welcome.config(text="Enter PIN number",font=("high tower",22),fg="white")
            lbl_welcome.place(relx=.385,rely=.06)
            lbl_cross=Label(transframe2,text="X",bg="#0f3d52",fg="black",font=("high tower",15),width=1,height=1)
            lbl_cross.place(relx=.963,rely=.01)
            lbl_cross.bind("<Button>",back)

            transframe2_pin_lbl=Label(transframe2,text="PIN",font=("high tower",21),bg="#0f3d52",fg="black")
            transframe2_pin_lbl.place(relx=.15,rely=0.29)
            transframe2_pin_ent=Entry(transframe2,bd=1,font=('Arial',20))
            transframe2_pin_ent.place(relx=.39,rely=0.29)
            transframe2_pin_ent.focus()

            btn_check=Button(transframe2,text="Done",font=("Arial",17,"bold"),fg="white",bg="#0f3d52",command=transfer_db,bd=1)
            btn_check.place(relx=.44,rely=.49)



        transframe=Frame(subframe_next)
        transframe.config(bg ="#0f3d52",highlightthickness=2,highlightbackground="#002230",highlightcolor="#002230")
        transframe.place(relx=0.15,rely=.15,relwidth=0.7,relheight=0.6)
        lbl_welcome.config(text="Transfer Amount",font=("high tower",22),fg="white")
        lbl_welcome.place(relx=.36,rely=.06)
        lbl_cross=Label(transframe,text="X",bg="#0f3d52",fg="black",font=("high tower",15),width=1,height=1)
        lbl_cross.place(relx=.963,rely=.01)
        lbl_cross.bind("<Button>",back)

        lbl_bal_amt=Label(transframe,text="Amount",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_bal_amt.place(relx=.13,rely=.25)
        ent_amt=Entry(transframe,bd=1,font=('Arial',19))
        ent_amt.place(relx=.45,rely=0.25)
        ent_amt.focus()

        lbl_to_acn=Label(transframe,text="Transfer to ",bg="#0f3d52",fg="black",font=("high tower",21))
        lbl_to_acn.place(relx=.13,rely=.4)
        ent_to_acn=Entry(transframe,bd=1,font=('Arial',19))
        ent_to_acn.place(relx=.45,rely=0.4)

       
        btn_Transfer=Button(transframe,text="Transfer",font=("Arial",16,"bold"),fg="white",bg="#0f3d52",command=next,bd=1)
        btn_Transfer.place(relx=.42,rely=.6)
    
    def txn_history():
        def back(event):
            historyframe.destroy()
            next_page()

        historyframe=Frame(subframe_next)
        historyframe.config(bg ="#0f3d52",highlightthickness=2,highlightbackground="#002230",highlightcolor="#002230")
        historyframe.place(relx=0.15,rely=.15,relwidth=0.7,relheight=0.6)
        lbl_welcome.config(text="Your Transactions history",font=("high tower",22),fg="white")
        lbl_welcome.place(relx=.33,rely=.06)
        lbl_cross=Label(historyframe,text="X",bg="#0f3d52",fg="black",font=("high tower",15),width=1,height=1)
        lbl_cross.place(relx=.963,rely=.01)
        lbl_cross.bind("<Button>",back)

        lbl_all=Label(historyframe,text="All trans.",bg="#0f3d52",fg="white",font=("high tower",15,"underline"))
        lbl_all.place(relx=.02,rely=.01)
        # lbl_all.bind("<Button>",all_db)


        lbl_de=Label(historyframe,text="Debit",bg="#0f3d52",fg="white",font=("high tower",15))
        lbl_de.place(relx=.16,rely=.01)

        lbl_cr=Label(historyframe,text="Credit",bg="#0f3d52",fg="white",font=("high tower",15))
        lbl_cr.place(relx=.26,rely=.01)

        tv=Treeview(historyframe)
        tv.place(relx=0,rely=0.08,relheight=.9163,relwidth=1)

        style = Style()
        style.configure("Treeview.Heading", font=('Arial',13,'bold'),foreground='Black')
        
        sb=Scrollbar(historyframe,orient='vertical',command=tv.yview)
        sb.place(relx=.974,rely=0.0828,relheight=0.912)
        
        tv['columns']=('Txn date','Txn amount','Txn type','Updated bal')
        
        tv.column('Txn date',width=120,anchor='c')
        tv.column('Txn amount',width=95,anchor='c')
        tv.column('Txn type',width=95,anchor='c')
        tv.column('Updated bal',width=95,anchor='c')

        tv.heading('Txn date',text='Txn date')
        tv.heading('Txn amount',text='Txn amount')
        tv.heading('Txn type',text='Txn type')
        tv.heading('Updated bal',text='Updated bal')
        
        tv['show']='headings'
        
        con=sqlite3.connect(database="RSB_bank.sqlite")
        cur=con.cursor()
        cur.execute("select txn_date,txn_amt,txn_type,txn_update_bal from txn where txn_account_no=?",(acnsign,))
        row=cur.fetchall()
        for i in row:
            tv.insert("","end",values=(i[0],i[1],i[2],i[3]))
            

    frame_next=Frame(win)
    frame_next.config(bg="#0f3d52")
    frame_next.place(relx=0,rely=.15,relwidth=1,relheight=1)

    subframe_next=Frame(frame_next)
    subframe_next.config(bg="#004f71")
    subframe_next.place(relx=0.2,rely=0,relwidth=0.6,relheight=1)

    btn_logout=Button(frame_next,text="Log out",font=("Arial",15,"bold"),fg="white",bg="#0f3d52",command=logout,bd=0)
    btn_logout.place(relx=.935,rely=.01)

    lbl_welcome=Label(subframe_next,text=f"Welcome {tup[0]},",font=("Arial",25,"bold","italic"),bg="#004f71",fg="white")
    lbl_welcome.place(relx=.372,rely=0.060)

    lbl_welcome2=Label(subframe_next,text="Enjoy your banking experience with us.",font=("Arial",21),bg="#004f71",fg="silver")
    lbl_welcome2.place(relx=.227,rely=0.15)

    # lbl_welcome=Label(subframe_next,text="",font=("Arial",22),bg="#004f71",fg="silver")
    # lbl_welcome.place(relx=.227,rely=0.17)

    btn_logout=Button(frame_next,text="Check balance",font=("Arial",17,"bold"),fg="white",bg="#004f71",command=checkbal,bd=1,width=15)
    btn_logout.place(relx=.027,rely=.15)

    btn_logout=Button(frame_next,text="Deposit",font=("Arial",17,"bold"),fg="white",bg="#004f71",command=deposit_db,bd=1,width=15)
    btn_logout.place(relx=.027,rely=.4)

    btn_logout=Button(frame_next,text="Withdrawal",font=("Arial",17,"bold"),fg="white",bg="#004f71",command=Withdrawal_db,bd=1,width=15)
    btn_logout.place(relx=.027,rely=.65)

    btn_logout=Button(frame_next,text="Tranfer amount",font=("Arial",17,"bold"),fg="white",bg="#004f71",command=transfer,bd=1,width=15)
    btn_logout.place(relx=.83,rely=.15)

    btn_logout=Button(frame_next,text="Transactions",font=("Arial",17,"bold"),fg="white",bg="#004f71",command=txn_history,bd=1,width=15)
    btn_logout.place(relx=.83,rely=.4)

    btn_logout=Button(frame_next,text="Update Profile",font=("Arial",17,"bold"),fg="white",bg="#004f71",command=update_db,bd=1,width=15)
    btn_logout.place(relx=.83,rely=.65)

    date=datetime.now().date()
    lbl_datetime=Label(subframe_next,text=f"Date- {date}",font=("Arial",15),bg="#004f71")
    lbl_datetime.place(relx=.8,rely=.78)
    

def forgot_page():

    scvalue1=StringVar()
    scvalue2=StringVar()
    scvalue3=StringVar()

    def reset():
        global acn,password
        email=""
        acn=""
        mob=""
        scvalue1.set(acn)
        scvalue2.set(email)
        scvalue3.set(mob)
       
    def back():
        frame_forgot.destroy()
        login_page()

    def get_db():

        acn=forgot_acn_ent.get()
        mob=forgot_mob_ent.get()
        email=forgot_email_ent.get()

        if(acn=="" and email=="" and mob==""):
            return

        elif(acn=="" or email=="" or mob==""):
            if(not(mob=="") and not(email=="")):
                messagebox.showwarning("Warning","Please, Enter Account number")
                return
            elif(not(acn=="") and not(email=="")):
                messagebox.showwarning("Warning","Please, Enter Mobile number")
                return
            elif(not(acn=="") and not(mob=="")):
                messagebox.showwarning("Warning","Please, Enter Email Address")
                return
            else:
                messagebox.showwarning("Warning","Please, Enter all details")
                return

        else:
            for i in acn:
                    index=acn.index(i)
                    value=ord(acn[index])
                    if(value<48 or value>57):
                        messagebox.showwarning("Warning","Account number must be numberic")
                        return

            if(("@gmail.com" in email)==False):
                messagebox.showwarning("Warning","Please, Enter valid email address")
                return
    
        
            for i in mob:
                    index=mob.index(i)
                    value=mob[index]
                    digit=ord(value)
                    if(digit<48 or digit>57):
                        messagebox.showwarning("Warning","Mobile number must be numberic")
                        return

            if( not(mob[0]=='9' or mob[0]=='8' or mob[0]=='7' or mob[0]=='6') or len(mob)<10 or len(mob)>10):
                messagebox.showwarning("Warning","Please, Enter valid Mobile number")
                return

            else:
                con=sqlite3.connect(database="RSB_bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_pass from accounts where account_no=? and account_mob=? and account_email=?",(acn,mob,email))
                tup=cur.fetchone()
                con.commit()
                con.close()

                iacn=int(acn)
                if(tup==None):
                    con=sqlite3.connect(database="RSB_bank.sqlite")
                    cur=con.cursor()
                    cur.execute(f"select account_no,account_mob from accounts where account_no=? and account_mob=?",(acn,mob))
                    tup2=cur.fetchone()
                    con.commit()
                    con.close()
                    if(tup2==None):
                        con=sqlite3.connect(database="RSB_bank.sqlite")
                        cur=con.cursor()
                        cur.execute(f"select account_no,account_email from accounts where account_no=? and account_email=?",(acn,email))
                        tup3=cur.fetchone()
                        con.commit()
                        con.close()
                        if(tup3==None):
                            messagebox.showerror("Input error","Invalid details")
                            reset()
                            return
                        elif(tup3[0]==iacn and tup3[1]==email):
                            messagebox.showerror("Input error","Your Mobile number is incorrect")
                            return
                    elif(tup2[0]==iacn and tup2[1]==mob):
                        messagebox.showerror("Input error","Your Email address is incorrect")
                        return
                else:
                    messagebox.showinfo("Success",f"Your password is {tup[0]}")
                    back()
          
    frame_forgot=Frame(win)
    frame_forgot.config(bg="#0f3d52")
    frame_forgot.place(relx=0,rely=.15,relwidth=1,relheight=1)

    subframe_forgot=Frame(frame_forgot)
    subframe_forgot.config(bg="#004f71",bd=10)
    subframe_forgot.place(relx=0.2,rely=0,relwidth=0.6,relheight=1)

    lbl_login=Label(subframe_forgot,text="Enter the following details, To know your Password",font=("high tower",22,"bold","italic"),bg="#004f71",fg="white")
    lbl_login.place(relx=.10,rely=0.070)

    btn_back=Button(frame_forgot,text="←",font=("Arial",26,"bold"),fg="white",bg="#0f3d52",command=back,bd=0)
    btn_back.place(relx=0,rely=0)

    forgot_acn_lbl=Label(subframe_forgot,text="Account no.",font=("high tower",21),bg="#004f71",fg="black")
    forgot_acn_lbl.place(relx=.208,rely=0.19)
    forgot_=Label(subframe_forgot,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    forgot_.place(relx=.39,rely=0.19)
    forgot_acn_ent=Entry(subframe_forgot,bd=1,font=('Arial',20),textvariable=scvalue1)
    forgot_acn_ent.focus()
    forgot_acn_ent.place(relx=.44,rely=0.19)

    forgot_email_lbl=Label(subframe_forgot,text="Email ID",font=("high tower",21),bg="#004f71",fg="black")
    forgot_email_lbl.place(relx=.208,rely=0.29)
    forgot_=Label(subframe_forgot,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    forgot_.place(relx=.39,rely=0.29)
    forgot_email_ent=Entry(subframe_forgot,bd=1,font=('Arial',20),textvariable=scvalue2)
    forgot_email_ent.focus()
    forgot_email_ent.place(relx=.44,rely=0.29)

    forgot_mob_lbl=Label(subframe_forgot,text="Mobile no",font=("high tower",21),bg="#004f71",fg="black")
    forgot_mob_lbl.place(relx=.208,rely=0.39)
    forgot_=Label(subframe_forgot,text=":",font=("high tower",20,"bold"),bg="#004f71",fg="black")
    forgot_.place(relx=.39,rely=0.39)
    forgot_mob_ent=Entry(subframe_forgot,bd=1,font=('Arial',20),textvariable=scvalue3)
    forgot_mob_ent.focus()
    forgot_mob_ent.place(relx=.44,rely=0.39)

    forgot_btn_sumit=Button(subframe_forgot,text="Get",font=("high tower",18),bg="#0f3d52",bd=1,fg="white",command=get_db,width=7)
    forgot_btn_sumit.place(relx=.37,rely=.52)

    forgot_btn_reset=Button(subframe_forgot,text="Reset",font=("high tower",18),bg="#0f3d52",bd=1,fg="white",command=reset,width=7)
    forgot_btn_reset.place(relx=.52165,rely=.52)


login_page()
win.mainloop()