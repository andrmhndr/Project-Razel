import tkinter as tk
import random
from tkinter.scrolledtext import ScrolledText

class CustomButton(tk.Button):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.config(
            font=('Arial', 12, 'bold'),
            relief=tk.GROOVE,
            bd=3,
            bg='#bada55',
            fg='#fff',
            activebackground='#8bc34a',
            activeforeground='#000'
        )

class Employee:
    def __init__(self, id, name, position, salary):
        self.id = id
        self.name = name
        self.position = position
        self.salary = salary

class EmployeeView:
    def __init__(self, master):
        self.master = master
        self.master.title("Employee Details")
        self.id_label = tk.Label(master, text="ID:")
        self.id_label.pack()
        self.name_label = tk.Label(master, text="Name:")
        self.name_label.pack()
        self.position_label = tk.Label(master, text="Position:")
        self.position_label.pack()
        self.salary_label = tk.Label(master, text="Salary:")
        self.salary_label.pack()

    def update_employee_details(self, employee):
        self.id_label.config(text="ID: " + str(employee.id))
        self.name_label.config(text="Name: " + employee.name)
        self.position_label.config(text="Position: " + employee.position)
        self.salary_label.config(text="Salary: " + str(employee.salary))

class EmployeeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.name_var = tk.StringVar()

    def set_employee_name(self, name):
        self.model.name = name
        self.view.update_employee_details(self.model)

    def get_employee_name(self):
        return self.model.name

    def update_view(self):
        self.view.update_employee_details(self.model)

    def create_view(self):
        self.name_var.set(self.model.name)
        self.name_entry = tk.Entry(self.view.master, textvariable=self.name_var)
        self.name_entry.pack()
        self.btn = CustomButton(self.view.master, text="Update", command=self.update_employee)
        self.btn.pack()

    def update_employee(self):
        self.set_employee_name(self.name_var.get())

class EmployeeStream:
    def __init__(self, master):
        self.master = master
        self.master.title("Employee Stream")
        self.text = ScrolledText(self.master, width=40, height=10)
        self.text.pack()
        self.btn = CustomButton(self.master, text="Generate", command=self.generate_employee)
        self.btn.pack()

    def add_employee_to_stream(self, employee):
        self.text.insert(tk.END, f"ID: {employee.id}\nName: {employee.name}\nPosition: {employee.position}\nSalary: {employee.salary}\n\n")

    def generate_employee(self):
        employee = Employee(random.randint(1, 100), "John Doe", "Developer", random.randint(3000, 8000))
        self.add_employee_to_stream(employee)

def main():
    root = tk.Tk()
    model = Employee(1, "John Doe", "Developer", 5000)
    view = EmployeeView(root)
    EmployeeStream(root)
    controller = EmployeeController(model, view)
    controller.create_view()
    root.mainloop()

if __name__ == '__main__':
    main()
    

# if __name__ == '__main__':
#     app = App()
#     app.mainloop()

# customtkinter.set_appearance_mode("dark")
# customtkinter.set_default_color_theme("green")

# root = customtkinter.CTk()
# root.geometry("500x350")

# def login():
#     print("test")
    
# frame = customtkinter.CTkFrame(master = root)
# frame.pack(pady=20, padx=60, fill="both", expand=True)

# label = customtkinter.CTkLabel(master = frame, text="Login System")
# label.pack(pady=12, padx=10)

# entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
# entry1.pack(pady=12, padx=10)

# entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*")
# entry2.pack(pady=12, padx=10)

# button = customtkinter.CTkButton(master = frame, text="login", command=login)
# button.pack(pady=12, padx=10)

# root.mainloop()
