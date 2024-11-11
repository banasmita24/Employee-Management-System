from customtkinter import *
from PIL import Image
from tkinter import ttk,messagebox
import database

#Functions
def delete_all():
    result=messagebox.askyesno('Confirm','Do you really want to delete all the records!?')
    if result:
        database.deleteall_records()
        treeview_data()
    else:
        pass

def show_all():
    treeview_data()
    searchEntry.delete(0,END)
    searchBox.set('Search By')

def search_employee():
    if searchEntry.get()=='':
        messagebox.showerror('Error', 'Enter value to search!!')
    elif searchBox.get()=='Search By':
        messagebox.showerror('Error', 'Please select an option!!')
    else:
        searched_data=database.search(searchBox.get(),searchEntry.get())
        tree.delete(*tree.get_children())
        for employee in searched_data:
            tree.insert('', END,values=employee)

def delete_employee():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Select data to delete!!')
    else:
        database.delete(idEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Success', 'Data is deleted!!')

def update_employee():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error','Select data to update!!')
    else:
        database.update(idEntry.get(),nameEntry.get(),phoneEntry.get(),roleBox.get(),genderBox.get(),salaryEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Success','Data is updated!!')

def selection(event):
    selected_item=tree.selection()
    if selected_item:
        row=tree.item(selected_item)['values']
        clear()
        idEntry.insert(0,row[0])
        nameEntry.insert(0,row[1])
        phoneEntry.insert(0,row[2])
        roleBox.set(row[3])
        genderBox.set(row[4])
        salaryEntry.insert(0,row[5])

def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    idEntry.delete(0,END)
    nameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    roleBox.set('Select Role')
    genderBox.set('Select Gender')
    salaryEntry.delete(0,END)

def treeview_data():
    employees=database.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('',END,values=employee)

def add_employee():
    if idEntry.get=='' or phoneEntry.get()=='' or nameEntry.get()=='' or salaryEntry.get()=='':
        messagebox.showerror('Error','All fields are required!!')
    elif database.id_exists(idEntry.get()):
        messagebox.showerror('Error', 'Id already exists!!')
    elif not idEntry.get().isnumeric():
        messagebox.showerror('Error', 'Invalid ID Format!!Id should be an integer!!')
    else:
        database.insert(idEntry.get(),nameEntry.get(),phoneEntry.get(),roleBox.get(),genderBox.get(),salaryEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Success','Data is added!!')

#GUI
window=CTk()
window.geometry('1200x600+100+100')
window.resizable(0,0)
window.title('Employee Management System')
window.configure(fg_color='#FFFFFF')

logo = CTkImage(Image.open('bg.png'), size=(1200,158))
logoLabel=CTkLabel(window,image=logo,text='')
logoLabel.grid(row=0,column=0,columnspan=2)

leftFrame=CTkFrame(window,fg_color='#FFFFFF')
leftFrame.grid(row=1,column=0)

idLabel=CTkLabel(leftFrame,text='Employee Id:',font=('Goudy Old Style',18,'bold'))
idLabel.grid(row=0,column=0,padx=20,pady=15,sticky='w')
idEntry=CTkEntry(leftFrame,font=('Goudy Old Style',18,'bold'),width=180)
idEntry.grid(row=0,column=1)

nameLabel=CTkLabel(leftFrame,text='Employee Name:',font=('Goudy Old Style',18,'bold'))
nameLabel.grid(row=1,column=0,padx=20,pady=15,sticky='w')
nameEntry=CTkEntry(leftFrame,font=('Goudy Old Style',18,'bold'),width=180)
nameEntry.grid(row=1,column=1)

phoneLabel=CTkLabel(leftFrame,text='Phone No.:',font=('Goudy Old Style',18,'bold'))
phoneLabel.grid(row=2,column=0,padx=20,pady=15,sticky='w')
phoneEntry=CTkEntry(leftFrame,font=('Goudy Old Style',18,'bold'),width=180)
phoneEntry.grid(row=2,column=1)

roleLabel=CTkLabel(leftFrame,text='Role:',font=('Goudy Old Style',18,'bold'))
roleLabel.grid(row=3,column=0,padx=20,pady=15,sticky='w')
role_options=['Web Developer','Cloud Engineer', 'Technical Writer', 'Network Engineer', 'Data Scientist', 'Business Analyst', 'IT Consultant', 'UI/UX Designer', 'DevOps Engineer']
roleBox=CTkComboBox(leftFrame,values=role_options,font=('Goudy Old Style',14),width=180,state='readonly')
roleBox.grid(row=3,column=1)
roleBox.set('Select Role')

genderLabel=CTkLabel(leftFrame,text='Gender:',font=('Goudy Old Style',18,'bold'))
genderLabel.grid(row=4,column=0,padx=20,pady=15,sticky='w')
gender_options=['Male','Female','Prefer not to say']
genderBox=CTkComboBox(leftFrame,values=gender_options,font=('Goudy Old Style',14),width=180,state='readonly')
genderBox.grid(row=4,column=1)
genderBox.set('Select Gender')

salaryLabel=CTkLabel(leftFrame,text='Salary:',font=('Goudy Old Style',18,'bold'))
salaryLabel.grid(row=5,column=0,padx=20,pady=15,sticky='w')
salaryEntry=CTkEntry(leftFrame,font=('Goudy Old Style',18,'bold'),width=180)
salaryEntry.grid(row=5,column=1)

rightFrame=CTkFrame(window)
rightFrame.grid(row=1,column=1)

search_options=['Id','Name','Phone','Role','Gender','Salary']
searchBox=CTkComboBox(rightFrame,values=search_options,font=('Goudy Old Style',14),width=180,state='readonly')
searchBox.grid(row=0,column=0)
searchBox.set('Search By')
searchEntry=CTkEntry(rightFrame,font=('Goudy Old Style',18,'bold'),width=180)
searchEntry.grid(row=0,column=1)

searchButton=CTkButton(rightFrame,text='Search',width=100,command=search_employee)
searchButton.grid(row=0,column=2)

showallButton=CTkButton(rightFrame,text='Show All',width=100,command=show_all)
showallButton.grid(row=0,column=3,pady=7)

tree=ttk.Treeview(rightFrame,height=13)
tree.grid(row=1,column=0,columnspan=4)

tree['columns']=('Emp. Id','Emp. Name','Phone no.','Role', 'Gender', 'Salary')

tree.heading('Emp. Id',text='Id')
tree.heading('Emp. Name',text='Name')
tree.heading('Phone no.',text='Phone')
tree.heading('Role',text='Role')
tree.heading('Gender',text='Gender')
tree.heading('Salary',text='Salary')

tree.config(show='headings')

tree.column('Emp. Id',width=60)
tree.column('Emp. Name',width=160)
tree.column('Phone no.',width=160)
tree.column('Role',width=160)
tree.column('Gender',width=100)
tree.column('Salary',width=100)

style=ttk.Style()
style.configure('Treeview.Heading',font=('Goudy Old Style',18,'bold'))
style.configure('Treeview',font=('Goudy Old Style',15,'bold'),rowheight=30,background='grey',foreground='white')

scrollbar=ttk.Scrollbar(rightFrame,orient=VERTICAL,command=tree.yview)
scrollbar.grid(row=1,column=4,sticky='ns')

tree.config(yscrollcommand=scrollbar.set)

buttonFrame=CTkFrame(window,fg_color='#FFFFFF')
buttonFrame.grid(row=2,column=0,columnspan=2,pady=10)

newButton=CTkButton(buttonFrame,text='New Employee',font=('Goudy Old Style',15,'bold'),width=160,corner_radius=15,command=lambda:clear(True))
newButton.grid(row=0,column=0,pady=10,padx=10)

addButton=CTkButton(buttonFrame,text='Add Employee',font=('Goudy Old Style',15,'bold'),width=160,corner_radius=15,command=add_employee)
addButton.grid(row=0,column=1,pady=10,padx=10)

updateButton=CTkButton(buttonFrame,text='Update Employee',font=('Goudy Old Style',15,'bold'),width=160,corner_radius=15,command=update_employee)
updateButton.grid(row=0,column=2,pady=10,padx=10)

deleteButton=CTkButton(buttonFrame,text='Delete Employee',font=('Goudy Old Style',15,'bold'),width=160,corner_radius=15,command=delete_employee)
deleteButton.grid(row=0,column=3,pady=10,padx=10)

deleteallButton=CTkButton(buttonFrame,text='Delete All',font=('Goudy Old Style',15,'bold'),width=160,corner_radius=15,command=delete_all)
deleteallButton.grid(row=0,column=4,pady=10,padx=10)

treeview_data()

window.bind('<ButtonRelease>',selection)

window.mainloop()