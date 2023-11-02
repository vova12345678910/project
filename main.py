import tkinter
from tkinter import ttk
import sqlite3
from database import Database
class EmployeeManagement(tkinter.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.init_ui()
        self.database = Database()
        self.view_records()

    def init_ui(self):
        toolbar = tkinter.Frame(bg="#17D2E6", bd=5)
        toolbar.pack(side=tkinter.LEFT, fill=tkinter.Y)

        self.tree = ttk.Treeview(self, columns=('ID', "Full Name", "Phone",
                                                "Email", "Salary"), height=45, show="headings")
        self.tree.column("ID", width=30, anchor=tkinter.CENTER)
        self.tree.column("Full Name", width=300, anchor=tkinter.CENTER)
        self.tree.column("Phone", width=150, anchor=tkinter.CENTER)
        self.tree.column("Email", width=150, anchor=tkinter.CENTER)
        self.tree.column("Salary", width=150, anchor=tkinter.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Full Name", text="Full Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salary", text="Salary")

        scroll = tkinter.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tkinter.LEFT)

        self.add_img = tkinter.PhotoImage(file="./img/add.png")
        btn_add = tkinter.Button(toolbar, bg="#FFFFFF", bd=0, image=self.add_img, command=self.open_add)
        btn_add.pack(side=tkinter.TOP)

        self.delete_img = tkinter.PhotoImage(file="./img/delete.png")
        btn_delete = tkinter.Button(toolbar, bg="#FFFFFF", bd=0, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tkinter.TOP, pady=5)

        self.edit_img = tkinter.PhotoImage(file="./img/edit.png")
        btn_edit = tkinter.Button(toolbar, bg="#FFFFFF", bd=0, image=self.edit_img, command=self.open_edit)
        btn_edit.pack(side=tkinter.TOP, pady=5)

        self.search_img = tkinter.PhotoImage(file="./img/search.png")
        btn_search = tkinter.Button(toolbar, bg="#FFFFFF", bd=0, image=self.search_img, command=self.open_search)
        btn_search.pack(side=tkinter.TOP, pady=5)

        self.refresh_img = tkinter.PhotoImage(file='./img/refresh.png')
        btn_refresh = tkinter.Button(toolbar, bg="#FFFFFF", bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tkinter.TOP, pady=5)

    def open_add(self):
        AddEmployeeWindow(self)

    def open_edit(self):
        selection = self.tree.selection()
        if selection:
            employee_data = self.tree.item(selection[0])['values']
            EditEmployeeWindow(self, employee_data)
        else:
            tkinter.messagebox.showwarning("Warning", "Please select an employee to edit.")

    def open_search(self):
        SearchEmployeeWindow(self)

    def records(self, full_name, phone, email, salary):
        self.database.insert_data(full_name, phone, email, salary)
        self.view_records()

    def view_records(self):
        self.database.cur.execute("SELECT * FROM employees")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.database.cur.fetchall()]

    def delete_records(self):
        for selection_time in self.tree.selection():
            self.database.cur.execute("DELETE FROM employees WHERE id = ?", (self.tree.set(selection_time, "#1"),))
        self.database.con.commit()
        self.view_records()

    def edit_records(self, id, full_name, phone, email, salary):
        self.database.cur.execute("UPDATE employees SET full_name=?, phone=?, email=?, salary=? WHERE id = ?", (full_name, phone, email, salary, id))
        self.database.con.commit()
        self.view_records()

    def search_record(self, full_name):
        full_name = ('%' + full_name + '%',)
        self.database.cur.execute("SELECT * FROM employees WHERE full_name LIKE ?", full_name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', "end", values=row) for row in self.database.cur.fetchall()]

class AddEmployeeWindow(tkinter.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.init_add_window()

    def init_add_window(self):
        self.title("Add Employee")
        self.geometry("400x300")
        self.resizable(False, False)

        label_full_name = tkinter.Label(self, text="Full Name:")
        label_full_name.place(x=50, y=50)
        label_phone = tkinter.Label(self, text="Phone:")
        label_phone.place(x=50, y=80)
        label_email = tkinter.Label(self, text="Email:")
        label_email.place(x=50, y=110)
        label_salary = tkinter.Label(self, text="Salary:")
        label_salary.place(x=50, y=140)

        self.entry_full_name = ttk.Entry(self, foreground="#2489A8")
        self.entry_full_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self, foreground="#2489A8")
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self, foreground="#2489A8")
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self, foreground="#2489A8")
        self.entry_salary.place(x=200, y=140)

        btn_cancel = ttk.Button(self, text="Cancel", command=self.destroy)
        btn_cancel.place(x=250, y=190)

        btn_confirm = ttk.Button(self, text="Confirm")
        btn_confirm.place(x=50, y=190)
        btn_confirm.bind("<Button-1>", self.add_employee)
        btn_confirm.bind("<Button-1>", lambda event: self.destroy(), add="+")

    def add_employee(self, event):
        full_name = self.entry_full_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        salary = self.entry_salary.get()
        self.master.records(full_name, phone, email, salary)
        self.destroy()

class EditEmployeeWindow(tkinter.Toplevel):
    def __init__(self, master, employee_data):
        super().__init__()
        self.master = master
        self.employee_data = employee_data
        self.init_edit_window()

    def init_edit_window(self):
        self.title("Edit Employee")
        self.geometry("400x300")
        self.resizable(False, False)

        label_full_name = tkinter.Label(self, text="Full Name:")
        label_full_name.place(x=50, y=50)
        label_phone = tkinter.Label(self, text="Phone:")
        label_phone.place(x=50, y=80)
        label_email = tkinter.Label(self, text="Email:")
        label_email.place(x=50, y=110)
        label_salary = tkinter.Label(self, text="Salary:")
        label_salary.place(x=50, y=140)

        self.entry_full_name = ttk.Entry(self, foreground="#2489A8")
        self.entry_full_name.insert(0, self.employee_data[1])
        self.entry_full_name.place(x=200, y=50)

        self.entry_phone = ttk.Entry(self, foreground="#2489A8")
        self.entry_phone.insert(0, self.employee_data[2])
        self.entry_phone.place(x=200, y=80)

        self.entry_email = ttk.Entry(self, foreground="#2489A8")
        self.entry_email.insert(0, self.employee_data[3])
        self.entry_email.place(x=200, y=110)

        self.entry_salary = ttk.Entry(self, foreground="#2489A8")
        self.entry_salary.insert(0, self.employee_data[4])
        self.entry_salary.place(x=200, y=140)

        btn_cancel = ttk.Button(self, text="Cancel", command=self.destroy)
        btn_cancel.place(x=250, y=190)

        btn_confirm = ttk.Button(self, text="Confirm")
        btn_confirm.place(x=50, y=190)
        btn_confirm.bind("<Button-1>", self.edit_employee)
        btn_confirm.bind("<Button-1>", lambda event: self.destroy(), add="+")

    def edit_employee(self, event):
        id = self.employee_data[0]
        full_name = self.entry_full_name.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()
        salary = self.entry_salary.get()
        self.master.edit_records(id, full_name, phone, email, salary)
        self.destroy()

class SearchEmployeeWindow(tkinter.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.init_search_window()

    def init_search_window(self):
        self.title("Search Employee")
        self.geometry('400x300')
        self.resizable(False, False)

        label_search = tkinter.Label(self, text="Search:")
        label_search.place(x=90, y=100)

        self.entry_search = ttk.Entry(self, foreground="#2489A8")
        self.entry_search.place(x=135, y=100, width=150)

        btn_cancel = ttk.Button(self, text="Cancel", command=self.destroy)
        btn_cancel.place(x=220, y=160)

        btn_search = ttk.Button(self, text="Search")
        btn_search.place(x=85, y=160)
        btn_search.bind("<Button-1>", self.search_employee)
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")

    def search_employee(self, event):
        full_name = self.entry_search.get()
        self.master.search_record(full_name)
        self.destroy()


class Database:
    def __init__(self):
        self.con = sqlite3.connect("employee_db.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, full_name TEXT, phone TEXT, email TEXT, salary INTEGER)")
        self.con.commit()

    def insert_data(self, full_name, phone, email, salary):
        self.cur.execute("INSERT INTO employees (full_name, phone, email, salary) VALUES (?, ?, ?, ?)", (full_name, phone, email, salary))
        self.con.commit()

if __name__ == "__main__":
    root = tkinter.Tk()
    app = EmployeeManagement(root)
    app.pack()

    root.title("Company Employee List")
    root.geometry("900x700")
    root.mainloop()
