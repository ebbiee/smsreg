import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import sqlite3

#creating the universal font variables
headlaabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

#connecting to the database where all information would be stored
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()

connector.execute("CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT(STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, MatricNo TEXT)")

#creating the functions 
def reset_fields():
  global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, MatricNo_strvar

  for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'MatricNo_strvar']:
    exec(f"{i}.set('')")
  dob.set_date(datetime.datetime.now().date())

def reset_form():
    global tree
    tree.delete(*tree.get_children())

    reset_fields()

def display_records():
   tree.delete(*tree.get_children())

   curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
   data = curr.fetchall()

   for records in data:
      tree.insert('', END, values=records)

def add_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, MatricNo_strvar

   name = name_strvar.get()
   email = email_strvar.get()
   contact = contact_strvar.get()
   gender = gender_strvar.get()
   DOB = dob.get_date()
   MatricNo = MatricNo_strvar.get()

   if not name or not email or not contact or not gender or not DOB or not MatricNo:
      mb.showerror("Error!", "please fill all the missing fields!!")
   else:
      try: 
         connector.execute(
            "INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, MatricNo) VALUES (?,?,?,?,?,?)", (name, email, contact,gender,DOB, MatricNo)
         )
         connector.commit()
         mb.showinfo("Record added", f"Record of {name} was successfully added")
         reset_fields()
         display_records()
      except:
         mb.showerror("wrong type", "The type of values entered is not accurate. Please note that the contac field can only contain numbers")

def remove_record():
   if not tree.selection():
      mb.showerror("Error", " please select an item from the database")
   else:
      current_item = tree.focus()
      values = tree.item(current_item)
      selection = values["values"]

      tree.delete(current_item)
      connector.execute("DELETE FROM SCHOOL MANAGEMENT WHERE STUDENT_ID=?" , (selection[0],))
      connector.commit()

      mb.showerror("Done, the record has been successfully deleted")

      display_records()

def view_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, MatricNo_strvar
   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]

   date = datetime.date(int(selection[5][:4]), int(selection[50][5:7]), int(selection[5][8:]))

   name_strvar.set(selection[1]); email_strvar.set(selection[2]); contact_strvar.set(selection[3]);  gender_strvar.set(selection[4])
   dob.set_date(date); MatricNo_strvar.set(selection[6])


   
#initializing the gui window
window = Tk()
window.title("Redeemers university school management system (Fabunmi Ebenezer)")
window.geometry("1000x600")
window.resizable(False, False)
#changing the image icon of the app
icon_path = '../sms/schoollogo.png'
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)
window.iconphoto(False, icon_photo)
#create bg and color variables
#let frame(Lf)
lf_bg = "MidnightBlue"
#center frame(cf)
cf_bg = "AntiqueWhite"

#creating the string vaiales or intvar variabls
name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
MatricNo_strvar = StringVar()

#placing the components in the main window
Label(window, text="SCHOOL MANAGEMENT SYSTEM", font=headlaabelfont, bg='GoldenRod3').pack(side=TOP, fill=X)

left_frame = Frame(window, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(window, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(window, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

#placing the components in the left frame
Label(left_frame, text="Name", font=labelfont, bg=lf_bg, fg='LightCyan').place(relx=0.4, rely=0.05)
Label(left_frame, text="Email", font=labelfont, bg=lf_bg, fg='LightCyan').place(relx=0.4, rely=0.18)
Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg, fg='LightCyan').place(relx=0.175, rely=0.31)
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg, fg='LightCyan').place(relx=0.3, rely=0.44)
Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg=lf_bg, fg='LightCyan').place(relx=0.1, rely=0.57)
Label(left_frame, text="MatricNo", font=labelfont, bg=lf_bg, fg='LightCyan').place(relx=0.3, rely=0.7)


Entry(left_frame, width=19, textvariable=name_strvar,font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.23)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.36)
Entry(left_frame, width=19, textvariable=MatricNo_strvar, font=entryfont).place(x=20, rely=0.75)

OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.49, relwidth=0.5)

dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.62)


Button(left_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete Database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)


# Placing components in the right frame
Label(right_frame, text='Students Records', font=headlaabelfont, bg='MidnightBlue', fg='LightCyan').pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,columns=("Student ID", "Name", "Email Address", "Contact Number", "Gender", "Date of Birth", "Matric Number"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Matric Number', text='Matric No', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

window.update()
window.mainloop()