
from customtkinter import *
import sqlite3
from tkinter import *
from tkinter import ttk
import sqlite3 as sq3
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import time


def LoginWindow():
    def initialize_databases():
        member_conn = sqlite3.connect('member.db')
        member_cursor = member_conn.cursor()
        member_cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL UNIQUE,
                                    email TEXT NOT NULL,
                                    password TEXT NOT NULL)''')
        member_conn.commit()
        member_conn.close()

        vip_conn = sqlite3.connect('vip.db')
        vip_cursor = vip_conn.cursor()
        vip_cursor.execute('''CREATE TABLE IF NOT EXISTS vips (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL UNIQUE,
                                    email TEXT NOT NULL,
                                    password TEXT NOT NULL)''')
        vip_conn.commit()
        vip_conn.close()

    initialize_databases()

    def username_exists(username, user_type):
        if user_type == 'member':
            conn = sqlite3.connect('member.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members WHERE username=?", (username,))
        else:
            conn = sqlite3.connect('vip.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vips WHERE username=?", (username,))

        result = cursor.fetchone()
        conn.close()
        return result is not None

    def save_member(username, email, password):
        member_conn = sqlite3.connect('member.db')
        member_cursor = member_conn.cursor()
        member_cursor.execute("INSERT INTO members (username, email, password) VALUES (?, ?, ?)",
                              (username, email, password))
        member_conn.commit()
        member_conn.close()

    def save_vip(username, email, password):
        vip_conn = sqlite3.connect('vip.db')
        vip_cursor = vip_conn.cursor()
        vip_cursor.execute("INSERT INTO vips (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))
        vip_conn.commit()
        vip_conn.close()

    def verify_login(username, password, user_type):
        if user_type == 'member':
            member_conn = sqlite3.connect('member.db')
            member_cursor = member_conn.cursor()
            member_cursor.execute("SELECT * FROM members WHERE username=? AND password=?", (username, password))
            result = member_cursor.fetchone()
            member_conn.close()
        elif user_type == 'vip':
            vip_conn = sqlite3.connect('vip.db')
            vip_cursor = vip_conn.cursor()
            vip_cursor.execute("SELECT * FROM vips WHERE username=? AND password=?", (username, password))
            result = vip_cursor.fetchone()
            vip_conn.close()
        else:
            result = None

        return result is not None

    def open_login_page():
        for widget in app.winfo_children():
            widget.destroy()

        login_label = CTkLabel(app,
                               text="Login",
                               font=("Arial Bold", 50))
        login_label.place(x=175, y=50)

        login_entry1 = CTkEntry(master=app,
                                placeholder_text="Username",
                                fg_color="#3B3B3B",
                                width=300,
                                height=40,
                                text_color="white")
        login_entry1.place(x=100, y=200)

        login_entry2 = CTkEntry(master=app,
                                placeholder_text="Password",
                                fg_color="#3B3B3B",
                                width=300,
                                height=40,
                                text_color="white",
                                show='*')
        login_entry2.place(x=100, y=260)

        def toggle_password_visibility():
            if show_password_var.get():
                login_entry2.configure(show='')
            else:
                login_entry2.configure(show='*')

        show_password_var = BooleanVar()
        show_password_checkbutton = CTkCheckBox(master=app,
                                                text="Show Password",
                                                variable=show_password_var,
                                                command=toggle_password_visibility)
        show_password_checkbutton.place(x=100, y=310)

        user_type_var = StringVar(value='member')
        member_radiobutton = CTkRadioButton(master=app, text='Member', variable=user_type_var, value='member')
        member_radiobutton.place(x=100, y=340)
        vip_radiobutton = CTkRadioButton(master=app, text='VIP', variable=user_type_var, value='vip')
        vip_radiobutton.place(x=200, y=340)

        def login():
            global username
            global password
            global user_type
            username = login_entry1.get()
            password = login_entry2.get()
            user_type = user_type_var.get()
            if verify_login(username, password, user_type):
                messagebox.showinfo("Login", "Login Successful!")
                app.destroy()
                MainTabs()
            else:
                messagebox.showerror("Login", "Invalid username or password.")

        login_button = CTkButton(master=app,
                                 text="Log In",
                                 width=300,
                                 height=50,
                                 corner_radius=32,
                                 fg_color="#6D9773",
                                 hover_color="#FFBA00",
                                 command=login)
        login_button.place(x=100, y=380)

    def toggle_register_button():
        if checkbox_var.get():
            button.configure(state=NORMAL)
        else:
            button.configure(state=DISABLED)

    app = CTk()
    app.geometry("+0+0")
    app.geometry("500x800")
    app.title("Registration")
    set_appearance_mode("dark")

    my_label1 = CTkLabel(app,
                         text="Registration",
                         font=("Arial Bold", 50))
    my_label1.place(x=100, y=100)

    canvas = Canvas(app, width=300, height=1, bg="white", highlightthickness=0)
    canvas.place(x=100, y=160)
    canvas.create_line(0, 0, 300, 0, fill="#FFFFFF", width=2)

    my_label2 = CTkLabel(app,
                         text="Parking Reservation!",
                         font=("Arial", 20))
    my_label2.place(x=150, y=170)

    entry1 = CTkEntry(master=app,
                      placeholder_text="Username",
                      fg_color="#3B3B3B",
                      width=300,
                      height=40,
                      text_color="white")
    entry1.place(x=100, y=350)

    entry2 = CTkEntry(master=app,
                      placeholder_text="Email",
                      fg_color="#3B3B3B",
                      width=300,
                      height=40,
                      text_color="white")
    entry2.place(x=100, y=410)

    entry3 = CTkEntry(master=app,
                      placeholder_text="Password",
                      fg_color="#3B3B3B",
                      width=300,
                      height=40,
                      text_color="white")
    entry3.place(x=100, y=470)

    checkbox_var = BooleanVar()
    checkbox = CTkCheckBox(master=app,
                           text="Agree with the Terms & Conditions",
                           fg_color="#FFBA00",
                           checkbox_height=20,
                           checkbox_width=20,
                           corner_radius=26,
                           variable=checkbox_var,
                           command=toggle_register_button)
    checkbox.place(x=110, y=530)

    def register_user():
        username = entry1.get()
        email = entry2.get()
        password = entry3.get()

        if username_exists(username, 'member') or username_exists(username, 'vip'):
            messagebox.showerror("Registration", "Username already exists. Please choose another one.")
        else:
            if VIPSwitch.get() == "on":
                save_vip(username, email, password)
            else:
                save_member(username, email, password)
            messagebox.showinfo("Registration", "Registration Successful!")
            open_login_page()

    button = CTkButton(master=app,
                       text="Create An Account",
                       width=300,
                       height=50,
                       corner_radius=32,
                       fg_color="#6D9773",
                       hover_color="#FFBA00",
                       state=DISABLED,
                       command=register_user)
    button.place(x=100, y=570)

    MyLabel3 = CTkLabel(app,
                        text="Member",
                        font=("Arial bold", 15))
    MyLabel4 = CTkLabel(app,
                        text="VIP",
                        font=("Arial bold", 15),
                        text_color="#FFBA00")
    MyLabel3.place(x=100, y=300)
    MyLabel4.place(x=370, y=300)

    def switcher():
        if VIPSwitch.get() == "on":
            entry1.configure(fg_color="#FFBA00", text_color="black", placeholder_text_color="#3B3B3B")
            entry2.configure(fg_color="#FFBA00", text_color="black", placeholder_text_color="#3B3B3B")
            entry3.configure(fg_color="#FFBA00", text_color="black", placeholder_text_color="#3B3B3B")
        else:
            entry1.configure(fg_color="#3B3B3B", text_color="white")
            entry2.configure(fg_color="#3B3B3B", text_color="white")
            entry3.configure(fg_color="#3B3B3B", text_color="white")

    global VIPSwitch
    VIPSwitch = StringVar(value="off")
    MySwitch = CTkSwitch(app, text=" ",
                         command=switcher,
                         variable=VIPSwitch,
                         onvalue="on",
                         offvalue="off")
    MySwitch.place(x=250, y=300)

    my_label2 = CTkLabel(app,
                         text="Already Registered?",
                         font=("Arial", 15))
    my_label2.place(x=100, y=700)

    login_button = CTkButton(master=app,
                             text="Log In",
                             corner_radius=32,
                             fg_color="#6D9773",
                             hover_color="#FFBA00",
                             command=open_login_page)
    login_button.place(x=250, y=700)

    app.mainloop()


def MainTabs():
    set_appearance_mode("System")
    set_default_color_theme("dark-blue")

    #   Main window attributes
    root = CTk()
    root.title("Roque Road")
    root.geometry('+0+0')
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    #   constants
    primary_color = "#6d9773"
    secondary_color = "#0c3b2e"
    accent_color = "#bb8a52"
    highlight_color = "#ffba00"
    white_color = "#ffffff"
    widthvar = root.winfo_screenwidth()
    heightvar = root.winfo_screenheight()
    windowcolor = root.cget("bg")

    current_frame = StringVar(value="homepage")

    #   Ribbon
    upperFrame = CTkCanvas(root, height=200, bg="#162c15")
    upperFrame.grid(row=0, column=0)

    tab = CTkTabview(upperFrame,
                     width=root.winfo_screenwidth(),
                     height=root.winfo_screenheight(),
                     segmented_button_selected_color="green",
                     corner_radius=7)

    tab.grid(row=1, column=0)

    #   Tabs
    home = tab.add("Home")
    reserve = tab.add("Reserve")
    status = tab.add("Status")


    # Home Tab
    def show_homepage():
        current_frame.set("homepage")
        homepage_frame.pack(expand=True, fill="both")

    homepage_frame = CTkScrollableFrame(home, fg_color=white_color)
    homepage_frame.pack(expand=True, fill="both", padx=20, pady=20)

    logo_image = Image.open("VisualAssets/Logo.jpg")
    logo_image = logo_image.resize((110, 110))
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = CTkLabel(homepage_frame, image=logo_photo, text="Roque Roads", compound="left", text_color="#E6C104",
                          font=("Times New Roman",105))
    logo_label.pack(padx=30)

    homepage_image = Image.open("VisualAssets/HomePageImage.jpg")
    homepage_photo = ImageTk.PhotoImage(homepage_image)

    homepage_label = CTkLabel(homepage_frame, image=homepage_photo, text="")
    homepage_label.pack(side="top", fill="x")

    map_label = CTkLabel(homepage_frame, text="We are located here", text_color=primary_color, font=("Arial", 35))
    map_label.pack(pady=10)

    homepage_image2 = Image.open("VisualAssets/Location.png")
    homepage_photo2 = ImageTk.PhotoImage(homepage_image2)
    homepage_label2 = CTkLabel(homepage_frame, image=homepage_photo2, text="")
    homepage_label2.pack()

    offers_label = CTkLabel(homepage_frame, text="OFFERS", text_color=primary_color, font=("Arial", 24))
    offers_label.pack(pady=20)

    offers_frame = CTkFrame(homepage_frame, fg_color=white_color)
    offers_frame.pack(pady=10)

    offers = [("MEMBER", "REGULAR RATES"), ("VIP", "EXCLUSIVE PERKS"), ("SEASON/HOLIDAYS", "COMING SOON...")]
    for offer in offers:
        offer_frame = CTkFrame(offers_frame, fg_color=white_color, border_color=primary_color, border_width=1,
                               width=300, height=200)
        offer_frame.grid(row=0, column=offers.index(offer), padx=10, pady=10)
        offer_label = CTkLabel(offer_frame, text=offer[0], text_color=primary_color, font=("Arial", 16))
        offer_label.pack(pady=10)
        offer_price = CTkLabel(offer_frame, text=offer[1], text_color="red", font=("Arial", 14))
        offer_price.pack(pady=5)

    faq_frame = CTkFrame(homepage_frame, fg_color=white_color, border_color=primary_color, border_width=2, corner_radius=10)
    faq_frame.pack(expand=True, fill="both", padx=10, pady=20)

    faq_label = CTkLabel(faq_frame, text="FAQ", text_color=primary_color, font=("Arial", 70))
    faq_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")

    faq_questions = [("What is the maximum duration I can stay in the parking area?",
                      "There is no time limit on the duration of your stay."),
                     ("What benefits are included with VIP parking?",
                      "VIP parking offers enhanced security for your vehicle, climate-controlled conditions, and\n additional space for greater convenience.")]

    question_label_1 = CTkLabel(faq_frame, text=faq_questions[0][0], text_color=primary_color, font=("Arial", 25))
    question_label_1.place(x=40, y=30)
    answer_label_1 = CTkLabel(faq_frame, text=faq_questions[0][1], text_color="black", font=("Arial", 15))
    answer_label_1.place(x=235, y=55)

    question_label_2 = CTkLabel(faq_frame, text=faq_questions[1][0], text_color=primary_color, font=("Arial", 25))
    question_label_2.place(x=1200, y=30)
    answer_label_2 = CTkLabel(faq_frame, text=faq_questions[1][1], text_color="black", font=("Arial", 15))
    answer_label_2.place(x=1160, y=55)

    # Create empty columns for spacing
    faq_frame.grid_columnconfigure(0, weight=1)
    faq_frame.grid_columnconfigure(1, weight=1)
    faq_frame.grid_columnconfigure(2, weight=1)

    #   End of home tab

    #   Main reservation tab

    def Status():
        root = CTk()
        root.title("Status page")
        root.geometry("+0+0")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        widthvar2 = root.winfo_screenwidth()
        heightvar2 = root.winfo_screenheight()
        set_appearance_mode("dark")

        rootcolor = root.cget("bg")

        UltimateFrame = CTkScrollableFrame(status, width=widthvar2, height=heightvar2)
        UltimateFrame.pack()
        UltimateFrame.columnconfigure(0, weight=1)


        def onclock():
            current_time = time.strftime('%Y-%m-%d')
            current_hour =  time.strftime('%H:%M:%S')
            time_label.configure(text=f"Current Date and Time: {current_time}, {current_hour}")
            time_label.after(1000, onclock)

        time_label = CTkLabel(UltimateFrame, font=("Century Gothic", 27), fg_color="#475E28")
        time_label.grid(row=0, sticky=EW, pady=20)

        onclock()


        def UpdateEntries():
            try:
                area_park_var.set(value=Reserver[0][0])
            except NameError:
                area_park_var.set(value="----")
            try:
                occupancy_var.set(value=Reserver[0][1])
            except NameError:
                occupancy_var.set(value="----")
            try:
                Plate_Number_var.set(value=Reserver[0][2])
            except NameError:
                Plate_Number_var.set(value="----")
            try:
                Vehicle_Type_var.set(value=Reserver[0][3])
            except NameError:
                Vehicle_Type_var.set(value="----")
            try:
                Start_Date_var.set(value=Reserver[0][4])
            except NameError:
                Start_Date_var.set(value="----")
            try:
                Start_Time_var.set(value=Reserver[0][5])
            except NameError:
                Start_Time_var.set(value="----")
            try:
                End_Date_var.set(value=Reserver[0][6])
            except NameError:
                End_Date_var.set(value="----")
            try:
                End_Time_var.set(value=Reserver[0][7])
            except NameError:
                End_Time_var.set(value="----")
            try:
                Total_payment_var.set(value=Reserver[0][8])
            except NameError:
                Total_payment_var.set(value="----")


        header_frame = CTkFrame(UltimateFrame, fg_color="Black")
        header_frame.grid(row=1, padx=10, pady=10, sticky=NSEW)
        header_frame.columnconfigure(0, weight=1)
        upper_frame = CTkFrame(header_frame, fg_color="Black", width=widthvar2)
        upper_frame.columnconfigure([0,1,2,3,4,5,6,7], weight=1)
        upper_frame.grid(row=1, column=0, padx=10, sticky=NSEW)
        upper_down = CTkFrame(header_frame, fg_color="Black")
        upper_down.grid(row=2, column=0, padx=10, pady=10, sticky=NS)
        upper_lower = CTkFrame(header_frame, fg_color="Black")
        upper_lower.grid(row=3, column=0, padx=10, pady=10, sticky=NS)

        status_label = CTkLabel(header_frame, text="See Your Parking Reservation Status", font=("Tahoma", 35))
        status_label.grid(row=0, column=0, pady=20)

        area_park_var = StringVar(value="------")
        area_park = CTkLabel(upper_frame, text="Parking Area", font=("Century Gothic", 30))
        area_park.grid(row=1, column=0, padx=10, pady=10)
        area_park_entry = CTkEntry(upper_frame, textvariable=area_park_var, width = 200, height=40, font=("Century Gothic", 22))
        area_park_entry.grid(row=2, column=0, padx=10, pady=10)

        occupancy_var = StringVar(value="------")
        occupancy = CTkLabel(upper_frame, text="Occupancy", font=("Century Gothic", 30))
        occupancy.grid(row=1, column=1, padx=10, pady=10)
        occupancy_entry = CTkEntry(upper_frame, textvariable=occupancy_var, width = 200, height=40, font=("Century Gothic", 22))
        occupancy_entry.grid(row=2, column=1, padx=10, pady=10)

        Plate_Number_var = StringVar(value="------")
        Plate_Number_ = CTkLabel(upper_frame, text="Plate Number", font=("Century Gothic", 30))
        Plate_Number_.grid(row=1, column=2, padx=10, pady=10)
        Plate_Number__entry = CTkEntry(upper_frame, textvariable=Plate_Number_var, width = 200, height=40, font=("Century Gothic", 22))
        Plate_Number__entry.grid(row=2, column=2, padx=10, pady=10)

        Vehicle_Type_var = StringVar(value="------")
        Vehicle_Type = CTkLabel(upper_frame, text="Vehicle Type", font=("Century Gothic", 30))
        Vehicle_Type.grid(row=1, column=3, padx=10, pady=10)
        Vehicle_Type_entry = CTkEntry(upper_frame, textvariable=Vehicle_Type_var, width = 200, height=40, font=("Century Gothic", 22))
        Vehicle_Type_entry.grid(row=2, column=3, padx=10, pady=10)

        Start_Date_var = StringVar(value="------")
        Start_Date = CTkLabel(upper_frame, text="Start Date", font=("Century Gothic", 30))
        Start_Date.grid(row=1, column=4, padx=10, pady=10)
        Start_Date_entry = CTkEntry(upper_frame, textvariable=Start_Date_var, width = 200, height=40, font=("Century Gothic", 22))
        Start_Date_entry.grid(row=2, column=4, padx=10, pady=10)

        Start_Time_var = StringVar(value="------")
        Start_Time = CTkLabel(upper_frame, text="Start Time", font=("Century Gothic", 30))
        Start_Time.grid(row=1, column=5, padx=10, pady=10, sticky="ew")
        Start_Time_entry = CTkEntry(upper_frame, textvariable=Start_Time_var, width = 200, height=40, font=("Century Gothic", 22))
        Start_Time_entry.grid(row=2, column=5, padx=10, pady=10, sticky="ew")

        End_Date_var = StringVar(value="------")
        End_Date = CTkLabel(upper_frame, text="End Date", font=("Century Gothic", 30))
        End_Date.grid(row=1, column=6, padx=10, pady=10, sticky="ew")
        End_Date_entry = CTkEntry(upper_frame, textvariable=End_Date_var, width = 200, height=40, font=("Century Gothic", 22))
        End_Date_entry.grid(row=2, column=6, padx=10, pady=10, sticky="ew")

        End_Time_var = StringVar(value="------")
        End_Time = CTkLabel(upper_frame, text="End Time", font=("Century Gothic", 30))
        End_Time.grid(row=1, column=7, padx=10, pady=10, sticky="ew")
        End_Time_entry = CTkEntry(upper_frame, textvariable=End_Time_var, width = 200, height=40, font=("Century Gothic", 22))
        End_Time_entry.grid(row=2, column=7, padx=10, pady=10, sticky="ew")

        Total_payment_var = StringVar(value="------")
        Total_payment = CTkLabel(upper_down, text="Total Payment", font=("Century Gothic", 30))
        Total_payment.grid(padx=10)
        Total_payment_entry = CTkEntry(upper_down, textvariable=Total_payment_var, width = 200, height=40, font=("Century Gothic", 22))
        Total_payment_entry.grid(padx=10, pady=10, sticky="news")

        See_Yours = CTkButton(upper_lower, text="See your reservation Info", width = 400, command=UpdateEntries, fg_color="#537B2E", 
                                     height=40, font=("Century Gothic", 30))
        See_Yours.grid(pady=30)

        for widget in upper_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        lower_frame = CTkFrame(UltimateFrame, fg_color="#475E28")
        lower_frame.grid(row=2, padx=10, pady=10, sticky=EW)

        completion_label = CTkLabel(lower_frame, text="Parking Status Information", font=("Century Gothic", 30))
        completion_label.pack(side="top", pady=(0,10))

        MainFrame = CTkScrollableFrame(UltimateFrame, bg_color=rootcolor, border_width=5, border_color="#353535",
                                        fg_color="Black", width=widthvar2/1.2, height=400)


        def Lister():
            i = 1
            ListUpdate = sq3.connect("parking.db")
            cursor3 = ListUpdate.cursor()

            CTkLabel(MainFrame, text="", font=("Century Gothic", 22), text_color="white",
                        fg_color=None).grid(column=0, row=0, padx=10)
            CTkLabel(MainFrame, text="Area", font=("Century Gothic", 22), text_color="white",
                        fg_color=None).grid(column=1, row=0, padx=10)
            CTkLabel(MainFrame, text="Occupancy", font=("Century Gothic", 22), text_color="white",
                        fg_color=None).grid(column=2, row=0, padx=10)
            CTkLabel(MainFrame, text="Plate Number", font=("Century Gothic", 22), text_color="white",
                        fg_color=None).grid(column=3, row=0, padx=10)
            CTkLabel(MainFrame, text="Vehicle Type", font=("Century Gothic", 22), text_color="white",
                        fg_color=None).grid(column=4, row=0, padx=10)
            CTkLabel(MainFrame, text="Start Date", font=("Century Gothic", 22), text_color="white", fg_color=None).grid(
                column=5, row=0, padx=10)
            CTkLabel(MainFrame, text="Start Time", font=("Century Gothic", 22), text_color="white",
                        fg_color=None).grid(column=6, row=0, padx=10)
            CTkLabel(MainFrame, text="End Date", font=("Century Gothic", 22), text_color="white",
                        fg_color=None).grid(column=7, row=0, padx=10)
            CTkLabel(MainFrame, text="End Time", font=("Century Gothic", 22), text_color="white",
                        fg_color=None).grid(column=8, row=0, padx=10)
            CTkLabel(MainFrame, text="Total Price", font=("Century Gothic", 22), text_color="white",
                        fg_color=None).grid(column=9, row=0, padx=10)

            while i != 36:
                cursor3.execute("SELECT rowid, * FROM parking WHERE rowid = ?", (str(i),))
                RefList = cursor3.fetchall
                Record = RefList()
                Texts = []

                if Record:
                    for items in range(0, 10):
                        if Record[0][items] == None:
                            Texts.append("----")
                        else:
                            Texts.append(Record[0][items])

                    C1 = CTkEntry(MainFrame, placeholder_text=str(Texts[0]), font=("Century Gothic", 22),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=55)
                    C2 = CTkEntry(MainFrame, placeholder_text=str(Texts[1]), font=("Century Gothic", 20),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=165)
                    C3 = CTkEntry(MainFrame, placeholder_text=str(Texts[2]), font=("Century Gothic", 20),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=165)
                    C4 = CTkEntry(MainFrame, placeholder_text=str(Texts[3]), font=("Century Gothic", 22),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=165)
                    C5 = CTkEntry(MainFrame, placeholder_text=str(Texts[4]), font=("Century Gothic", 22),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=165)
                    C6 = CTkEntry(MainFrame, placeholder_text=str(Texts[5]), font=("Century Gothic", 22),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=165)
                    C7 = CTkEntry(MainFrame, placeholder_text=str(Texts[6]), font=("Century Gothic", 22),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=165)
                    C8 = CTkEntry(MainFrame, placeholder_text=str(Texts[7]), font=("Century Gothic", 22),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=165)
                    C9 = CTkEntry(MainFrame, placeholder_text=str(Texts[8]), font=("Century Gothic", 22),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=165)
                    C10 = CTkEntry(MainFrame, placeholder_text=str(Texts[9]), font=("Century Gothic", 22),
                                    placeholder_text_color="white",
                                    fg_color="#202124", corner_radius=0, border_color="black", width=165)

                    C1.configure(state=DISABLED)
                    C1.grid(column=0, row=i)
                    C2.configure(state=DISABLED)
                    C2.grid(column=1, row=i)
                    C3.configure(state=DISABLED)
                    C3.grid(column=2, row=i)
                    C4.configure(state=DISABLED)
                    C4.grid(column=3, row=i)
                    C5.configure(state=DISABLED)
                    C5.grid(column=4, row=i)
                    C6.configure(state=DISABLED)
                    C6.grid(column=5, row=i)
                    C7.configure(state=DISABLED)
                    C7.grid(column=6, row=i)
                    C8.configure(state=DISABLED)
                    C8.grid(column=7, row=i)
                    C9.configure(state=DISABLED)
                    C9.grid(column=8, row=i)
                    C10.configure(state=DISABLED)
                    C10.grid(column=9, row=i)

                i += 1
            ListUpdate.close()

            def clear_frame():
                for widget in MainFrame.winfo_children():
                    widget.destroy()

            lower_body = CTkFrame(UltimateFrame)
            lower_body.grid(row=4)

            OpenB = CTkButton(lower_body, text="Open", fg_color="#537B2E", 
                            width=150, height=50, font=("Century Gothic", 30),command=Lister)
            OpenB.grid(row=0, column=0, padx=30, pady=30)
            RefreshB = CTkButton(lower_body, text="Refresh", fg_color="#537B2E", 
                                width=150, height=50, font=("Century Gothic", 30),command=clear_frame)
            RefreshB.grid(row=0, column=1, padx=30, pady=30)

            MainFrame.grid(row=3)


        def plotavg_week():
            income_dates = [f"{month}/2024" for month in range(1, 13)]
            price_amount = []

            conn = sq3.connect("parking.db")
            cursorbar = conn.cursor()

            for month in range(1, 13):
                month_pattern = f"2024/{month}/%"
                cursorbar.execute("SELECT SUM(Total_Price) FROM parking WHERE Start_Day LIKE ?", (month_pattern,))
                total_price = cursorbar.fetchone()[0]
                price_amount.append(total_price if total_price is not None else 0)

            conn.close()

            plt.figure(figsize=(10, 6))
            plt.plot(income_dates, price_amount, marker='o', linestyle='-')
            plt.xlabel("Month in 2024", labelpad=10, font="Tahoma", fontsize=10)
            plt.ylabel("Total Income", labelpad=10, font="Tahoma", fontsize=10)
            plt.title("Monthly Parking Reservation Income in 2024", font="Tahoma", fontsize=18, pad=10)
            plt.grid(linestyle="--", alpha=0.5, axis="y", zorder=-1)
            plt.gca().set_axisbelow(True)
            plt.tight_layout()
            plt.show()

        def bar_graph_income():
            types = ["Sedan", "Coupe", "Sports Car", "Station Wagon", "Hatchback", "Convertible", "SUV", "Minivan",
                    "Pickup Truck"]
            amount = []
            width = 0.3
            conn = sq3.connect("parking.db")
            cursorbar = conn.cursor()

            for items in types:
                cursorbar.execute("SELECT * FROM parking WHERE Vehicle_Type = ?", (items,))
                lister = cursorbar.fetchall()
                Number = len(lister)
                amount.append(Number)

            conn.close()

            x_positions = np.arange(len(amount)) * (1 + width)

            plt.figure(figsize=(10, 6))
            plt.bar(x_positions, amount, width=width, color="orange", label="Number of Vehicles Parked")

            plt.xticks(x_positions, types, rotation=45, ha='right')
            plt.xlabel("Vehicle Types", labelpad=10, font="Tahoma", fontsize=10)
            plt.ylabel("Number of Vehicles", labelpad=10, font="Tahoma", fontsize=10)
            plt.title("Number of Vehicles by Type", font="Tahoma", fontsize=18, pad=10)
            plt.grid(linestyle="--", alpha=0.5, axis="y", zorder=-1)
            plt.gca().set_axisbelow(True)
            plt.legend(loc="upper left")

            plt.tight_layout()
            plt.show()

        def show_graphs_plotavg():
            plotavg_week()

        def show_graphs_income():
            bar_graph_income()

        Footer_labelF = CTkFrame(UltimateFrame, fg_color="#475E28")
        Footer_Buttons = CTkFrame(UltimateFrame)
        Footer_labelF.grid(row=5, sticky=EW)
        Footer_Buttons.grid(row=6)

        Graph_Label = CTkLabel(Footer_labelF, text="Generate Graphs", font=("Tahoma", 35))
        Graph_Label.pack(pady=20)

        show_button_avg = CTkButton(Footer_Buttons, text="Income Graph", fg_color="#537B2E", 
                                    width=450, height=40, font=("Century Gothic", 30), command=show_graphs_plotavg)
        show_button_avg.grid(row=0, column=0, padx=30, pady=30)

        show_button_income = CTkButton(Footer_Buttons, text="Accommodation Graph", fg_color="#537B2E", 
                                    width=450, height=40, font=("Century Gothic", 30),command=show_graphs_income)
        show_button_income.grid(row=0, column=1, padx=30)

        Invisilabel = CTkLabel(UltimateFrame, text="", height=50, pady=30)
        Invisilabel.grid(row=7)
        
        Lister()

    Status()

    def MainReservation():

        root = CTk()
        root.title("Reservation window")
        root.geometry("+0+0")
        widthvar=root.winfo_screenwidth()
        heightvar=root.winfo_screenheight()

        CTk._set_appearance_mode(root, 'dark')
        windowcolor = root.cget("bg")

        Usernameref = username
        Passwordref = password
        VIPSwitchRef = user_type

        class Managers():
            def __init__(self, year, month, day, YeartoEdit, MonthtoEdit, DaytoEdit):
                self.year = year
                self.month = month
                self.day = day
                self.MonthtoEdit = MonthtoEdit
                self.DaytoEdit = DaytoEdit
                self.YeartoEdit = YeartoEdit

            def MonthManager(self, *args):
                if int(self.year.get()) == None or int(self.year.get()) < 2000:
                    self.DaytoEdit.configure(state=DISABLED)
                    self.MonthtoEdit.configure(state=DISABLED)
                else:
                    self.MonthtoEdit.configure(state=NORMAL)

            def DayManager(self, *args):
                if int(self.month.get()) == 1:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days31)
                if int(self.month.get()) == 2 and int(self.year.get())%4!=0:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=FebUnLeap)
                if int(self.month.get()) == 2 and int(self.year.get())%4==0:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=FebLeap)
                if int(self.month.get()) == 3:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days31)
                if int(self.month.get()) == 4:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days30)
                if int(self.month.get()) == 5:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days31)
                if int(self.month.get()) == 6:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days30)
                if int(self.month.get()) == 7:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days31)
                if int(self.month.get()) == 8:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days31)
                if int(self.month.get()) == 9:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days30)
                if int(self.month.get()) == 10:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days31)
                if int(self.month.get()) == 11:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days30)
                if int(self.month.get()) == 12:
                    self.DaytoEdit.configure(state=NORMAL)
                    self.DaytoEdit.configure(values=Days31)

        MegaFrame = CTkFrame(reserve, bg_color=windowcolor, fg_color="#353535", width=widthvar, height=heightvar)
        ContentFrame = CTkScrollableFrame(MegaFrame, bg_color=windowcolor, border_width=2, border_color="#353535", 
                                        fg_color="black", width=(widthvar*0.65), height=heightvar)
        ContentHeader = CTkFrame(ContentFrame, bg_color=windowcolor,  fg_color="#202124", width=(widthvar*0.62), height=100)
        CMidBody = CTkFrame(ContentFrame, bg_color="black",  fg_color="#141212", width=(widthvar*0.62))
        Offer1 = CTkFrame(CMidBody, bg_color="#153619",  fg_color="#153619")
        Offer2 = CTkFrame(CMidBody, bg_color="#475E28",  fg_color="#475E28")
        Offer3 = CTkFrame(CMidBody, bg_color="#819550",  fg_color="#819550")
        MapsFrame = CTkFrame(ContentFrame,  fg_color="#141212", width=(widthvar*0.62))
        Maps_Header = CTkFrame(MapsFrame, fg_color="#162C15")
        Maps_Buttons = CTkFrame(MapsFrame,  fg_color="#202124")
        HeaderElements = CTkFrame(ContentFrame, bg_color="transparent",  fg_color="transparent", width=600, height=100)
        UltraFrame = CTkScrollableFrame(MegaFrame, bg_color=windowcolor, border_width=2, border_color="#353535", 
                                        fg_color="#202124", width=(widthvar*0.32), height=heightvar)
        MainFrame = CTkFrame(UltraFrame, bg_color=windowcolor, fg_color="#162C15",
                            border_width=2)
        HeaderMF = CTkFrame(MainFrame, bg_color="#162C15", fg_color="#162C15")
        BodyMF = CTkFrame(MainFrame, fg_color="#162C15")
        DateManager = CTkFrame(BodyMF, fg_color="#162C15")
        DateManager2 = CTkFrame(BodyMF, fg_color="#162C15")
        TimeManager = CTkFrame(BodyMF, fg_color="#162C15")
        TimeManager2 = CTkFrame(BodyMF, fg_color="#162C15")
        PlateManager = CTkFrame(BodyMF, fg_color="#162C15")
        MidBody= CTkFrame(MainFrame, fg_color="#162C15")
        LowerBody = CTkFrame(MainFrame, fg_color="#162C15")
        PriceFrame =  CTkFrame(LowerBody, fg_color="#162C15")
        CancelFrame = CTkFrame(UltraFrame, bg_color=windowcolor, fg_color="#162C15", border_width=2)
        BlankFrame = CTkFrame(UltraFrame, bg_color="#202124", fg_color="#202124", height=100)
        CHeaderMF = CTkFrame(CancelFrame,  bg_color="#162C15", fg_color="#162C15")
        CBodyMF = CTkFrame(CancelFrame, fg_color="#162C15")
        CLowerBody = CTkFrame(CancelFrame, fg_color="#162C15", height=1000)
        
        MegaFrame.pack(fill=BOTH, expand=True)
        ContentFrame.grid()
        ContentHeader.grid(sticky=NSEW)
        ContentFrame.grid_rowconfigure(0, weight=0)
        ContentFrame.grid_columnconfigure(0, weight=1)
        HeaderElements.place(x=190, y=20)
        CMidBody.grid(column=0, row=1, sticky=NSEW)
        CMidBody.grid_rowconfigure(0, weight=1)
        CMidBody.grid_columnconfigure(0, weight=1)
        CMidBody.grid_columnconfigure(1, weight=1)
        CMidBody.grid_columnconfigure(2, weight=1)
        Offer1.grid(column=0, row=0, padx=45, pady=20, sticky=NS)
        Offer2.grid(column=1, row=0, padx=10, pady=20, sticky=NS)
        Offer3.grid(column=2, row=0, padx=50, pady=20, sticky=NS)
        MapsFrame.grid(column=0, row=2, sticky=NSEW)
        MapsFrame.columnconfigure(0, weight=1)
        Maps_Header.grid(column=0, row=0, sticky=EW)
        Maps_Header.columnconfigure(0, weight=1)
        Maps_Buttons.grid(column=0, row=1, sticky=EW)
        Maps_Buttons.columnconfigure([0,1], weight=1)
        UltraFrame.grid(column=1, row=0, pady=15, sticky=NSEW)
        UltraFrame.grid_columnconfigure(0, weight=1)
        MainFrame.grid(column=0, row=0, pady=10, sticky=EW)
        HeaderMF.pack(padx=20, pady=5)
        BodyMF.pack(padx=20, fill=X)
        DateManager.grid(column=1, row=2, sticky=W, padx=10)
        TimeManager.grid(column=1, row=3, sticky=W)
        DateManager2.grid(column=1, row=4, sticky=W, padx=10)
        TimeManager2.grid(column=1, row=5, sticky=W)
        PlateManager.grid(column=1, row=6, sticky=W)
        MidBody.pack(padx=20, pady = 5)
        LowerBody.pack(pady = 10)
        PriceFrame.grid(column=0, row=3, pady=10)
        CancelFrame.grid(column=0, row=1, pady=10, sticky=NSEW)
        CHeaderMF.grid(padx=10, pady=10)
        CBodyMF.grid(padx=10, pady=10)
        CLowerBody.grid(padx=10, pady=10)
        BlankFrame.grid(column=0, row=2, pady=10, sticky=NSEW)

        def MemberMap():
            MemberM = CTk()
            MemberM.geometry("1600x800")
            MemberM.title("Member Parking Space Layout")

            canvas = CTkCanvas(MemberM, width=1600, height=800)
            canvas.pack()

            canvas.create_text(13, 120, text="ENTRANCE", anchor="w", font=("Arial", 12, "bold"))

            canvas.create_text(1580, 750, text="EXIT", anchor="e", font=("Arial", 12, "bold"))

            def draw_hollow_rectangle(canvas, x, y, width, height, angle, fill_color, label):
                angle_rad = math.radians(angle)
                cos_theta = math.cos(angle_rad)
                sin_theta = math.sin(angle_rad)

                x0, y0 = x, y
                x1, y1 = x + width * cos_theta, y - width * sin_theta
                x2, y2 = x1 - height * sin_theta, y1 - height * cos_theta
                x3, y3 = x - height * sin_theta, y - height * cos_theta

                points = [x0, y0, x1, y1, x2, y2, x3, y3]

                canvas.create_polygon(points, outline="black", fill=fill_color, width=5)

                center_x = (x0 + x2) / 2
                center_y = (y0 + y2) / 2
                canvas.create_text(center_x, center_y, text=label, font=("Arial", 10, "bold"))

            draw_hollow_rectangle(canvas, 100, 170, 3, 80, 90, '', '')
            draw_hollow_rectangle(canvas, 100, 170, 3, 575, -170, '', '')
            draw_hollow_rectangle(canvas, 200, 733, 3, 1272, -90, '', '')
            draw_hollow_rectangle(canvas, 1475, 733, 3, 60, -125, '', '')
            draw_hollow_rectangle(canvas, 20, 60, 3, 120, -90, '', '')
            draw_hollow_rectangle(canvas, 140, 60, 3, 45, -35, '', '')
            draw_hollow_rectangle(canvas, 168, 23, 3, 1350, -90, '', '')
            draw_hollow_rectangle(canvas, 1520, 23, 3, 620, 180, '', '')
            draw_hollow_rectangle(canvas, 1518, 640, 3, 60, -125, '', '')

            draw_hollow_rectangle(canvas, 130, 230, 5, 450, -170, '', '')
            draw_hollow_rectangle(canvas, 500, 573, 5, 900, -90, '', '')
            draw_hollow_rectangle(canvas, 500, 303, 5, 900, -90, '', '')

            parking_status = [
                False, True, False, True, False,
                True, False, True, False, True,
                True, False, True, False, True,
                True, False, True, False, True,
                True, False, True, False, True
            ]

            parking_labels = [
                "A1", "A2", "A3", "A4", "A5",
                "B1", "B2", "B3", "B4", "B5",
                "C1", "C2", "C3", "C4", "C5",
                "D1", "D2", "D3", "D4", "D5",
                "E1", "E2", "E3", "E4", "E5"
            ]

            left_diagonal_coords = [(142, 280), (157, 370), (173, 460), (190, 550), (205, 640)]
            for i, (x, y) in enumerate(left_diagonal_coords):
                fill_color = 'green' if parking_status[i] else '#4B3434'
                draw_hollow_rectangle(canvas, x, y, 50, 80, -40, fill_color, parking_labels[i])

            first_row_coords = [(560, 300), (640, 300), (720, 300), (800, 300), (880, 300),
                                (1000, 300), (1080, 300), (1160, 300), (1240, 300), (1320, 300)]
            for i, (x, y) in enumerate(first_row_coords):
                fill_color = 'green' if parking_status[i + 5] else '#4B3434'
                draw_hollow_rectangle(canvas, x, y, 50, 80, 30, fill_color, parking_labels[i + 5])

            second_row_coords = [(560, 570), (640, 570), (720, 570), (800, 570), (880, 570),
                                (1000, 570), (1080, 570), (1160, 570), (1240, 570), (1320, 570)]
            for i, (x, y) in enumerate(second_row_coords):
                fill_color = 'green' if parking_status[i + 15] else '#4B3434'
                draw_hollow_rectangle(canvas, x, y, 50, 80, 30, fill_color, parking_labels[i + 15])

            MemberM.mainloop()

        def VIPMap():
            VIPM = CTk()
            VIPM.geometry("1600x800")
            VIPM.title("Parking Space Layout")

            canvas = CTkCanvas(VIPM, width=1600, height=800)
            canvas.pack()

            canvas.create_text(13, 120, text="ENTRANCE", anchor="w", font=("Arial", 12, "bold"))

            canvas.create_text(1580, 750, text="EXIT", anchor="e", font=("Arial", 12, "bold"))

            def draw_hollow_rectangle(canvas, x, y, width, height, angle, fill_color, label):
                angle_rad = math.radians(angle)
                cos_theta = math.cos(angle_rad)
                sin_theta = math.sin(angle_rad)

                x0, y0 = x, y
                x1, y1 = x + width * cos_theta, y - width * sin_theta
                x2, y2 = x1 - height * sin_theta, y1 - height * cos_theta
                x3, y3 = x - height * sin_theta, y - height * cos_theta

                points = [x0, y0, x1, y1, x2, y2, x3, y3]

                canvas.create_polygon(points, outline="black", fill=fill_color, width=3)

                center_x = (x0 + x2) / 2
                center_y = (y0 + y2) / 2
                canvas.create_text(center_x, center_y, text=label, font=("Arial", 10, "bold"))

            draw_hollow_rectangle(canvas, 100, 170, 30, 80, 90, '', '')
            draw_hollow_rectangle(canvas, 100, 170, 3, 575, -180, '', '')
            draw_hollow_rectangle(canvas, 100, 743, 3, 1373, -90, '', '')
            draw_hollow_rectangle(canvas, 1475, 743, 3, 60, -125, '', '')
            draw_hollow_rectangle(canvas, 20, 60, 3, 120, -90, '', '')
            draw_hollow_rectangle(canvas, 140, 60, 3, 45, -35, '', '')
            draw_hollow_rectangle(canvas, 168, 23, 3, 1350, -90, '', '')
            draw_hollow_rectangle(canvas, 1520, 23, 3, 620, 180, '', '')
            draw_hollow_rectangle(canvas, 1518, 640, 3, 60, -125, '', '')

            draw_hollow_rectangle(canvas, 518, 260, 5, 1000, -90, '', '')
            draw_hollow_rectangle(canvas, 516, 285, 3, 262, 0, '', '')
            draw_hollow_rectangle(canvas, 713, 285, 3, 262, 0, '', '')
            draw_hollow_rectangle(canvas, 913, 285, 3, 262, 0, '', '')
            draw_hollow_rectangle(canvas, 1113, 285, 3, 262, 0, '', '')
            draw_hollow_rectangle(canvas, 1313, 285, 3, 262, 0, '', '')

            draw_hollow_rectangle(canvas, 100, 502, 5, 1000, -90, '', '')
            draw_hollow_rectangle(canvas, 302, 480, 3, 262, 180, '', '')
            draw_hollow_rectangle(canvas, 501, 480, 3, 262, 180, '', '')
            draw_hollow_rectangle(canvas, 702, 480, 3, 262, 180, '', '')
            draw_hollow_rectangle(canvas, 901, 480, 3, 262, 180, '', '')
            draw_hollow_rectangle(canvas, 1100, 480, 3, 262, 180, '', '')

            parking_status = [
                False, True, False, True, False,
                True, False, True, False, True
            ]

            parking_labels = [
                "F1", "F2", "F3", "F4", "F5",
                "G1", "G2", "G3", "G4", "G5"
            ]

            first_row_coords = [(535, 230), (735, 230), (935, 230), (1135, 230), (1335, 230)]
            for i, (x, y) in enumerate(first_row_coords):
                fill_color = 'green' if parking_status[i] else '#4B3434'
                draw_hollow_rectangle(canvas, x, y, 160, 190, 0, fill_color, parking_labels[i])

            second_row_coords = [(120, 730), (320, 730), (520, 730), (720, 730), (920, 730)]
            for i, (x, y) in enumerate(second_row_coords):
                fill_color = 'green' if parking_status[i + 5] else '#4B3434'
                draw_hollow_rectangle(canvas, x, y, 160, 190, 0, fill_color, parking_labels[i + 5])

            VIPM.mainloop()

        HeaderLabel = CTkLabel(ContentHeader, text="", width=1000, height=190)
        Logo = CTkLabel(ContentHeader, text="", fg_color="#969696", 
                        bg_color="transparent", width=150, height=190)
        NameLogo = CTkLabel(HeaderElements, text=" Main Reservation", font=("Arial Bold", 65), text_color="White",
                            bg_color="transparent", fg_color="transparent")
        BarSep = Canvas(HeaderElements, bg="white", height=1, width=1150)
        Motto = CTkLabel(HeaderElements, text="   Securing Your Space and Comfort", font=("Arial Bold", 28), text_color="White",
                            bg_color="transparent", fg_color="transparent")
        
        OfferName1 = CTkLabel(Offer1, text="Wide Selection!", font=("Arial Black", 30), text_color="White")
        BarSep2 = Canvas(Offer1, bg="white", height=1, width=250)
        Description1 = CTkLabel(Offer1, text="Choose from a total of 25 different parking spaces!", 
                                font=("Tahoma", 28), text_color="White", wraplength=200, justify=LEFT)
        
        OfferName2 = CTkLabel(Offer2, text="Low Rates!", font=("Arial Black", 35), text_color="White")
        BarSep3 = Canvas(Offer2, bg="white", height=1, width=250)
        Description2 = CTkLabel(Offer2, text="Enjoy secured parking for a minimum of ₱6.25 per hour!", 
                                font=("Tahoma", 28), text_color="White", wraplength=250, justify=LEFT)
        
        OfferName3 = CTkLabel(Offer3, text="You're Valued!", font=("Arial Black", 35), text_color="White")
        BarSep4 = Canvas(Offer3, bg="white", height=1, width=250)
        Description3 = CTkLabel(Offer3, text="Avail membership for 10 exclusive spaces just for you!", 
                                font=("Tahoma", 28), text_color="White", wraplength=230, justify=LEFT)
        DecoyRow = CTkLabel(Offer3, text="")

        MapsLabel = CTkLabel(Maps_Header, text="View Parking Layout!", font=("Tahoma", 30), text_color="White")
        MemberButton = CTkButton(Maps_Buttons, text="See Member Parking Layout", font=("Century Gothic", 25), width=100, height=300,
                                fg_color="#4B3434", hover_color="#527F03", command=MemberMap)
        VIPButton = CTkButton(Maps_Buttons, text="See VIP Parking Layout", font=("Century Gothic", 25), width=100, height=300,
                                fg_color="#4B3434", hover_color="#527F03", command=VIPMap)

        HeaderLabel.grid(column=0, row=0)
        Logo.grid(column=0, row=0, sticky=W)
        NameLogo.grid(column=0, row=0, ipadx=0, sticky=W)
        BarSep.grid(column=0, row=1, sticky=W, pady=15)
        Motto.grid(column=0, row=2, sticky=W)
        OfferName1.grid(column=0, row=0, padx=10, pady=1)
        BarSep2.grid(column=0, row=1, pady=15, padx=10)
        Description1.grid(column=0, row=2, padx=30)
        OfferName2.grid(column=0, row=0, padx=10, pady=1)
        BarSep3.grid(column=0, row=1, pady=15)
        Description2.grid(column=0, row=2, padx=30)
        OfferName3.grid(column=0, row=0, padx=10, pady=1)
        BarSep4.grid(column=0, row=1, pady=15)
        Description3.grid(column=0, row=2, padx=30)
        DecoyRow.grid(column=0, row=3, pady=10)
        MapsLabel.grid(row=0, padx=15, pady=15, sticky=NSEW)
        MemberButton.grid(column=0, row=0, padx=15, pady=15, sticky=NSEW)
        VIPButton.grid(column=1, row=0, padx=15, pady=15, sticky=NSEW)


        class ErrorsMBX():
            def __init__(self, title, message):
                self.title = title
                self.message = message

            def MessageFunc(self):
                self = messagebox.showinfo(title=self.title, 
                            message=self.message)
                    
        TimeErrorBox = ErrorsMBX("Invalid Time Input", "Invalid Time Input. Please check your reservation dates.")
        SpaceErrorBox = ErrorsMBX("Invalid Space Input", "Invalid Space Input. Please check your reservation space.")
        ReservedBox = ErrorsMBX("Reserved Space", "Space is unavailable. Please choose another one.")
        WrongDetails = ErrorsMBX("Vehicle Not Found", "Please check if all information are correct.")
        CancelSuccess = ErrorsMBX("Cancel Successful", "Reservation successfully cancelled")
        ReserveSuccess = ErrorsMBX("Reservation Successful", "Reservation successful!")

        if VIPSwitchRef == "member":
            ParkingOptions = ["A", "B", "C", "D", "E"]
        elif VIPSwitchRef == "vip":
            ParkingOptions = ["A", "B", "C", "D", "E", "F", "G"]
        else:
            ParkingOptions = ["A", "B", "C", "D", "E"]

        SpaceOptions = ["1", "2", "3", "4", "5"]
        VehicleType = ["Sedan", "Coupe", "Sports Car", "Station Wagon", "Hatchback", "Convertible", "SUV", "Minivan",
                    "Pickup Truck"]

        DaysOptions = ["0"]
        Days31 = [str(day) for day in range(1,32)]
        Days30 = [str(day) for day in range(1,31)]
        FebUnLeap = [str(day) for day in range(1,29)]
        FebLeap = [str(day) for day in range(1,30)]

        WherePark = StringVar()
        WhereSpace = StringVar()
        WhatType = StringVar()
        SelectedYear = StringVar(value="Year")
        SelectedMonth = StringVar(value="M")
        SelectedDay = StringVar(value="D")
        ESelectedYear = StringVar(value="Year")
        ESelectedMonth = StringVar(value="M")
        ESelectedDay = StringVar(value="D")



        TitleResSys = CTkLabel(HeaderMF, text="RESERVE A PARKING SPACE!", font=("Century Gothic", 28), text_color="white",
                            fg_color=None)
        ParkOptLab = CTkLabel(BodyMF, text="In which area do you want to park?", font=("Century Gothic", 19), 
                            text_color="white")
        ParkSpaceLab = CTkLabel(BodyMF, text="Which space do you want to avail?", font=("Century Gothic", 19),
                                text_color="white")
        StartDateLab = CTkLabel(BodyMF, text="In what day is your reservation?", font=("Century Gothic", 19),
                                text_color="white")
        StartOptLab = CTkLabel(BodyMF, text="What time do you want to park?", font=("Century Gothic", 19),
                            text_color="white")
        EndDateLab = CTkLabel(BodyMF, text="When will your reservation end?", font=("Century Gothic", 19),
                            text_color="white")
        EndOptLab = CTkLabel(BodyMF, text="What time do you want to leave?", font=("Century Gothic", 19),
                            text_color="white")
        PlateLab = CTkLabel(BodyMF, text="What is your plate number?", font=("Century Gothic", 19),
                            text_color="white")
        VehicleLab = CTkLabel(BodyMF, text="What type is your vehicle?", font=("Century Gothic", 19),
                            text_color="white")
        TTimeLab = CTkLabel(LowerBody, text="Your total time of stay is: ", font=("Century Gothic", 19),
                            text_color="white")
        TPriceLab = CTkLabel(PriceFrame, text="Your total payment is: ", font=("Century Gothic", 19),
                            text_color="white")


        HourLab = StringVar(value="Hour")
        MinLab = StringVar(value="Minute")
        HourLab2 = StringVar(value="Hour")
        MinLab2 = StringVar(value="Minute")
        PlateLab2 = StringVar(value="XXX-0000")
        TotalTimeLab = StringVar()
        TotalPriceLab = StringVar()


        def Submit():
            to_input = ""
            Space = str(WherePark.get())+str(WhereSpace.get())
            Records = sq3.connect("parking.db")

            cursor = Records.cursor()
            try:
                cursor.execute('SELECT * FROM parking WHERE Area = ?', (Space,))
                tester = cursor.fetchone()[1]
                if tester == "Reserved":
                    ReservedBox.MessageFunc()
                elif tester == "Available":
                    try:
                        start_year = int(SelectedYear.get())
                        start_month = int(SelectedMonth.get())
                        start_day = int(SelectedDay.get())
                        start_hour = int(HourLab.get())
                        start_minute = int(MinLab.get())

                        end_year = int(ESelectedYear.get())
                        end_month = int(ESelectedMonth.get())
                        end_day = int(ESelectedDay.get())
                        end_hour = int(HourLab2.get())
                        end_minute = int(MinLab2.get())

                        start_time = datetime(start_year, start_month, start_day, start_hour, start_minute)
                        end_time = datetime(end_year, end_month, end_day, end_hour, end_minute)

                        time_difference = end_time - start_time
                        total_minutes = time_difference.total_seconds() / 60

                        if total_minutes < 0:
                            TimeErrorBox.MessageFunc()
                        else:
                            SubmitConfirm = messagebox.askyesno("Confirm Reservation", 
                                                                "Would you like to confirm your reservation?")
                            if SubmitConfirm:
                                rate = 50/480
                                totalprice = total_minutes*rate
                                year = total_minutes//525600
                                if year != 0:
                                    to_input = to_input + str(int(year)) + " years, "
                                months = (total_minutes%525600)//43800
                                if months != 0:
                                    to_input = to_input + str(int(months)) + " months, "
                                days = ((total_minutes%525600)%43800)//1440
                                if days != 0:
                                    to_input = to_input + str(int(days)) + " days, "
                                hours = (((total_minutes%525600)%43800)%1440)//60
                                if hours != 0:
                                    to_input = to_input + str(int(hours)) + " hours, and "
                                minutes = ((((total_minutes%525600)%43800)%1440)%3600)%60
                                to_input = to_input + str(int(minutes)) + " minutes"
                                TotalTimeLab.set(to_input)
                                TotalPriceLab.set(totalprice)

                                SDFormat = str(SelectedYear.get())+"/"+str(SelectedMonth.get())+"/"+str(SelectedDay.get())
                                STFormat = str(HourLab.get())+":"+str(MinLab.get())
                                EDFormat= str(ESelectedYear.get())+"/"+str(ESelectedMonth.get())+"/"+str(ESelectedDay.get())
                                ETFormat =  str(HourLab2.get())+":"+str(MinLab2.get())

                                global Reserver

                                Reserver = [(Space, "Reserved", PlateLab2.get(), WhatType.get(), SDFormat, STFormat,
                                            EDFormat, ETFormat, totalprice, total_minutes, Usernameref, Passwordref)]
                                
                                cursor.execute("""
                                            UPDATE parking SET 
                                            Occupancy = ?,
                                            Plate_Number =  ?,
                                                Vehicle_Type = ?,
                                                Start_Day = ?,
                                                Start_Time = ?,
                                                End_Day = ?,
                                                End_TIME = ?,
                                                Total_Price = ?,
                                                Total_Time = ?,
                                                Username = ?,
                                                Password = ?
                                            WHERE Area = ?""",
                                            (Reserver[0][1], Reserver[0][2], Reserver[0][3], Reserver[0][4], Reserver[0][5], 
                                            Reserver[0][6], Reserver[0][7], Reserver[0][8], Reserver[0][9], Reserver[0][10],
                                            Reserver[0][11], Reserver[0][0])
                                            )
                                
                                Records.commit()
                                Records.close()
                                ReserveSuccess.MessageFunc()

                            else:
                                pass
                                
                    except ValueError:
                        TimeErrorBox.MessageFunc()

            except TypeError or sq3.OperationalError or sq3.ProgrammingError:
                SpaceErrorBox.MessageFunc()
            


        ParkOpt = CTkComboBox(BodyMF, variable=WherePark, values=ParkingOptions, width=190,
                            button_color="#537b2e", border_color="#537b2e", button_hover_color="#2E522A", 
                            dropdown_fg_color="gray")
        ParkOpt.configure(height=25, font=("Century Gothic", 24))
        SpaceOpt = CTkComboBox(BodyMF, variable=WhereSpace, values=SpaceOptions, width=190, 
                            button_color="#537b2e", border_color="#537b2e", button_hover_color="#2E522A")
        SpaceOpt.configure(height=25,font=("Century Gothic", 24))
        SDateOptYear = CTkEntry(DateManager, width=60, textvariable=SelectedYear,
                                border_color="#537b2e")
        SDateOptYear.configure(font=("Century Gothic", 20))
        SDateOptMonth = ttk.Spinbox(DateManager, from_=1, to=12, textvariable=SelectedMonth, wrap=True, width=3, 
                                    state=DISABLED, font=("Century Gothic", 14))
        SDateOptDay = CTkComboBox(DateManager, variable=SelectedDay, width=70, values=DaysOptions, state=DISABLED,
                                button_color="#537b2e", border_color="#537b2e", button_hover_color="#2E522A", 
                                dropdown_fg_color="gray")
        SDateOptDay.configure(font=("Century Gothic", 20))
        StartHrOpt = ttk.Spinbox(TimeManager, from_=0, to=23, textvariable=HourLab, wrap=True, width=5, 
                                font=("Century Gothic", 14))
        StartMinOpt = ttk.Spinbox(TimeManager, from_=0, to=59, textvariable=MinLab, wrap=True, width=7, 
                                font=("Century Gothic", 14))

        EDateOptYear = CTkEntry(DateManager2, width=60, textvariable=ESelectedYear, border_color="#537b2e")
        EDateOptYear.configure(font=("Century Gothic", 20))
        EDateOptMonth = ttk.Spinbox(DateManager2, from_=1, to=22, textvariable=ESelectedMonth, wrap=True, width=3, 
                                    state=DISABLED, font=("Century Gothic", 14))
        EDateOptDay = CTkComboBox(DateManager2, variable=ESelectedDay, width=70, values=DaysOptions, state=DISABLED,
                                button_color="#537b2e", border_color="#537b2e", 
                                button_hover_color="#2E522A", dropdown_fg_color="gray")
        EDateOptDay.configure(font=("Century Gothic", 20))

        EndHrOpt = ttk.Spinbox(TimeManager2, from_=0, to=23, textvariable=HourLab2, wrap=True, width=5, 
                                font=("Century Gothic", 14))
        EndMinOpt = ttk.Spinbox(TimeManager2, from_=0, to=59, textvariable=MinLab2, wrap=True, width=7, 
                                font=("Century Gothic", 14))

        PlateOpt = CTkEntry(PlateManager, textvariable=PlateLab2, width=190, 
                            border_color="#537b2e")
        PlateOpt.configure(font=("Century Gothic", 24))

        VehicleOpt = CTkComboBox(BodyMF, variable=WhatType, values = VehicleType, width=190,
                            button_color="#537b2e", border_color="#537b2e", button_hover_color="#2E522A", 
                            dropdown_fg_color="gray")
        VehicleOpt.configure(font=("Century Gothic", 24))

        Submit = CTkButton(MidBody, text="Submit", font=("Century Gothic", 20), width=120, height=40, fg_color="#537B2E", command=Submit)

        TTimeDisplay = CTkComboBox(LowerBody, width = 550, corner_radius=35, height=40, variable=TotalTimeLab,
                                button_color="#537b2e", border_color="#537b2e",
                                state=DISABLED, text_color_disabled="white")
        TTimeDisplay.configure(font=("Century Gothic", 18))

        TPriceDisplay = CTkComboBox(PriceFrame, width = 250, variable=TotalPriceLab, height=40,
                                button_color="#537b2e", border_color="#537b2e",
                                state=DISABLED, text_color_disabled="white")
        TPriceDisplay.configure(font=("Century Gothic", 20))

        TitleResSys.grid(pady=15)
        ParkOptLab.grid(column=0, row=0, padx=10, pady=3, sticky=W)
        ParkSpaceLab.grid(column=0, row=1, padx=10, pady=3, sticky=W)
        StartDateLab.grid(column=0, row=2, padx=10, pady=3, sticky=W)
        StartOptLab.grid(column=0, row=3, padx=10, pady=3, sticky=W)
        EndDateLab.grid(column=0, row=4, padx=10, pady=3, sticky=W)
        EndOptLab.grid(column=0, row=5, padx=10, pady=3, sticky=W)
        PlateLab.grid(column=0, row=6, padx=10, pady=3, sticky=W)
        VehicleLab.grid(column=0, row=7, padx=10, pady=3, sticky=W)
        TTimeLab.grid(column=0, row=0, padx=10, pady=3, sticky=NSEW)
        TPriceLab.grid(column=0, row=0, padx=10, pady=3, sticky=NSEW)

        ParkOpt.grid(column=1, row=0, padx=15, pady=10, sticky=W)
        SpaceOpt.grid(column=1, row=1, padx=15, pady=10, sticky=W)

        SDateOptYear.grid(column=0, row=0, pady=10, padx=2)
        SDateOptMonth.grid(column=1, row=0, pady=10, padx=2)
        SDateOptDay.grid(column=2, row=0, pady=10, padx=2)
        StartHrOpt.grid(column=0, row=0, sticky=NSEW, padx=17, pady=10)
        StartMinOpt.grid(column=1, row=0, sticky=NSEW, pady=10)

        EDateOptYear.grid(column=0, row=0, pady=10)
        EDateOptMonth.grid(column=1, row=0, pady=10, padx=5)
        EDateOptDay.grid(column=2, row=0, pady=10)

        EndHrOpt.grid(column=0, row=0, sticky=NSEW, padx=17, pady=10)
        EndMinOpt.grid(column=1, row=0, sticky=W, pady=10)

        PlateOpt.grid(column=0, row=0, sticky=W, padx=11, pady=10)

        VehicleOpt.grid(column=1, row=7, pady=10, sticky=W, padx=11)

        StartingYear = Managers(SelectedYear, SelectedMonth,  SelectedDay,
                                SDateOptYear, SDateOptMonth, SDateOptDay)
        EndingYear = Managers(ESelectedYear, ESelectedMonth,  ESelectedDay,
                                EDateOptYear, EDateOptMonth, EDateOptDay)
        SelectedYear.trace(W, StartingYear.MonthManager)
        SelectedMonth.trace(W, StartingYear.DayManager)
        ESelectedYear.trace(W, EndingYear.MonthManager)
        ESelectedMonth.trace(W, EndingYear.DayManager)

        Submit.grid(pady=10)

        def Submit2():
            DeleteRecords = sq3.connect("parking.db")
            cursor2 = DeleteRecords.cursor()

            RefPlate = str(CancelPlateLabel.get())
            RefName = str(CUsernameLabel.get())
            RefPass = str(CPasswordLabel.get())

            try:
                ChPlate = cursor2.execute('SELECT * FROM parking WHERE Plate_Number = ?', (RefPlate,))
                RefPlate2 = ChPlate.fetchone()[2]
                if RefPlate2 is not None:
                    ChUserN = cursor2.execute('SELECT * FROM parking WHERE Username = ?', (RefName,))
                    RefName2 = ChUserN.fetchone()[10]
                    ChUserN2 = cursor2.execute('SELECT * FROM parking WHERE Username = ?', (RefName,))
                    RefPlate3 = ChUserN2.fetchone()[2]
                    if RefName2 is not None and RefPlate3 == RefPlate2:
                        ChPassW = cursor2.execute('SELECT * FROM parking WHERE Password = ?', (RefPass,))
                        RefPass2 = ChPassW.fetchone()[11]
                        ChPassW2 = cursor2.execute('SELECT * FROM parking WHERE Password = ?', (RefPass,))
                        RefPlate4 = ChPassW2.fetchone()[2]
                        if RefPass2 is not None and RefPlate2 == RefPlate4:
                            ConfirmC = messagebox.askyesno("Confirm Cancel", "Proceed to Cancelling Reservation?")
                            if ConfirmC:
                                cursor2.execute(""" UPDATE parking SET
                                                    Occupancy = "Available",
                                                Plate_Number = NULL,
                                                    Vehicle_Type = NULL,
                                                    Start_Day = NULL,
                                                    Start_Time = NULL,
                                                    End_Day = NULL,
                                                    End_TIME = NULL,
                                                    Total_Price = NULL,
                                                    Total_Time = NULL,
                                                    Username = NULL,
                                                    Password = NULL
                                                WHERE Plate_Number = ? AND Username = ? AND Password = ?""",
                                                (str(CancelPlateLabel.get()), str(CUsernameLabel.get()), 
                                                    str(CPasswordLabel.get()),) 
                                                    )
                                CancelSuccess.MessageFunc()
                                DeleteRecords.commit()
                                DeleteRecords.close()
                            else:
                                pass
                        else:
                            WrongDetails.MessageFunc()
                    else:
                        WrongDetails.MessageFunc()
                else:
                    WrongDetails.MessageFunc()
            except TypeError:
                WrongDetails.MessageFunc()
            
        TTimeDisplay.grid(column=0, row=1, padx=5, pady=10, sticky=NW)
        TPriceDisplay.grid(column=1, row=0, padx=5, pady=10, sticky=NW)

        CancelPlateLabel = StringVar(value="XXX-0000")
        CUsernameLabel = StringVar()
        CPasswordLabel = StringVar()

        CancelTitle = CTkLabel(CHeaderMF, text="Cancel Reservation", font=("Century Gothic", 28), text_color="white",
                            fg_color=None)
        CancelLabel = CTkLabel(CBodyMF, text="Confirm Plate number: ", 
                            font=("Century Gothic", 22), text_color="white", fg_color=None, wraplength=260,
                            justify=LEFT)
        CUserLabel = CTkLabel(CBodyMF, text="Confirm account username: ", 
                            font=("Century Gothic", 22), text_color="white", fg_color=None, wraplength=260,
                            justify=LEFT)
        CPWLabel = CTkLabel(CBodyMF, text="Confirm account password: ", 
                            font=("Century Gothic", 22), text_color="white", fg_color=None, wraplength=260,
                            justify=LEFT)

        CancelPlate = CTkEntry(CBodyMF, width=300, height=40, font=("Tahoma", 22), textvariable=CancelPlateLabel)
        CUsername = CTkEntry(CBodyMF, width=300,  height=40, font=("Tahoma", 22), textvariable=CUsernameLabel)
        CPassword = CTkEntry(CBodyMF, width=300,  height=40, font=("Tahoma", 22), textvariable=CPasswordLabel)
        CSubmit = CTkButton(CLowerBody, text="Submit", font=("Century Gothic", 20), width=120, height=40, fg_color="#537B2E", command=Submit2)

        
        CancelTitle.grid(pady=5, sticky=NSEW)
        CancelLabel.grid(column=0, row=0, padx=15, pady=15, sticky=W)
        CUserLabel.grid(column=0, row=1, padx=15, pady=15, sticky=W)
        CPWLabel.grid(column=0, row=2, padx=15, pady=15, sticky=W)
        CancelPlate.grid(column=1, row=0, padx=5, pady=15)
        CUsername.grid(column=1, row=1, padx=5, pady=15)
        CPassword.grid(column=1, row=2, padx=5, pady=15)
        CSubmit.pack(pady=15)

    MainReservation()

    root.mainloop()

LoginWindow()
