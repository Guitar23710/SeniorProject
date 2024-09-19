import cv2
import serial
import threading
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import matplotlib.pyplot as plt
import numpy as np
from tkinter import*
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview
from tkinter import messagebox
from tkinter import PhotoImage
import tkinter
import pymysql
import mysql.connector
from sqlalchemy import create_engine,inspect
import pandas as pd
import glob
import io
from io import BytesIO
import os
import openpyxl
from PIL import Image , ImageTk
from tkinter import filedialog, simpledialog, messagebox #upload รูปภาพ
from tkcalendar import Calendar #ปฏิทิน
import pyodbc
from datetime import datetime
import pytz #ใช้กับ datetime
import time
import csv
# pip install mysqlclient


def sign_up_page():

    def root_signup_page_2():

        def conn_dtb_signuppage2_2():
            if nameuser2.get() == '' or Lastname2.get() == '' or radio2.get()==''or date2.cget("text")=='' or phonenum2.get()=='' :
                messagebox.showerror('Error','All fields Are Require')
            else:
            
                try:
                    con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                    mycursor=con.cursor()
                except:
                    messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                    return
            
                try:
                    query='use userdata_3'
                    mycursor.execute(query)
                except:
                    mycursor.execute('use userdata_3')
            
                query='select * from data where userid=%s'  
                mycursor.execute(query,(User_SignUp.get()))
                query="UPDATE data SET firstname = %s , lastname = %s , gender =%s ,dateofbirth=%s, phone =%s  WHERE userid = %s"
                mycursor.execute(query,(nameuser2.get(),Lastname2.get(),radio2.get(),date2.cget("text"),phonenum2.get(),User_SignUp.get()))
                con.commit()
                con.close()

                messagebox.showinfo('Success','Signup is successful')
                root_signup2.destroy()
                root_signup.destroy()
 

        def selectPic2(): #ใช้ from tkinter import filedialog (ใช้สำหรับการดาวน์โหลดรูปภาพจากไฟล์ภายในเครื่อง)
            global imgselect2
            filename2 = filedialog.askopenfilename(initialdir="/images",title='Select Image',filetypes=(('jpg images','*.jpg'),('png images','*.png')))
            imgselect2 = Image.open(filename2)
            imgselect2 = imgselect2.resize((200,200), Image.LANCZOS) #ANTIALIAS เลิกใช้งานแล้วและจะถูกนำออกใน Pillow 10  ใช้ LANCZOS หรือ Resampling.LANCZOS แทน
            imgselect2 = ImageTk.PhotoImage(imgselect2)
            lbl_show_pic2['image'] = imgselect2
            entry_pic_path2.insert(0,filename2)
            
            def convert_to_binary2(img2):
                with open(img2,'rb') as file:
                    bd2 = file.read()
                return bd2 

            try:
                con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                mycursor=con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                return
        
            try:
                query='use userdata_3'
                mycursor.execute(query)
            except:
                mycursor.execute('use userdata_3')

            query='select * from data where userid=%s'  
            mycursor.execute(query,(User_SignUp.get()))
            query="UPDATE data SET media_name = %s , image = %s WHERE userid = %s"
            pic2 = convert_to_binary2(filename2)
            mycursor.execute(query,(entry_pic_path2.get(),pic2,User_SignUp.get()))
            con.commit()
            con.close()

        root_signup2 = Toplevel(root)
        root_signup2.resizable(False,False) 
        root_signup2.configure(bg='#fff') 
        root_signup2.title('Signup Profile') 
        root_signup2.geometry('925x500+300+200')

        bg_sgup2=Image.open('bg_medical7.jpg')
        bg_sgup2=ImageTk.PhotoImage(bg_sgup2) 
        canvas2=Canvas(root_signup2,width=925,height=500) #canvas = ใช้วาดรูปบนหน้าจอ 
        canvas2.pack()
        canvas2.create_image(0,0,image=bg_sgup2,anchor=CENTER)

        frame_signuppage2 = Frame(root_signup2,width=350,height=400,bg='#F5F5F5')
        frame_signuppage2.pack()
        frame_signuppage2.place(x=500,y=30) 

        nameuser_heading2 = Label(frame_signuppage2,text='First Name:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
        nameuser_heading2.place(x=20,y=35) 
        nameuser2 = Entry(frame_signuppage2,width=20,bg='white',border=2,font=('Jasmine UPC',10))
        nameuser2.place(x=150,y=35) 

        Lastname_heading2 = Label(frame_signuppage2,text='Last Name:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
        Lastname_heading2.place(x=20,y=85)
        Lastname2 = Entry(frame_signuppage2,width=20,bg='white',border=2,font=('Jasmine UPC',10))
        Lastname2.place(x=150,y=85)

        Gender_heading2 = Label(frame_signuppage2,text='Gender:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
        Gender_heading2.place(x=20,y=135)
        radio2=StringVar()
        gd_male2 = Radiobutton(frame_signuppage2,text='Male',bg='#F5F5F5',fg='black',value='Male',variable=radio2)
        gd_male2.place(x=120,y=135)
        gd_female2 = Radiobutton(frame_signuppage2,text='Female',bg='#F5F5F5',fg='black',value='Female',variable=radio2)
        gd_female2.place(x=190,y=135)
        gd_lgbtq2 = Radiobutton(frame_signuppage2,text='lgbtq+',bg='#F5F5F5',fg='black',value='LGBTQ+',variable=radio2)
        gd_lgbtq2.place(x=260,y=135)

        phone_heading2 = Label(frame_signuppage2,text='Phone number:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
        phone_heading2.place(x=20,y=235)
        phonenum2 = Entry(frame_signuppage2,width=20,bg='white',border=2,font=('Jasmine UPC',10))
        phonenum2.place(x=150,y=235)

        daybirth_heading2 = Label(frame_signuppage2,text='Day of birth:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
        daybirth_heading2.place(x=20,y=185)
        
        def birthcalendar2():
            root_bd2 = Toplevel(root_signup2)
            root_bd2.title('Birth Calendar')
            root_bd2.geometry('250x220+850+450')
            root_bd2.resizable(False,False)
            birthcal2 = Calendar(root_bd2, selectmode = 'day',firstweekday='sunday',date_pattern ='dd/mm/y')
            birthcal2.place(x=0,y=0)

            def grad_date2():
                selected_date2 = birthcal2.get_date()
                date2.config(text=selected_date2)
                if date2 != '':
                    root_bd2.destroy()

            bdbutton = Button(root_bd2, text = "Enter Date",command = grad_date2)
            bdbutton.place(x=90,y=190)
        
        date2 = Label(frame_signuppage2, text ='',width=20,bg='white')
        date2.pack()
        date2.place(x=134,y=185)
        bf_btn2 = Button(frame_signuppage2,text='V',bg='white',fg='black',command=birthcalendar2,font=('Jasmine UPC',7),border=1)
        bf_btn2.place(x=280,y=185)

        #part upload picProfile
        imgprofile2 = PhotoImage(file='Profile (1).png')
        frame_profile_signup2 = Frame(root_signup2,width=350,height=400,bg='#F5F5F5')
        frame_profile_signup2.place(x=100,y=30)
        lbl_show_pic2 = Label(frame_profile_signup2,bg='#F0FFFF',highlightthickness=3,image=imgprofile2)
        lbl_show_pic2.place(x=72,y=20)
        ImagePath2 = Label(frame_profile_signup2,text='Image Path:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',9,'bold'))
        ImagePath2.place(x=5,y=260)
        entry_pic_path2 = Entry(frame_profile_signup2,font=('Jasmine UPC',9),width=25)
        entry_pic_path2.place(x=87,y=260)
        btn_browse2 = Button(frame_profile_signup2,font=('Jasmine UPC',8),width=10,border=1,pady=2,text='Select Image',bg='white',command=selectPic2,cursor='hand2')
        btn_browse2.place(x=135,y=300)

        button_signuppage2 = Button(frame_signuppage2,width=25,border=0,bg='#63B8FF',text='Enter',pady=6,command=conn_dtb_signuppage2_2,cursor='hand2')
        button_signuppage2.place(x=85,y=320)
            
        root_signup2.transient(root)
        root_signup2.iconphoto(False, hostuicon)
        root_signup2.mainloop()


    def clear():
        Email_SignUp.delete(0,END)
        User_SignUp.delete(0,END)
        PassWord_SignUp.delete(0,END)
        PassWordConfirm_SignUp.delete(0,END)

    def connect_database(): #ต้องไปดาวน์โหลดและติดตั้ง MySQL กำหนด location Path ของไฟล์ MySQL.EXE ใน bin 
        #เปิด MySQL ใน Command Promp --> พิมพ์ mysql -u root -p --> รหัส Jamesanddef00 --> show databases;
        
        if Email_SignUp.get()=='' or User_SignUp.get()=='' or PassWord_SignUp.get()=='' or PassWordConfirm_SignUp.get()=='':
            messagebox.showerror('Error','All fields Are Require')
        elif len(PassWord_SignUp.get()) < 8:
            messagebox.showerror('Error','Password less than 8 characters')
        elif len(PassWord_SignUp.get()) > 20:
            messagebox.showerror('Error','Password  must be than 20 characters')
        elif PassWord_SignUp.get() != PassWordConfirm_SignUp.get():
            messagebox.showerror('Error','Password Mismatch')
        else:
            try:
                con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                mycursor=con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                return
        
            try:
                query = 'create database userdata_3'
                mycursor.execute(query)
                query='use userdata_3'
                mycursor.execute(query)
                query='create table data(id int auto_increment primary key not null,email varchar(50),userid varchar(50),password varchar(20),firstname varchar(50),lastname varchar(50),gender varchar(15),dateofbirth varchar(15),phone varchar(15),department_ward_unit varchar(50),media_name varchar(100),image LONGBLOB)'
                mycursor.execute(query)
            except:
                mycursor.execute('use userdata_3')

            query='select * from data where userid=%s'  
            mycursor.execute(query,(User_SignUp.get()))
            row = mycursor.fetchone() #ชื่อผู้ใช้มีอยู่ไม่ให้ซ้ำ
            if row !=None:
                 messagebox.showerror('Error','UserID Already exists')
            else:
                query='insert into data(email,userid,password) values(%s,%s,%s)'
                mycursor.execute(query,(Email_SignUp.get(),User_SignUp.get(),PassWord_SignUp.get()))
                con.commit()
                con.close()
                #clear() #function ที่ทำให้ข้อมูลในช่องหายหลังจากกดปุ่ม
                root_signup.withdraw()
                root_signup_page_2()
        
    def login_page():
        root_signup.destroy()
        

    def enter_data():#เก็บข้อมูลลง Excel #ตอนนี้ไม่ได้ใช้อันนี้ ใช้ connect_database เก็บลงใน MySQL แทน
        #user info
        Email = Email_SignUp.get()
        UserID = User_SignUp.get()
        Password = PassWord_SignUp.get()
        confirmPassword = PassWordConfirm_SignUp.get()
        
        #filepath
        filepath = r"C:\Users\admin\Documents\Project ปี4\GUI\data_signup_Handhygein.xlsx"

        if not os.path.exists(filepath):
            worksheet = openpyxl.Workbook()
            sheet = worksheet.active
            heading = ["Email","User ID","Password","Confirm Password"]
            sheet.append(heading)
            worksheet.save(filepath)
        worksheet=openpyxl.load_workbook(filepath)
        sheet = worksheet.active
        sheet.append([Email,UserID,Password,confirmPassword])
        worksheet.save(filepath)

    root_signup = Toplevel() #Toplevel เป็นเครื่องมือที่ช่วยในการทำงาน ที่มีการสร้างหน้าต่างโต้ตอบ แต่การทำงานจะทำงานจะออกมาแยกหน้าต่างกัน สามารถทำงานรันทีนึงแสดงออกมาหลายหน้าต่าง
    root_signup.title('SignUp Page')
    root_signup.geometry('925x500+300+200')
    root_signup.configure(bg='#fff')
    root_signup.resizable(False,False) #False,False คือ ไม่ให้ปรับขยายหน้าจอ

    
    Label(root_signup,image=img,bg='white').place(x=125,y=50)

    
    Label(root_signup,image=logohos,bg='white').place(x=50,y=400)

   
    Label(root_signup,image=logotu,bg='white').place(x=455,y=410)

    
    Label(root_signup,image=logotse,bg='white').place(x=550,y=400)

    frame=Frame(root_signup,width=350,height=400,bg='#FFFFFF')#สร้างกรอบภายใน geometry ที่ตั้ง (ตั้งสีที่มองเห็นชัดก่อนตอนแรกค่อยเปลี่ยน)
    frame.place(x=480,y=10) 

    heading1=Label(root_signup,text='CREATE AN ACCOUNT',fg='#363636',bg='white',font=('Oswald',30,'bold')) #คำและoptionใน frame
    heading1.place(x=481,y=0)

    #Email for Login_SignUp
    def on_enter(e):
        Email_SignUp.delete(0,'end')
    def on_leave(e):
        name=Email_SignUp.get()
        if name == '':
            Email_SignUp.insert(0,'Email')
    Email_heading=Label(frame,text='Email',fg='black',bg='White',font=('Jasmine UPC',11,'bold'))
    Email_heading.place(x=47,y=60)
    Email_SignUp = Entry(frame,width=25,border=0,bg='white',font=('Ubuntu',11),fg='#4F4F4F')
    Email_SignUp.place(x=60,y=85)
    Email_SignUp.insert(0,'Email')
    Email_SignUp.bind('<FocusIn>',on_enter)
    Email_SignUp.bind('<FocusOut>',on_leave)


    Frame(frame,width=245,height=2,bg='#4F4F4F').place(x=60,y=110)

    #USER ID for Login_SignUp
    def on_enter(e):
        User_SignUp.delete(0,'end')
    def on_leave(e):
        name=User_SignUp.get()
        if name == '':
            User_SignUp.insert(0,'User ID')
    User_heading=Label(frame,text='User ID',fg='black',bg='White',font=('Jasmine UPC',11,'bold'))
    User_heading.place(x=47,y=120)
    User_SignUp = Entry(frame,width=25,border=0,bg='white',font=('Ubuntu',11),fg='#4F4F4F')
    User_SignUp.place(x=60,y=145)
    User_SignUp.insert(0,'User ID')
    User_SignUp.bind('<FocusIn>',on_enter)
    User_SignUp.bind('<FocusOut>',on_leave)

    Frame(frame,width=245,height=2,bg='#4F4F4F').place(x=60,y=170)

    #PassWord_SignUp
    def on_enter(e):
        PassWord_SignUp.delete(0,'end')
    def on_leave(e):
        name=PassWord_SignUp.get()
        if name == '':
            PassWord_SignUp.insert(0,'Password')
    PassWord_Heading=Label(frame,text='Password',fg='Black',bg='White',font=('Jasmine UPC',11,'bold'))
    PassWord_Heading.place(x=47,y=180)
    PassWord_SignUp = Entry(frame,width=25,fg='#4F4F4F',border=0,font= ('Ubantu',11),bg='white')
    PassWord_SignUp.place(x=60,y=205)
    PassWord_SignUp.insert(0,'Password')
    PassWord_SignUp.bind('<FocusIn>',on_enter)
    PassWord_SignUp.bind('<FocusOut>',on_leave)

    Frame(frame,width=245,height=2,bg='#4F4F4F').place(x=60,y=230)


    #Password_Confirm
    def on_enter(e):
        PassWordConfirm_SignUp.delete(0,'end')
    def on_leave(e):
        name=PassWordConfirm_SignUp.get()
        if name == '':
            PassWordConfirm_SignUp.insert(0,'Confirm Password')
    PassWordConfirm_Heading=Label(frame,text='Confirm Password',fg='Black',bg='White',font=('Jasmine UPC',11,'bold'))
    PassWordConfirm_Heading.place(x=47,y=240)
    PassWordConfirm_SignUp = Entry(frame,width=25,fg='#4F4F4F',border=0,font= ('Ubantu',11),bg='white')
    PassWordConfirm_SignUp.place(x=60,y=265)
    PassWordConfirm_SignUp.insert(0,'Confirm Password')
    PassWordConfirm_SignUp.bind('<FocusIn>',on_enter)
    PassWordConfirm_SignUp.bind('<FocusOut>',on_leave) 

    Frame(frame,width=245,height=2,bg='#4F4F4F').place(x=60,y=290)


    #Button_SignUp
    Button_SignUp = Button(frame,border=0,width=30,bg='#CC0000',fg='White',text='Sign up',pady=7,command=connect_database)
    Button_SignUp.place(x=75,y=320) 

    #Login
    fogetpass = Button(frame,width=13,text='Forget Password ?',border=0,bg='white',cursor='hand2',fg='#1E90FF',command=forgetpassword)
    fogetpass.place(x=110,y=370)

    loginButton=Button(frame,text='Login',fg='#CC0000',bg='white',font=('Jasmine UPC',10,'bold'),border=0,command=login_page)
    loginButton.place(x=210,y=368)

    root_signup.transient(root) #transient เปลี่ยนหน้าต่างให้เป็นหน้าต่างชั่วคราว (ชั่วคราว) สำหรับหน้าต่างหลักที่กำหนดหรือหน้าต่างหลักของหน้าต่าง เมื่อไม่มีการให้อาร์กิวเมนต์
    root_signup.iconphoto(False, hostuicon,guiicon) 
    root_signup.mainloop()


def forgetpassword():
    def change_password():
        if UserID_forget_entry.get()=='' or Password_forget_entry.get()=='' or Confirmpass_forget_entry.get()=='':
            messagebox.showerror('Error','All Fileds Are Required',parent=root_forgetpass)
        elif Password_forget_entry.get() != Confirmpass_forget_entry.get():
            messagebox.showerror('Error','Password and Confirm Password are not matching')
        elif len(Password_forget_entry.get()) < 8:
            messagebox.showerror('Error','Password less than 8 characters')
        elif len(Confirmpass_forget_entry.get()) > 20:
            messagebox.showerror('Error','Password  must be than 20 characters') 
        else:
            con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00',database='userdata_3')
            mycursor=con.cursor()
            query = 'select * from data where userid=%s'
            mycursor.execute(query,(UserID_forget_entry.get()))
            row = mycursor.fetchone()
            if row==None:
                messagebox.showerror('Error','Incorrect UserID',parent=root_forgetpass)
            else:
                query = 'update data set password=%s where userid=%s'
                mycursor.execute(query,(Password_forget_entry.get(),UserID_forget_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success','Password is reset , please login with new password',parent=root_forgetpass)
                root_forgetpass.destroy()
    def cancel_forgetpassword():
        root_forgetpass.destroy()

    root_forgetpass = Toplevel()
    root_forgetpass.title('Change Password')
    root_forgetpass.geometry('700x500+400+200')
    root_forgetpass.configure(bg='#6699FF')
    root.resizable(False,False)

    frame_forget = Frame(root_forgetpass,width=340,height=450,bg='white',highlightthickness=5)
    frame_forget.place(x=180,y=20)
    imgkey = PhotoImage(file='key_100x100.png')
    Label(frame_forget,bg='white',image=imgkey).place(x=120,y=10)

    heading_resetpass = Label(frame_forget,text='Reset Password',bg='white',font=('Ubuntu',26,'bold'),fg='#708090')
    heading_resetpass.place(x=35,y=125)
    
    heading_UserID_forget = Label(frame_forget,text='User ID',font=('Jasmine UPC',10,'bold'),bg='white')
    heading_UserID_forget.place(x=70,y=185)
    UserID_forget_entry = Entry(frame_forget,width=30,bg='white',border=2)
    UserID_forget_entry.place(x=72.5,y=210)

    heading_Password_forget = Label(frame_forget,text='New Password',font=('Jasmine UPC',10,'bold'),bg='white')
    heading_Password_forget.place(x=70,y=245)
    Password_forget_entry = Entry(frame_forget,width=30,bg='white',border=2)
    Password_forget_entry.place(x=72.5,y=270)

    heading_Confirmpass_forget = Label(frame_forget,text='Confirm New Password',font=('Jasmine UPC',10,'bold'),bg='white')
    heading_Confirmpass_forget.place(x=70,y=305)
    Confirmpass_forget_entry = Entry(frame_forget,width=30,bg='white',border=2)
    Confirmpass_forget_entry.place(x=72.5,y=330)

    UserID_forget_button = Button(frame_forget,width=25,bg='#708090',text='Enter',border=0,fg='white',pady=3,command=change_password)
    UserID_forget_button.place(x=73,y=375)

    cancel_forget_button = Button(frame_forget,width=6,text='Cancel',bg='white',border=0,fg='red',command=cancel_forgetpassword)
    cancel_forget_button.place(x=140,y=410)

    root_forgetpass.iconphoto(False, hostuicon,guiicon) 
    root_forgetpass.transient(root)
    root_forgetpass.mainloop()

def login_user():

    
    def afterlogin_editprofile():

        def after_start_test():

            root_editprofile.deiconify()

            try:
                con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                mycursor=con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                return
        
            try:
                query='use test1'
                mycursor.execute(query)
            except:
                mycursor.execute('use test1')
        
            query=f'select * from data where {dtb_combobox.get()}'  
            mycursor.execute(query)
            query="UPDATE data SET score = %s , result = %s  WHERE id = %s"
            mycursor.execute(query,())
            con.commit()
            con.close()
            refreshTable()

        def start_test():

            class Test:
                def __init__(self, port='COM3', baudrate=9600):
                    self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=1)
                    self.filename = None
                    self.frame_per_second = 30.0
                    self.res = None
                    self.STD_DIMENSIONS = {
                        "480p": (640, 480),
                        "720p": (1280, 720),
                        "1080p": (1920, 1080),
                        "4k": (3840, 2160),
                    }
                    self.VIDEO_TYPE = {
                        'avi': cv2.VideoWriter_fourcc(*'XVID'),
                        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
                    }
                    self.out = None
                    self.handmp = mp.solutions.hands
                    self.hands = None
                    self.Fg_thresh = 115
                    self.LightCondition = 0
                    self.max_area_left_LED = 0
                    self.max_area_right_LED = 0
                    self.max_area_left_UV = 0
                    self.max_area_right_UV = 0
                    self.stop_camera = False  # Variable to control camera loop

                def Name(self, filename, frame_per_second, res):
                    self.filename = filename
                    self.frame_per_second = frame_per_second
                    self.res = res

                def change_res(self, cap, width, height):
                    cap.set(3, width)
                    cap.set(4, height)

                def get_dims(self, cap, res='1080p'):
                    width, height = self.STD_DIMENSIONS["720p"]
                    if res in self.STD_DIMENSIONS:
                        width, height = self.STD_DIMENSIONS[res]
                    self.change_res(cap, width, height)
                    return width, height

                def get_video_type(self, filename):
                    filename, ext = os.path.splitext(filename)
                    if ext in self.VIDEO_TYPE:
                        return self.VIDEO_TYPE[ext]
                    return self.VIDEO_TYPE['avi']

                def send_command(self, command):
                    self.arduino.write(bytes(command, 'utf-8'))
                    time.sleep(0.05)
                    return self.arduino.readline()

                def initialize_hand_detection(self):
                    self.hands = self.handmp.Hands(
                        static_image_mode=False, 
                        model_complexity=1, 
                        min_detection_confidence=0.75, 
                        min_tracking_confidence=0.75, 
                        max_num_hands=2
                    )

                def process_frame(self, frame):
                    frame = cv2.flip(frame, 1)
                    frame = cv2.line(frame, (640, 0), (640, 720), (0, 255, 0), 5)
                    ImageLAB = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
                    blur = cv2.GaussianBlur(ImageLAB[:, :, 0], (3, 3), 0)
                    _, Fg_thresh = cv2.threshold(blur, self.Fg_thresh, 255, cv2.THRESH_BINARY)
                    FgHand_contours, _ = cv2.findContours(Fg_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    for c in FgHand_contours:
                        area = cv2.contourArea(c)
                        M = cv2.moments(c)
                        if M["m00"] == 0:
                            continue
                        cx = M["m10"] / M["m00"]

                        if self.LightCondition == 0:
                            if cx < 640:
                                self.max_area_left_LED = max(self.max_area_left_LED, area)
                            else:
                                self.max_area_right_LED = max(self.max_area_right_LED, area)
                        elif self.LightCondition == 1:
                            if cx < 640:
                                self.max_area_left_UV = max(self.max_area_left_UV, area)
                            else:
                                self.max_area_right_UV = max(self.max_area_right_UV, area)

                        if len(c) > 200:
                            hull = cv2.convexHull(c)
                            Xbar = int(M["m10"] / M["m00"])
                            Ybar = int(M["m01"] / M["m00"])
                            cv2.circle(frame, (Xbar, Ybar), 5, (0, 0, 255), -1)
                            cv2.drawContours(frame, [c], -1, (0, 0, 255), 4)
                            cv2.drawContours(frame, [hull], -1, (0, 255, 0), 4)
                            cv2.putText(frame, f"Area: {area:.2f}", (Xbar, Ybar - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.hands.process(frame_rgb)
                    if results.multi_hand_landmarks:
                        for i, hand_handedness in enumerate(results.multi_handedness):
                            label = MessageToDict(hand_handedness)['classification'][0]['label']
                            pos = (45, 50) if label == 'Left' else (980, 50)
                            cv2.putText(frame, label + ' Hand', pos, cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

                    cv2.imshow('Foreground', frame)
                    cv2.setWindowProperty('Foreground', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                def camera1(self, cam):
                    self.cam = cv2.VideoCapture(cam)
                    width, height = self.get_dims(self.cam, self.res)
                    self.out = cv2.VideoWriter(self.filename, self.get_video_type(self.filename), self.frame_per_second, (width, height))
                    self.initialize_hand_detection()
                    while self.cam.isOpened() and not self.stop_camera:
                        ret, frame = self.cam.read()
                        self.out.write(frame)
                        if not ret:
                            break
                        self.process_frame(frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    self.cam.release()
                    self.out.release()
                    cv2.destroyAllWindows()

                def calculate_percentage_difference(self, area1, area2):
                    if area1 == 0 or area2 == 0:
                        return 0
                    return 100 - (abs(area1 - area2) / max(area1, area2) * 100)

                def compare_areas(self):
                    print(f"Max Area Left LED: {self.max_area_left_LED}")
                    print(f"Max Area Right LED: {self.max_area_right_LED}")
                    print(f"Max Area Left UV: {self.max_area_left_UV}")
                    print(f"Max Area Right UV: {self.max_area_right_UV}")

                    difference_left = self.calculate_percentage_difference(self.max_area_left_LED, self.max_area_left_UV)
                    difference_right = self.calculate_percentage_difference(self.max_area_right_LED, self.max_area_right_UV)

                    print(f"Percentage Difference Left: {difference_left:.2f}%")
                    print(f"Percentage Difference Right: {difference_right:.2f}%")

                def start_timer(self, minutes, seconds):
                    total_seconds = minutes * 60 + seconds
                    print(f"Timer was set to {minutes} min {seconds} sec")
                    start_time = time.time()
                    self.LightCondition = 0

                    while True:
                        elapsed_time = time.time() - start_time
                        time_left = max(total_seconds - elapsed_time, 0)
                        minutes_left = int(time_left // 60)
                        seconds_left = int(time_left % 60)
                        print(f"time 1 {minutes_left} min {seconds_left} sec", end="\r")

                        if elapsed_time >= total_seconds:
                            print(f"LightCondition{self.LightCondition}")
                            print(f"Max Area Left LED: {self.max_area_left_LED}")
                            print(f"Max Area Right LED: {self.max_area_right_LED}")
                            print("\nTimer ended")
                            self.stop_camera = True  # Stop the camera loop
                            break

                        if elapsed_time > 9:  # Send command after 9 seconds
                            response = self.send_command("a")
                            self.Fg_thresh = 115

                        time.sleep(1)

                def start_timer1(self, minutes, seconds):
                    total_seconds = minutes * 60 + seconds
                    print(f"Timer was set to {minutes} min {seconds} sec")
                    start_time = time.time()
                    self.LightCondition = 2

                    while True:
                        elapsed_time = time.time() - start_time
                        time_left = max(total_seconds - elapsed_time, 0)
                        minutes_left = int(time_left // 60)
                        seconds_left = int(time_left % 60)
                        print(f"time 2 {minutes_left} min {seconds_left} sec", end="\r")

                        if elapsed_time >= total_seconds:
                            print("\nTimer ended")
                            self.stop_camera = True  # Stop the camera loop
                            break

                        if elapsed_time >= 0.1:  # Send command after 1 second
                            response = self.send_command("c")
                            self.Fg_thresh = 250

                        time.sleep(1)

                def start_timer2(self, minutes, seconds):
                    total_seconds = minutes * 60 + seconds
                    print(f"Timer was set to {minutes} min {seconds} sec")
                    start_time = time.time()
                    self.LightCondition = 1

                    while True:
                        elapsed_time = time.time() - start_time
                        time_left = max(total_seconds - elapsed_time, 0)
                        minutes_left = int(time_left // 60)
                        seconds_left = int(time_left % 60)
                        print(f"time 3 {minutes_left} min {seconds_left} sec", end="\r")

                        if elapsed_time >= total_seconds:
                            print(f"LightCondition{self.LightCondition}")
                            print(f"Max Area Left UV: {self.max_area_left_UV}")
                            print(f"Max Area Right UV: {self.max_area_right_UV}")
                            print("\nTimer ended")
                            self.compare_areas()
                            self.stop_camera = True  # Stop the camera loop
                            break

                        if elapsed_time > 1:  # Send command after 1 second
                            response = self.send_command("b")
                            self.Fg_thresh = 20

                        time.sleep(1)

                def close(self):
                    self.arduino.close()

            if __name__ == '__main__':
                for i in range(2):  # Loop to repeat 2 rounds
                    tester = Test()
                    tester.Name("test.avi", 30, '720p')
                    camera_thread = threading.Thread(target=tester.camera1, args=(0,))
                    camera_thread.start()

                    tester.start_timer(0, 10)
                    tester.start_timer1(0, 1)
                    tester.start_timer2(0, 10)

                    # Ensure the camera thread has finished before starting the next round
                    camera_thread.join()

                    # Close the Arduino connection before starting the next round
                    tester.close()

        def update_frame():
            root_editprofile.update(lbl_show_pic)
            root_editprofile.update_idletasks(lbl_show_pic)

        def fetch_data():
            try:
                con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                mycursor=con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                return
        
            try:
                query='use userdata_3'
                mycursor.execute(query)
            except:
                mycursor.execute('use userdata_3')
        
            query='select image from data where userid=%s'  
            mycursor.execute(query,(user_entry.get()))
            image_bytes = mycursor.fetchone()[0]
            image = Image.open(io.BytesIO(image_bytes))
            image = image.resize((200, 200))
            photo_image = ImageTk.PhotoImage(image)
            
            query='select firstname from data where userid=%s'  
            mycursor.execute(query,(user_entry.get()))
            firstname_fetch = mycursor.fetchone()[0]

            con.commit()
            con.close()
            
            lbl_show_pic.config(image='')
            lbl_show_pic.config(image = photo_image)

            if firstname_fetch != None:
                fisrtname_entry.config(state='normal')
                fisrtname_entry.delete(0,END)
                fisrtname_entry.insert(0,firstname_fetch)
                fisrtname_entry.config(state='readonly')

            update_frame()

        def signup_page_2():
                
            def on_closing():
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                    root_signup_2.destroy()
                    edt1.config(state='active')  

            def conn_dtb_signuppage2():
                if nameuser.get() == '' or Lastname.get() == '' or radio.get()==' - Please select your gender - 'or date.cget("text")=='' or phonenum.get()=='' :
                    messagebox.showerror('Error','All fields Are Require')
                else:
                    try:
                        con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                        mycursor=con.cursor()
                    except:
                        messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                        return
                
                    try:
                        query='use userdata_3'
                        mycursor.execute(query)
                    except:
                        mycursor.execute('use userdata_3')
                
                    query='select * from data where userid=%s'  
                    mycursor.execute(query,(user_entry.get()))
                    query="UPDATE data SET firstname = %s , lastname = %s , gender =%s ,dateofbirth=%s, phone =%s  WHERE userid = %s"
                    mycursor.execute(query,(nameuser.get(),Lastname.get(),radio.get(),date.cget("text"),phonenum.get(),user_entry.get()))
    
                    con.commit()
                    con.close()
                    messagebox.showinfo('Success','Edit profile is successful') 
                    root_signup_2.destroy()
                    edt1.config(state='active')      
                    fetch_data()           
                    

            #def selectPic(): #ใช้ from tkinter import filedialog (ใช้สำหรับการดาวน์โหลดรูปภาพจากไฟล์ภายในเครื่อง)
                #global imgselect
                #filename = filedialog.askopenfilename(initialdir="/images",title='Select Image',filetypes=(('jpg images','*.jpg'),('png images','*.png')))
                #imgselect = Image.open(filename)
                #imgselect = imgselect.resize((200,200), Image.LANCZOS) #ANTIALIAS เลิกใช้งานแล้วและจะถูกนำออกใน Pillow 10  ใช้ LANCZOS หรือ Resampling.LANCZOS แทน
                #imgselect = ImageTk.PhotoImage(imgselect) 
                #lbl_show_pic['image'] = imgselect 
                #entry_pic_path.insert(0,filename) 
                
                #def convert_to_binary(img):
                    #with open(img,'rb') as file:
                        #bd = file.read()
                    #return bd 

                #try:
                    #con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                    #mycursor=con.cursor()
                #except:
                    #messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                    #return
            
                #try:
                    #query='use userdata_3'
                    #mycursor.execute(query)
                #except:
                    #mycursor.execute('use userdata_3')

                #query='select * from data where userid=%s'  
                #mycursor.execute(query,(user_entry.get()))
                #query="UPDATE data SET media_name = %s , image = %s WHERE userid = %s"
                #pic = convert_to_binary(filename)
                #mycursor.execute(query,(entry_pic_path.get(),pic,user_entry.get()))
                #con.commit()
                #con.close()
            
            def selectPic():
                global imgselect
                filename = filedialog.askopenfilename(initialdir="/images", title='Select Image', filetypes=(('jpg images', '*.jpg'), ('png images', '*.png')))
                if filename:
                    try:
                        imgselect = Image.open(filename)
                        imgselect = imgselect.resize((200, 200), Image.LANCZOS)  # ANTIALIAS เลิกใช้งานแล้วและจะถูกนำออกใน Pillow 10  ใช้ LANCZOS หรือ Resampling.LANCZOS แทน
                        imgselect = ImageTk.PhotoImage(imgselect)
                        lbl_show_pic['image'] = imgselect
                        entry_pic_path.insert(0, filename)
                        
                        def convert_to_binary(img):
                            with open(img, 'rb') as file:
                                bd = file.read()
                            return bd 
                        
                        try:
                            con = pymysql.connect(host='localhost', user='root', password='Jamesanddef00')
                            mycursor = con.cursor()
                        except:
                            messagebox.showerror('Error', 'Database Connectivity Issue, Please Try Again')
                            return
                        
                        try:
                            query = 'use userdata_3'
                            mycursor.execute(query)
                        except:
                            mycursor.execute('use userdata_3')

                        query = 'select * from data where userid=%s'
                        mycursor.execute(query, (user_entry.get(),))
                        row = mycursor.fetchone()  # ดึงข้อมูลเดิมของผู้ใช้
                        if row:
                            query = "UPDATE data SET media_name = %s , image = %s WHERE userid = %s"
                            pic = convert_to_binary(filename)
                            mycursor.execute(query, (entry_pic_path.get(), pic, user_entry.get()))
                            con.commit()
                        else:
                            pass
                        con.commit()
                        con.close()
                    except Exception as e:
                        messagebox.showerror('Error', str(e))

            edt1.config(state='disabled')
            root_signup_2 = Toplevel(root_editprofile) 
            root_signup_2.resizable(False,False) 
            root_signup_2.configure(bg='#fff') 
            root_signup_2.title('Signup Profile') 
            root_signup_2.geometry('925x500+300+200') 

            bg_sgup2=Image.open('bg_medical7.jpg')
            bg_sgup2=ImageTk.PhotoImage(bg_sgup2) 
            canvas=Canvas(root_signup_2,width=925,height=500) #canvas = ใช้วาดรูปบนหน้าจอ 
            canvas.create_image(0,0,image=bg_sgup2,anchor=CENTER)
            canvas.pack(fill=tk.BOTH, expand=True)

            frame_signuppage_2 = Frame(root_signup_2,width=350,height=400,bg='#F5F5F5')
            frame_signuppage_2.place(x=500,y=30)

            #part nameuser editprofile in main test

            nameuser_heading = Label(frame_signuppage_2,text='First Name:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
            nameuser_heading.place(x=20,y=35) 
            nameuser = Entry(frame_signuppage_2,width=20,bg='white',border=2,font=('Jasmine UPC',10))
            nameuser.place(x=150,y=35) 

            try:
                con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                mycursor=con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                return
        
            try:
                query='use userdata_3'
                mycursor.execute(query)
            except:
                mycursor.execute('use userdata_3')
        
            query = 'select firstname from data where userid=%s'
            mycursor.execute(query,(user_entry.get()))
            firstname_sql = mycursor.fetchone()[0]
            if firstname_sql != None:
                nameuser.insert(0,firstname_sql)


            #part Lastname user editprofile in main test

            Lastname_heading = Label(frame_signuppage_2,text='Last Name:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
            Lastname_heading.place(x=20,y=85)
            Lastname = Entry(frame_signuppage_2,width=20,bg='white',border=2,font=('Jasmine UPC',10))
            Lastname.place(x=150,y=85)

            try:
                con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                mycursor=con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                return
        
            try:
                query='use userdata_3'
                mycursor.execute(query)
            except:
                mycursor.execute('use userdata_3')
        
            query = 'select lastname from data where userid=%s'
            mycursor.execute(query,(user_entry.get()))
            lastname_sql = mycursor.fetchone()[0]
            if lastname_sql != None:
                Lastname.insert(0,lastname_sql)

            #part gender user editprofile in main test

            Gender_heading = Label(frame_signuppage_2,text='Gender:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
            Gender_heading.place(x=20,y=135)
            radio = StringVar()
            gender_combobox = ttk.Combobox(frame_signuppage_2,values=(' - Please select your gender - ','Male','Female','Lgbtq+','Not specified'),state='readonly',width=25,cursor='hand2',textvariable=radio)
            gender_combobox.current(0)
            gender_combobox.place(x=120,y=135)

            try:
                con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                mycursor=con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                return
        
            try:
                query='use userdata_3'
                mycursor.execute(query)
            except:
                mycursor.execute('use userdata_3')
        
            query = 'select gender from data where userid=%s'
            mycursor.execute(query,(user_entry.get()))
            gender_sql = mycursor.fetchone()[0]
            if gender_sql != None:
                gender_combobox.config(state='normal')
                gender_combobox.delete(0,END)
                gender_combobox.insert(0,gender_sql)
                gender_combobox.config(state='readonly')

            #part phone user editprofile in main test

            phone_heading = Label(frame_signuppage_2,text='Phone number:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
            phone_heading.place(x=20,y=235)
            phonenum = Entry(frame_signuppage_2,width=20,bg='white',border=2,font=('Jasmine UPC',10))
            phonenum.place(x=150,y=235)

            try:
                con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                mycursor=con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                return
        
            try:
                query='use userdata_3'
                mycursor.execute(query)
            except:
                mycursor.execute('use userdata_3')
        
            query = 'select phone from data where userid=%s'
            mycursor.execute(query,(user_entry.get()))
            phone_sql = mycursor.fetchone()[0]
            if phone_sql != None:
                phonenum.insert(0,phone_sql)


            #part dateofbirth user editprofile in main test

            daybirth_heading = Label(frame_signuppage_2,text='Day of birth:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',11,'bold'))
            daybirth_heading.place(x=20,y=185)
            
            def birthcalendar():
                root_bd = Toplevel(root_signup_2)
                root_bd.title('Birth Calendar')
                root_bd.geometry('250x220+850+450')
                root_bd.resizable(False,False)
                birthcal = Calendar(root_bd, selectmode = 'day',firstweekday='sunday',date_pattern ='dd/mm/y')
                birthcal.place(x=0,y=0)

                def grad_date():
                    selected_date = birthcal.get_date()
                    date.config(text=selected_date)
                    if date != '':
                        root_bd.destroy()

                bdbutton = Button(root_bd, text = "Enter Date",command = grad_date)
                bdbutton.place(x=90,y=190)
            
            date = Label(frame_signuppage_2, text ='',width=20,bg='white')
            date.pack()
            date.place(x=134,y=185)
            bf_btn = Button(frame_signuppage_2,text='V',bg='white',fg='black',command=birthcalendar,font=('Jasmine UPC',7),border=1,cursor='hand2')
            bf_btn.place(x=280,y=185)

            try:
                con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
                mycursor=con.cursor()
            except:
                messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
                return
        
            try:
                query='use userdata_3'
                mycursor.execute(query)
            except:
                mycursor.execute('use userdata_3')
        
            query = 'select dateofbirth from data where userid=%s'
            mycursor.execute(query,(user_entry.get()))
            dateofbirth_sql = mycursor.fetchone()[0]
            if dateofbirth_sql != None:
                date.config(text=dateofbirth_sql)

            #part upload picProfile
            imgprofile = PhotoImage(file='Profile (1).png')
            frame_profile_signup_2 = Frame(root_signup_2,width=350,height=400,bg='#F5F5F5')
            frame_profile_signup_2.place(x=100,y=30)
            lbl_show_pic = Label(frame_profile_signup_2,bg='#F0FFFF',highlightthickness=3,image='')
            if image_bytes != None:
                lbl_show_pic.config(image=photo_image)
            else:
                lbl_show_pic.config(image=imgprofile)
            lbl_show_pic.place(x=72,y=20)
            ImagePath = Label(frame_profile_signup_2,text='Image Path:',bg='#F5F5F5',fg='black',font=('Jasmine UPC',9,'bold'))
            ImagePath.place(x=5,y=260)
            entry_pic_path = Entry(frame_profile_signup_2,font=('Jasmine UPC',9),width=25)
            entry_pic_path.place(x=87,y=260)
            btn_browse = Button(frame_profile_signup_2,font=('Jasmine UPC',8),width=10,border=1,pady=2,text='Select Image',bg='white',command=selectPic,cursor='hand2')
            btn_browse.place(x=135,y=300)

            button_signuppage_2 = Button(frame_signuppage_2,width=25,border=0,bg='#63B8FF',text='Enter',pady=6,command=conn_dtb_signuppage2,cursor='hand2')
            button_signuppage_2.place(x=85,y=320)
                
            root_signup_2.transient(root_editprofile)
            root_signup_2.iconphoto(False, hostuicon)
            root_signup_2.protocol("WM_DELETE_WINDOW", on_closing)
            root_signup_2.mainloop()

        def validate_inputt(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
            # ตรวจสอบว่าข้อความใหม่เป็นตัวอักษรพิมพ์เล็กภาษาอังกฤษ หรือตัวเลข หรือเครื่องหมาย underscore (_) เท่านั้น
            if text.islower() or text.isdigit() or text == "_" or text == "":
                return True
            else:
                return False
        def check_table_exists(table_name, db_url):
            try:
                # สร้างการเชื่อมต่อกับ MySQL
                engine = create_engine(f"mysql+pymysql://{db_url['user']}:{db_url['password']}@{db_url['host']}:{db_url['port']}/{db_url['database']}")
                inspector = inspect(engine)
                return table_name in inspector.get_table_names()
            except Exception as e:
                print(f"An error occurred: {e}")
                return False

        def import_excel_to_db(excel_file, sheet_name, db_url, table_name):
            try:
                # อ่านข้อมูลจากไฟล์ Excel
                df = pd.read_excel(excel_file, sheet_name=sheet_name)

                # ตรวจสอบว่ามีข้อมูลในไฟล์ Excel หรือไม่
                if df.empty:
                    messagebox.showwarning("Empty File", "The selected Excel file is empty.")
                    return

                # ลบช่องว่างข้างหน้าและข้างหลังจากชื่อคอลัมน์
                df.columns = df.columns.str.strip()

                # ตรวจสอบจำนวนแถวและคอลัมน์
                num_rows, num_cols = df.shape

                # ตรวจสอบจำนวนคอลัมน์
                if num_cols != 8:
                    messagebox.showerror("Invalid Columns", f"The selected Excel file contains {num_cols} columns. Please select a file with exactly 8 columns.")
                    return

                # ตรวจสอบข้อมูลในแถวแรก
                expected_data = ["id", "name", "lastname", "department", "type_wash", "score", "result", "date_test"]
                first_row = df.columns.tolist()  # ใช้ชื่อคอลัมน์แทนแถวแรก 

                # ลบช่องว่างข้างหน้าและข้างหลังจากข้อมูลในแถวแรก
                first_row = [str(item).strip() for item in first_row]

                if first_row != expected_data:
                    messagebox.showerror("Invalid Data", "The data in the first row does not match the expected values.")
                    return

                # แปลงค่าว่างหรือ None เป็น NULL
                df = df.applymap(lambda x: None if pd.isna(x) or x == 'None' else x)

                # สร้างการเชื่อมต่อกับฐานข้อมูล
                engine = create_engine(f"mysql+pymysql://{db_url['user']}:{db_url['password']}@{db_url['host']}:{db_url['port']}/{db_url['database']}")

                # นำข้อมูลเข้าไปในตารางในฐานข้อมูล
                df.to_sql(table_name, con=engine, if_exists='replace', index=False)

                print(f'Data imported successfully into table {table_name}')
                messagebox.showinfo("Success", f"Data imported successfully into table {table_name}")
                current_values = set_dtbname_combobox['values']
                updated_values = list(current_values)  # สร้างรายการใหม่เพื่อประกอบด้วยรายการเดิมและรายการใหม่
                updated_values.append(table_name)
                set_dtbname_combobox['values'] = updated_values
                set_dtbname_entry.delete(0, tk.END)
            except Exception as e:
                print(f"An error occurred: {e}")
                messagebox.showerror("Error", f"An error occurred: {e}")

        def select_file():
            file_path = filedialog.askopenfilename(
                title="Select Excel File",
                filetypes=(("Excel files", "*.xlsx *.xls"), ("All files", "*.*"))
            )
            
            if file_path:
                # ตรวจสอบว่าเป็นไฟล์ Excel หรือไม่
                if not file_path.endswith(('.xls', '.xlsx')):
                    messagebox.showerror("Invalid File", "Please select a valid Excel file.")
                    return

                db_url = {
                    'host': 'localhost',
                    'user': 'root',  # เปลี่ยนเป็น username ที่ถูกต้อง
                    'password': 'Jamesanddef00',  # เปลี่ยนเป็น password ที่ถูกต้อง
                    'port': 3306,
                    'database': 'test1'
                }
                
                # ขอให้ผู้ใช้กรอกชื่อ Sheet
                sheet_name = ask_for_input("Sheet Name", "Enter the name of the sheet:", root_editprofile)
                
                if not sheet_name:
                    messagebox.showwarning("Input Error", "Sheet name cannot be empty.")
                    return

                # ขอให้ผู้ใช้กรอกชื่อตาราง
                table_name = ask_for_input("Table Name", "Enter the name of the table: \n(lowercase English letters only)", root_editprofile, validate=True)
                
                if not table_name:
                    messagebox.showwarning("Input Error", "Table name cannot be empty.")
                    return

                # ตรวจสอบว่าชื่อตารางมีอยู่แล้วหรือไม่
                if check_table_exists(table_name, db_url):
                    messagebox.showwarning("Table Exists", f"The table '{table_name}' already exists in the database.")
                    return

                import_excel_to_db(file_path, sheet_name, db_url, table_name)

        def ask_for_input(title, prompt, root_editprofile, validate=False):
            input_dialog = tk.Toplevel(root_editprofile)
            input_dialog.title(title)
            input_dialog.lift()
            input_dialog.attributes('-topmost', True)
            
            # คำนวณตำแหน่งที่ตั้งที่เหมาะสมเพื่อตั้งค่า geometry ของหน้าต่าง
            window_width = 300
            window_height = 130
            screen_width = input_dialog.winfo_screenwidth()
            screen_height = input_dialog.winfo_screenheight()
            position_top = int(screen_height / 2 - window_height / 2)
            position_right = int(screen_width / 2 - window_width / 2)
            input_dialog.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

            tk.Label(input_dialog, text=prompt).pack(pady=10)
            user_input = tk.StringVar()
            
            if validate:
                vcmd = (input_dialog.register(validate_inputt), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
                input_entry = tk.Entry(input_dialog, textvariable=user_input, validate="key", validatecommand=vcmd)
            else:
                input_entry = tk.Entry(input_dialog, textvariable=user_input)
            
            input_entry.pack(pady=5)
            
            def on_submit():
                input_dialog.destroy()

            submit_button = tk.Button(input_dialog, text="Submit", command=on_submit)
            submit_button.pack(pady=10)
            
            input_entry.focus_set()
            input_dialog.transient(root_editprofile)
            input_dialog.grab_set()
            
            input_dialog.after(0, lambda: input_dialog.attributes('-topmost', True))
            input_dialog.after(1000, lambda: input_dialog.attributes('-topmost', False))

            root_editprofile.wait_window(input_dialog)
            
            return user_input.get()
                
        def setph(word,num):
            for ph in range(0,8):
                if ph == num:
                    placeholderArray[ph].set(word)
        def save():

            name = name_entry.get().strip()  
            lastname = lastname_entry.get().strip()
            no = no_entry.get().strip()

            if not all([name, lastname,no]):
                messagebox.showerror("Error", "Name or Lasname or No. fields Are Require")
                return
            if dtb_combobox.get() == '':
                messagebox.showerror("Error", "Please select Database before")
                return
            try:
            
                con = pymysql.connect(host='localhost', user='root', password='Jamesanddef00')
                mycursor = con.cursor()
                mycursor.execute(f'use test1')
                insert_query = f'insert into {dtb_combobox.get()}(name, lastname, department, type_wash, score, result, date_test) values(%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(insert_query, (name, lastname, department_entry.get(), type_wash_entry.get(), score_entry.get(), result_combobox.get(), date_test_entry.get()))
                con.commit()

            except pymysql.err.ProgrammingError as err:
                messagebox.showerror("Error", f"ข้อผิดพลาดฐานข้อมูล (การเขียนโปรแกรม): {str(err)}")
                print(err) 

            except pymysql.err.OperationalError as err:
                messagebox.showerror("Error", f"ข้อผิดพลาดการเชื่อมต่อฐานข้อมูล: {str(err)}")
                print(err)  

            except Exception as err:
                messagebox.showerror("Error", f"เกิดข้อผิดพลาดที่ไม่คาดคิดขึ้น: {str(err)}")
                print(err)  

            finally:
                if con:
                    con.close()

            refreshTable()

        def update():
            table = dtb_combobox.get()
            selectedItemId = ''
            try:
                selectedItem = treeview.selection()[0]
                selectedItemId = str(treeview.item(selectedItem)['values'][0])
            except:
                messagebox.showwarning("", "Please select a data row")
            print(selectedItemId)
            no = str(no_entry.get())
            name = str(name_entry.get())
            lastname = str(lastname_entry.get())
            department = str(department_entry.get())
            type_wash = str(type_wash_entry.get())
            score = str(score_entry.get())
            result_test = str(result_combobox.get()) 
            date_test = str(date_test_entry.get())
            if not(no and no.strip()) or not(name and name.strip()) or not(lastname and lastname.strip()) :
                messagebox.showwarning("","Please fill up all entries")
                return
            if(selectedItemId!=no):
                messagebox.showwarning("","You can't change Item ID")
                return
            try:
                cursor.connection.ping()
                sql=f"UPDATE {table} SET `name` = '{name}', `lastname` = '{lastname}', `department` = '{department}', `type_wash` = '{type_wash}', `score` = '{score}', `result` = '{result_test}', `date_test` = '{date_test}' WHERE `id` = '{no}' "
                cursor.execute(sql)
                conn.commit()
                conn.close()
                for num in range(0,8):
                    setph('',(num))
            except Exception as err:
                messagebox.showwarning("","Error occured ref: "+str(err))
                return
            refreshTable()

        def select():
            try:
                selectedItem = treeview.selection()[0]
                no = str(treeview.item(selectedItem)['values'][0])
                name = str(treeview.item(selectedItem)['values'][1])
                lastname = str(treeview.item(selectedItem)['values'][2])
                department = str(treeview.item(selectedItem)['values'][3])
                type_wash = str(treeview.item(selectedItem)['values'][4])
                score = str(treeview.item(selectedItem)['values'][5])
                resultt = str(treeview.item(selectedItem)['values'][6])
                date_test = str(treeview.item(selectedItem)['values'][7])
                setph(no,0)
                setph(name,1)
                setph(lastname,2)
                setph(department,3)
                setph(type_wash,4)
                setph(score,5)
                setph(resultt,6)
                setph(date_test,7)
            except:
                messagebox.showwarning("", "Please select a data row")

        def delete():
            table = dtb_combobox.get()
            try:
                if(treeview.selection()[0]):
                    decision = messagebox.askquestion("", "Delete the selected data?")
                    if(decision != 'yes'):
                        return
                    else:
                        selectedItem = treeview.selection()[0]
                        itemId = str(treeview.item(selectedItem)['values'][0])
                        try:
                            cursor.connection.ping()
                            sql=f"DELETE FROM {table} WHERE `id` = '{itemId}' "
                            cursor.execute(sql)
                            conn.commit()
                            conn.close()
                            messagebox.showinfo("","Data has been successfully deleted")
                        except:
                            messagebox.showinfo("","Sorry, an error occured")
                        refreshTable()
            except:
                messagebox.showwarning("", "Please select a data row")

        def find():
            no = str(no_entry.get())
            name = str(name_entry.get())
            lastname = str(lastname_entry.get())
            department = str(department_entry.get())
            type_wash = str(type_wash_entry.get())
            score = str(score_entry.get())
            result_combb = str(result_combobox.get())
            datetest = str(date_test_entry.get())
            
            cursor.connection.ping()
            
            base_sql = f'SELECT id, name, lastname, department, type_wash, score, result, date_test FROM {dtb_combobox.get()} WHERE'
            
            conditions = []
            params = []

            # สร้างเงื่อนไขการค้นหาตามค่าที่ป้อนในแต่ละฟิลด์
            if no and no.strip():
                conditions.append("id LIKE %s")
                params.append(f"%{no}%")
            if name and name.strip():
                conditions.append("name LIKE %s")
                params.append(f"%{name}%")
            if lastname and lastname.strip():
                conditions.append("lastname LIKE %s")
                params.append(f"%{lastname}%")
            if department and department.strip():
                conditions.append("department LIKE %s")
                params.append(f"%{department}%")
            if type_wash and type_wash.strip():
                conditions.append("type_wash LIKE %s")
                params.append(f"%{type_wash}%")
            if score and score.strip():
                conditions.append("score LIKE %s")
                params.append(f"%{score}%")
            if result_combb and result_combb.strip():
                conditions.append("result LIKE %s")
                params.append(f"%{result_combb}%")
            if datetest and datetest.strip():
                conditions.append("date_test LIKE %s")
                params.append(f"%{datetest}%")
            
            if not conditions:
                messagebox.showwarning("", "Please fill up one of the entries")
                return
            
            sql = f"{base_sql} {' AND '.join(conditions)}"

            try:
                cursor.execute(sql, params)
                resultt = cursor.fetchall()
                if resultt:
                    for num in range(0, 7):
                        setph(resultt[0][num], num)
                    conn.commit()
                else:
                    messagebox.showwarning("", "No data found")
            except Exception as e:
                messagebox.showwarning("", str(e))
            finally:
                cursor.close()
                conn.close()

        def clear():
            for num in range(0,8):
                setph('',(num))

        def exportExcel():
            if show_dtbname_label['text'] == '':
                messagebox.showerror('Error','Please select your database')
                return
            else:
                table = dtb_combobox.get()
                cursor.connection.ping()
                sql = f"SELECT `id`, `name`, `lastname`, `department`, `type_wash`, `score`, `result`, `date_test` FROM {table}"
                cursor.execute(sql)
                dataraw = cursor.fetchall()

                # สร้าง DataFrame จากข้อมูลที่ดึงมาจากฐานข้อมูล
                df = pd.DataFrame(dataraw, columns=["id", "name", "lastname", "department", "type_wash", "score", "result", "date_test"])

                # ให้ผู้ใช้เลือกตำแหน่งและตั้งชื่อไฟล์
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("Excel files", "*.xls")])
                if not file_path:
                    return  # ถ้าผู้ใช้ยกเลิกการเลือกตำแหน่ง ไม่ต้องทำอะไรเพิ่มเติม
                
                # สร้างไฟล์ Excel
                df.to_excel(file_path, index=False)

                conn.commit()
                conn.close()
                messagebox.showinfo("", "Excel file downloaded")

        def destroy_profile():
            result = messagebox.askokcancel("Quit", "Do you want to quit?")
            if result:
                root_editprofile.destroy()
                user_entry.delete(0,END)
                password_entry.delete(0,END)
                root.deiconify() # deiconify คำสั่งแสดงหน้าต่างกลับมาอีกครั้งหลังจาก withdraw
            else:
                pass

        root_editprofile = Toplevel(root) 
        root_editprofile.title('Hand Hygeine Testing Profile - TUH')
        root_editprofile.resizable(True,True)
        root_editprofile.attributes('-fullscreen',True) #full screen แบบเต็มจริงไม่มีขอบไม่มีปุ่มปิดด้วย
        #width= root_editprofile.winfo_screenwidth()  # 1             
        #height= root_editprofile.winfo_screenheight()     #2          
        #root_editprofile.geometry("%dx%d" % (width, height))   #3 full screen แบบ เหมือนขยายจากหน้าจอเล็กไปใหญ่เฉยๆ มีขอบ
        #root_editprofile.state('zoomed') #full screen แบบดีสุด
        root_editprofile.configure(bg='#fff')
        #frame_aft_ed1 = Frame(root_editprofile,width=300,height=root_editprofile.winfo_screenwidth(),bg='#79cdcd').place(x=0,y=0)
        #frame_aft_ed2 = Frame(root_editprofile,bg='#79cdcd',width=root_editprofile.winfo_screenwidth(),height=70).place(x=0,y=0) #ตรง width คือทำให้กว้างสุดขอบจอ
        style = ttk.Style()
        #part icon root
        hostuicon = PhotoImage(file='logohos_70x70.png')
        #root_editprofile.iconphoto(False, hostuicon) 
        
        placeholderArray=['','','','','','','','']

        for i in range(0,8):
            placeholderArray[i]= tkinter.StringVar()

        #part photo back ground
        bg_edt_2=Image.open('hd-wall3.jpg') 
        bg_edt_2_jpg = ImageTk.PhotoImage(bg_edt_2)
        bg_img = Label(root_editprofile,image=bg_edt_2_jpg)
        bg_img.place(relheight=1,relwidth=1)

        #part frame 
        frame_information = Frame(root_editprofile,width=610,height=250,bg='white')
        frame_information.place(x=350,y=50)

        frame_descripe = Frame(root_editprofile,width=425,height=250,bg='white')
        frame_descripe.place(x=995,y=50)

        frame_treeview = Frame(root_editprofile,width=1073,height=447,bg='white')
        frame_treeview.place(x=350,y=350)

        #part tab editprofile
        edt1 = Button(root_editprofile,padx=24,pady=7,border=1,bg='#C1CDCD',text='Edit Profile',font=('Jasmine UPC',18,'bold'),cursor='hand2',state='normal',command=signup_page_2)
        edt1.place(x=50,y=350)
        edt2 = Button(root_editprofile,padx=19,pady=7,border=1,bg='#C1CDCD',text='Test History',font=('Jasmine UPC',18,'bold'),cursor='hand2')
        edt2.place(x=50,y=450)
        edt3 = Button(root_editprofile,padx=15,pady=7,border=1,bg='#32CD32',text='Start Testing',font=('Jasmine UPC',18,'bold'),cursor='hand2',command=start_test)
        edt3.place(x=50,y=550)
        edt4 = Button(root_editprofile,padx=15,pady=7,border=1,bg='#FF0000',text='Exit Program',font=('Jasmine UPC',18,'bold'),command=destroy_profile,cursor='hand2')
        edt4.place(x=50,y=650)

        import_excel = Button(root_editprofile,text='Import Excel',relief='ridge',cursor='hand2',command=select_file)
        import_excel.place(x=1170,y=820)
        export_excel = Button(root_editprofile,text='Export Excel',relief='ridge',cursor='hand2',command=exportExcel)
        export_excel.place(x=1270,y=820)

        #part photo profile
        imgprofile_aft_ed = PhotoImage(file='Profile (1).png')
        lbl_show_pic = Label(root_editprofile,bg='#F0FFFF',highlightthickness=3,image=imgprofile_aft_ed)
        lbl_show_pic.place(x=42,y=50)

        #part show picture profile onscreen 
        try:
            con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Database Connectivity Issue, Please Try Again')
            return
    
        try:
            query='use userdata_3'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata_3')
    
        query='select image from data where userid=%s'  
        mycursor.execute(query,(user_entry.get()))
        image_bytes = mycursor.fetchone()[0]
        if image_bytes != None:
            image = Image.open(io.BytesIO(image_bytes))
            image = image.resize((200, 200))
            photo_image = ImageTk.PhotoImage(image)
            lbl_show_pic.config(image=photo_image)
        #frame_image = Frame(root_editprofile,width=200,height=200)
        #frame_image.place(x=47,y=55)
        #label_pic = Label(frame_image, image= photo_image)
        #label_pic.place(x=0,y=0)

        #part time
        #now = datetime.now()
        #date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        #date_time_lable = Label(root_editprofile,text=date_time,fg='black',font=('Jasmine UPC',12,'bold'))
        #date_time_lable.place(x=50,y=800)

        #part main information

        heading_name = Label(frame_information,text='Name :',bg='white')
        heading_name.place(x=5,y=10)
        name_entry = Entry(frame_information,width=60,textvariable=placeholderArray[1])
        name_entry.place(x=100,y=10)

        heading_lastname = Label(frame_information,text='Lastname :',bg='white')
        heading_lastname.place(x=5,y=40)
        lastname_entry = Entry(frame_information,width=60,textvariable=placeholderArray[2])
        lastname_entry.place(x=100,y=40)

        heading_department = Label(frame_information,text='Department :',bg='white')
        heading_department.place(x=5,y=70)
        department_entry = Entry(frame_information,width=60,textvariable=placeholderArray[3])
        department_entry.place(x=100,y=70)

        heading_type = Label(frame_information,text='Type washed :',bg='white')
        heading_type.place(x=5,y=100)
        type_wash_entry = Entry(frame_information,width=60,textvariable=placeholderArray[4])
        type_wash_entry.place(x=100,y=100)

        heading_score = Label(frame_information,text='score :',bg='white')
        heading_score.place(x=5,y=130)
        score_entry = Entry(frame_information,width=60,textvariable=placeholderArray[5])
        score_entry.place(x=100,y=130)

        heading_result = Label(frame_information,text='result :',bg='white')
        heading_result.place(x=5,y=160)
        result_combobox = ttk.Combobox(frame_information,values=('','Pass','Fail'),textvariable=placeholderArray[6],width=25,cursor='hand2')
        result_combobox.place(x=100,y=160)

        heading_date_test = Label(frame_information,text='Date test :',bg='white')
        heading_date_test.place(x=5,y=190)
        date_test_entry = Entry(frame_information,width=60,textvariable=placeholderArray[7])
        date_test_entry.place(x=100,y=190)

        heading_no = Label(frame_information,text='No.',bg='white')
        heading_no.place(x=5,y=220)
        no_entry = Entry(frame_information,width=20,textvariable=placeholderArray[0])
        no_entry.place(x=100,y=220)

        savebutton = Button(frame_information,text='Save',font=('Jasmine UPC',12),padx=12,relief='raised',border=1,cursor='hand2',command=save)
        savebutton.place(x=500,y=10)

        selectbutton = Button(frame_information,text='Select',font=('Jasmine UPC',12),padx=8,relief='raised',border=1,cursor='hand2',command=select)
        selectbutton.place(x=500,y=50)

        Updatebutton = Button(frame_information,text='Update',font=('Jasmine UPC',12),padx=5,relief='raised',border=1,cursor='hand2',command=update)
        Updatebutton.place(x=500,y=90)

        Deletebutton = Button(frame_information,text='Delete',font=('Jasmine UPC',12),padx=7,relief='raised',border=1,cursor='hand2',command=delete)
        Deletebutton.place(x=500,y=130)

        findbutton = Button(frame_information,text='Find',font=('Jasmine UPC',12),padx=14,relief='raised',border=1,cursor='hand2',command=find)
        findbutton.place(x=500,y=170)

        clear_button = Button(frame_information,text='Clear',font=('Jasmine UPC',12),padx=11,relief='raised',border=1,cursor='hand2',command=clear)
        clear_button.place(x=500,y=210)

        def set_dtbname_sql():
            tablename = dtb_combobox.get()
            try:
                # เชื่อมต่อกับฐานข้อมูล
                con = pymysql.connect(host='localhost', user='root', password='Jamesanddef00')
                mycursor = con.cursor()

                # ตรวจสอบว่าฐานข้อมูลมีอยู่หรือไม่
                mycursor.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'test1'" )
                exists = mycursor.fetchone()

                if exists:
                    # ฐานข้อมูลมีอยู่ ใช้ฐานข้อมูลนั้น
                    mycursor.execute('USE test1')
                else:
                    # ฐานข้อมูลไม่มีอยู่ สร้างฐานข้อมูลใหม่
                    mycursor.execute('CREATE DATABASE test1')
                    mycursor.execute(f'USE test1')  # เปลี่ยนไปใช้ฐานข้อมูลที่สร้างใหม่

                # ตรวจสอบว่าตารางมีอยู่หรือไม่
                mycursor.execute(f"SHOW TABLES LIKE '{tablename}'")
                table_exists = mycursor.fetchone()

                if table_exists:
                    show_dtbname_label.config(text=f'{tablename}')
                    root_editprofile.focus_set()
                    refreshTable()
                else:
                    # สร้างตาราง
                    query = f'CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, name VARCHAR(50), lastname VARCHAR(50), department VARCHAR(50), type_wash VARCHAR(50), score VARCHAR(10), result VARCHAR(10), date_test VARCHAR(20))'
                    mycursor.execute(query)
                    mycursor.execute(f"SHOW TABLES LIKE '{tablename}'")
                    table_exists = mycursor.fetchone()
                    con.commit()
                    show_dtbname_label.config(text=f'{tablename}')
                    root_editprofile.focus_set()
                    refreshTable()

            except (pymysql.err.OperationalError, pymysql.err.ProgrammingError) as err:
                # จัดการข้อผิดพลาดการเชื่อมต่อฐานข้อมูลหรือการเรียกใช้คิวรี
                messagebox.showerror('Error', f'ข้อผิดพลาดฐานข้อมูล: {str(err)}')

            finally:
                # ปิดการเชื่อมต่อ (ถ้ามี)
                if con:
                    con.close()
                show_dtbname_label.config(text=f'{tablename}')
                set_dtbname_entry.delete(0,END)
                before_delete()
                root_editprofile.focus_set()

        choose_dtbname_heading = Label(frame_descripe,text='Choose Database :',bg='white')
        choose_dtbname_heading.place(x=5,y=160)

        def on_entry_change(*args):
            # เมื่อข้อความใน Entry เปลี่ยนแปลง ตรวจสอบว่ามีข้อความหรือไม่
            if entry_var.get().strip():
                set_dtbname_button.config(state=tk.NORMAL)
                set_dtbname_button.config(cursor='hand2')
            else:
                set_dtbname_button.config(state=tk.DISABLED)
                set_dtbname_button.config(cursor='')

        entry_var = tk.StringVar()
        entry_var.trace('w', on_entry_change)
        set_dtbname_heading = Label(frame_descripe,text='Add database :',bg='white')
        set_dtbname_heading.place(x=5,y=194)
        def validate_input(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
            # ตรวจสอบว่าข้อความใหม่เป็นตัวอักษรพิมพ์เล็กภาษาอังกฤษหรือไม่
            if text.isalpha() and text.islower():
                return True
            elif text == "":  # อนุญาตให้ลบข้อความ
                return True
            else:
                return False
        vcmd = (root_editprofile.register(validate_input), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        set_dtbname_entry = tk.Entry(frame_descripe,width=25,bg='#F5F5F5',textvariable=entry_var,validate="key", validatecommand=vcmd)
        set_dtbname_entry.place(x=130,y=195)

        mycursor.execute('use test1')
        mycursor.execute(f"SHOW TABLES")
        table_fetch = mycursor.fetchall()

        def add_to_combobox():
            tablename = dtb_combobox.get() or set_dtbname_entry.get()
            try:
                # เชื่อมต่อกับฐานข้อมูล
                con = pymysql.connect(host='localhost', user='root', password='Jamesanddef00')
                mycursor = con.cursor()
                mycursor.execute('use test1')
                mycursor.execute(f"SHOW TABLES LIKE '{tablename}'")
                table_exists = mycursor.fetchone()
                if table_exists:
                    # ตารางมีอยู่ แสดงข้อความแจ้งเตือน
                    messagebox.showerror('Error', f'Database " {tablename} " Already Exist Please change database.')
                else:
                    new_item = set_dtbname_entry.get()
                    current_values = set_dtbname_combobox['values']
                    updated_values = list(current_values)  # สร้างรายการใหม่เพื่อประกอบด้วยรายการเดิมและรายการใหม่
                    updated_values.append(new_item)
                    set_dtbname_combobox['values'] = updated_values
                    set_dtbname_entry.delete(0, END)
            except (pymysql.err.OperationalError, pymysql.err.ProgrammingError) as err:
                # จัดการข้อผิดพลาดการเชื่อมต่อฐานข้อมูลหรือการเรียกใช้คิวรี
                messagebox.showerror('Error', f'ข้อผิดพลาดฐานข้อมูล: {str(err)}')

            finally:
                # ปิดการเชื่อมต่อ (ถ้ามี)
                if con:
                    con.close()

        def before_delete():
            delete_dtbname_button.config(state='active')
            delete_dtbname_button.config(cursor='hand2')

        def delete_dtb_sql():
            tablename = show_dtbname_label.cget("text")
            print(tablename)
            if dtb_combobox.get() == show_dtbname_label.cget("text"):
                try:
                    # เชื่อมต่อกับฐานข้อมูล
                    con = pymysql.connect(host='localhost', user='root', password='Jamesanddef00')
                    mycursor = con.cursor()

                    # ตรวจสอบว่าฐานข้อมูลมีอยู่หรือไม่
                    mycursor.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'test1'")
                    exists = mycursor.fetchone()

                    if exists:
                        # ฐานข้อมูลมีอยู่ ใช้ฐานข้อมูลนั้น
                        mycursor.execute('USE test1')
                    else:
                        # ฐานข้อมูลไม่มีอยู่ สร้างฐานข้อมูลใหม่
                        mycursor.execute('CREATE DATABASE test1')
                        mycursor.execute(f'USE test1')  # เปลี่ยนไปใช้ฐานข้อมูลที่สร้างใหม่

                    mycursor.execute(f"SHOW TABLES LIKE '{tablename}'")
                    mycursor.execute(f'DROP TABLE {tablename}')
                    con.commit()

                    # ลบข้อมูลใน Treeview
                    for item in treeview.get_children():
                        treeview.delete(item)

                    # แปลงค่า Combobox ให้อยู่ในรูปแบบรายการ
                    combobox_values = [value[0] if isinstance(value, tuple) else value for value in set_dtbname_combobox['values']]

                    # ลบชื่อที่ตรงกับ tablename ใน Combobox
                    set_dtbname_combobox.set('')
                    print(combobox_values)
                    if tablename in combobox_values:
                        combobox_values.remove(tablename)
                        set_dtbname_combobox.config(values=combobox_values)  # อัพเดตค่าใน Combobox

                    messagebox.showinfo('Success','Database already delete')

                except (pymysql.err.OperationalError, pymysql.err.ProgrammingError) as err:
                    # จัดการข้อผิดพลาดการเชื่อมต่อฐานข้อมูลหรือการเรียกใช้คิวรี
                    messagebox.showerror('Error', f'ข้อผิดพลาดฐานข้อมูล: {str(err)}')

                finally:
                    # ปิดการเชื่อมต่อ (ถ้ามี)
                    if con:
                        con.close()
                    show_dtbname_label.config(text='')
                    delete_dtbname_button.config(state='disabled')
                    delete_dtbname_button.config(cursor='')
                    clear()
                    root_editprofile.focus_set()
            else:
                messagebox.showerror('Error','Please select your database')
                return

        dtb_combobox = StringVar()
        set_dtbname_combobox = ttk.Combobox(frame_descripe,width=25,background='#F5F5F5',values=table_fetch,textvariable=dtb_combobox,cursor='hand2')
        set_dtbname_combobox.place(x=130,y=160)
        choose_dtbname_button = tk.Button(frame_descripe,text='Enter',padx=5,command=set_dtbname_sql,cursor='hand2')
        choose_dtbname_button.place(x=330,y=155)
        set_dtbname_button = tk.Button(frame_descripe,text='Add',padx=7,command=add_to_combobox,state=tk.DISABLED)
        set_dtbname_button.place(x=330,y=188)
        show_dtbname_heading = Label(frame_descripe,text='Database name :',bg='white')
        show_dtbname_heading.place(x=5,y=223)
        show_dtbname_label = Label(frame_descripe,text='',bg='white',fg='#00CC00')
        show_dtbname_label.place(x=130,y=223)
        delete_dtbname_button = tk.Button(frame_descripe,text='Delete',padx=5,state='disabled',command=delete_dtb_sql)
        delete_dtbname_button.place(x=330,y=220)

        treeview=ttk.Treeview(frame_treeview,show='headings',height=21)

        def connection():
            conn=pymysql.connect(
                host='localhost',
                user='root',
                password='Jamesanddef00',
                db='test1'
            )
            return conn

        conn=connection()
        cursor=conn.cursor()

        def read():
            cursor.connection.ping()
            data = set_dtbname_combobox.get()
            print(data)
            sql=f"select * FROM {data} " 
            cursor.execute(sql)
            results=cursor.fetchall()
            conn.commit()
            conn.close()
            return results

        def refreshTable():
            for data in treeview.get_children():
                treeview.delete(data)
            for array in read():
                # แทนที่ค่า None ด้วยค่าว่างในแต่ละ column
                filtered_array = [col if col is not None else '' for col in array]
                treeview.insert(parent='', index='end', iid=array, text="", values=(filtered_array), tag="orow")
            treeview.tag_configure('orow', background="#EEEEEE")
            treeview.pack()

        style.configure(root_editprofile)
        treeview['columns']=("No.","Name","Lastname","Department","Type washed","Score","Result","Date test")
        treeview.column("#0",width=0,stretch=NO)
        treeview.column("No.",anchor=CENTER,width=70)
        treeview.column("Name",anchor=CENTER,width=125)
        treeview.column("Lastname",anchor=CENTER,width=125)
        treeview.column("Department",anchor=CENTER,width=150)
        treeview.column("Type washed",anchor=CENTER,width=150)
        treeview.column("Score",anchor=CENTER,width=150)
        treeview.column("Result",anchor=CENTER,width=150)
        treeview.column("Date test",anchor=CENTER,width=150)
        treeview.heading("No.",text="No.",anchor=CENTER)
        treeview.heading("Name",text="Name",anchor=CENTER)
        treeview.heading("Lastname",text="Lastname",anchor=CENTER)
        treeview.heading("Department",text="Department",anchor=CENTER)
        treeview.heading("Type washed",text="Type washed",anchor=CENTER)
        treeview.heading("Score",text="Score",anchor=CENTER)
        treeview.heading("Result",text="Result",anchor=CENTER)
        treeview.heading("Date test",text="Date test",anchor=CENTER)
        treeview.tag_configure('orow',background="#EEEEEE")
        treeview.place(x=0,y=0)

        #part name_admin

        mycursor.execute('use userdata_3')
        query='select firstname from data where userid=%s'  
        mycursor.execute(query,(user_entry.get()))
        firstname_fetch = mycursor.fetchone()[0]
        hi_label = Label(frame_descripe,text='HI,',font=('Arial',26,'bold'),border=0,bg='white')
        hi_label.place(x=20,y=30)
        fisrtname_entry = Entry(frame_descripe,text='',font=('Arial',28,'bold'),border=0,bg='white',width=20,readonlybackground='white')
        fisrtname_entry.place(x=80,y=27)
        if firstname_fetch != None:
            fisrtname_entry.insert(0,firstname_fetch)
        fisrtname_entry.config(state='readonly')

        #part time onscreen
        IST = pytz.timezone('Asia/Bangkok')
        label_date_now = Label(root_editprofile,text='',font=('Jasmine UPC',10,'bold'),bg='#d1d1d1')
        label_date_now.place(x=65,y=765)
        label_time_now = Label(root_editprofile,text='',font=('Jasmine UPC',10,'bold'),bg='#d1d1d1')
        label_time_now.place(x=155,y=765)
        def update_clock():
            raw_TS = datetime.now(IST)
            date_now = raw_TS.strftime("%d %b %Y")
            time_now = raw_TS.strftime("%H:%M:%S %p")
            formatted_now = raw_TS.strftime("%d-%m-%Y")
            label_date_now.config(text = date_now)
            # label_date_now.after(500, update_clock)
            label_time_now.config(text = time_now)
            label_time_now.after(1000, update_clock)
            return formatted_now
        update_clock()
        #app =FullScreen(root_editprofile)    #ใช้กับ fuction class 
        root_editprofile.mainloop()

    if user_entry.get()=='USER ID' or user_entry.get()==''or password_entry.get()=='Password' or password_entry.get()=='':
        messagebox.showerror('Error','All Fields Are Require')
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='Jamesanddef00')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Connection is not established try again')
            return
        query = 'use userdata_3'
        mycursor.execute(query)
        query = 'select * from data where userid=%s and password=%s'
        mycursor.execute(query,(user_entry.get(),password_entry.get())) #check userid และ password ว่าที่ผู้ใช้ป้อน ตรงกับในฐานข้อมูลไหม
        row=mycursor.fetchone() 
        if row==None: #ไม่ตรงกับในฐานข้อมูลเลยทั้งคู่
            messagebox.showerror('Error','Invalid UserID or Password')
        else:
            messagebox.showinfo('Success','Login is successful')
            root.withdraw() # withdraw คำสั่งซ่อนหน้าต่าง 
            afterlogin_editprofile()

def on_closing_root():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
               
root = Tk()

root.title('Hand Hygeine Testing - TUH')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False,False)

img = PhotoImage(file='logohandwash_resize.png')
#photo = ImageTk.PhotoImage(img) #แปลง pillow image ให้เป็น TkImage
Label(root,image=img,bg='white').place(x=125,y=50)

logohos = PhotoImage(file= 'logohos2.png')
Label(root,image=logohos,bg='white').place(x=50,y=400)

logotu = PhotoImage(file= 'tulogo (1).png')
Label(root,image=logotu,bg='white').place(x=455,y=410)

logotse = PhotoImage(file= 'tselogo100.png')
Label(root,image=logotse,bg='white').place(x=550,y=400)

guiicon = PhotoImage(file='hand_icon_.png')
hand_icon = PhotoImage(file='hand-washing_icon.png')
hostuicon = PhotoImage(file='logohos_70x70.png')
root.iconphoto(False, hostuicon,guiicon) 

frame=Frame(root,width=350,height=300,bg='#FFFFFF')#สร้างกรอบภายใน geometry ที่ตั้ง (ตั้งสีที่มองเห็นชัดก่อนตอนแรกค่อยเปลี่ยน)
frame.place(x=480,y=80)

heading1=Label(text='Hand Hygeine Testing',fg='#363636',bg='white',font=('Oswald',30,'bold')) #คำและoptionใน frame
heading1.place(x=470,y=15)

heading2=Label(frame,text='Sign in',fg='#FF0000',bg='white',font=('Jasmine UPC',23,'bold')) #คำและoptionใน frame
heading2.place(x=115,y=15) #ต้องวางตำแหน่งหัวข้อถึงจะโชว์

# Username
def on_enter(event):
    name = user_entry.get()
    if name == 'USER ID' :
      user_entry.delete(0,'end')
def on_leave(event):
    name=user_entry.get()
    if name == '':
        user_entry.insert(0,'USER ID') 
    
user_entry = Entry(frame,width=25,fg='#4F4F4F',border=0,bg='white',font=('Ubuntu',11))
user_entry.place(x=30,y=90)
user_entry.insert(0,'USER ID')
user_entry.bind('<FocusIn>',on_enter)
user_entry.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='#4F4F4F').place(x=25,y=117)

# Password
def on_focus_in(event):
    password_login = event.widget
    if password_login.get() == 'Password':
       password_login.delete(0, 'end')
       password_login.config(show='*')       

def on_focus_out(event):
    password_login = event.widget
    if password_login.get() == '':
       password_login.insert(0, 'Password')
       password_login.config(show='')
def show_password():
    if password_entry.cget('show')=='*':
        password_entry.config(show='')
    else:
        password_entry.config(show='*')

password_entry = Entry(frame,width=25,fg='#4F4F4F',border=0,bg='white',font=('Ubuntu',11))
password_entry.place(x=30,y=160)
password_entry.insert(0,'Password')
password_entry.bind('<FocusIn>',on_focus_in)
password_entry.bind('<FocusOut>',on_focus_out)

Frame(frame,width=295,height=2,bg='#4F4F4F').place(x=25,y=187)

#CheckPassword_Button
checkpassword = IntVar()
Check_Password = Checkbutton(frame, text='Show Password',command=show_password,bg='white',cursor='hand2',variable=checkpassword)
Check_Password.place(x=30,y=247)

#button
def on_enter_pressed(event=None):
    login_user()
    
button=Button(frame,width=39,pady=7,border=0,bg='#57a1f8',text='Enter',fg='white',command=login_user,cursor='hand2').place(x=35,y=205) #pad y ขนาดภายนอกของกรอบ widget
root.bind('<Return>', on_enter_pressed)

#sign_up
sign_up = Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#1E90FF',command=sign_up_page)
sign_up.place(x=92,y=275)

Frame(frame,width=2,height=12,bg='#4F4F4F').place(x=150,y=280)

#Forget Password
fogetpass = Button(frame,width=13,text='Forget Password ?',border=0,bg='white',cursor='hand2',fg='#1E90FF',command=forgetpassword)
fogetpass.place(x=165,y=275)

root.protocol("WM_DELETE_WINDOW", on_closing_root)
root.mainloop()