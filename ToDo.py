import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from customtkinter import *
import csv
import os


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('To Do App')
        self.iconbitmap('iicon.ico')

        my_width = self.winfo_screenwidth()
        my_height = self.winfo_screenheight()

        x = (my_width/2) - 150
        y = (my_height/2) - 225

        self.geometry(f'300x450+{int(x)}+{int(y)}')
        self.resizable(False, False)
        self.tables()

    def tables(self):
        self.table = ttk.Treeview(self, columns='first', show='headings')
        self.table.heading('first', text='To Do Activities', anchor=tk.CENTER)
        self.table.bind('<<TreeviewSelect>>', self.selects)

        self.table.pack()

        self.entry = CTkEntry(self,
                              font=('Times new roman', 15),
                              fg_color='white',
                              text_color='black',
                              corner_radius=15,
                              width=190)
        self.entry.pack(pady=10)

        self.add_task = CTkButton(self,
                                  text=('Add Task'),
                                  font=('Times new roman', 15),
                                  corner_radius=10,
                                  command=self.add_tasks)
        self.add_task.pack(pady=5)

        self.done_task = CTkButton(self,
                                   text=('Done Task'),
                                   font=('Times new roman', 15),
                                   corner_radius=10,
                                   command=self.done_task)
        self.done_task.pack(pady=5)

        self.close = CTkButton(self,
                               text=('Exit'),
                               font=('Times new roman', 15),
                               corner_radius=10,
                               command=self.exit_main)
        self.close.pack(pady=5)

        self.created = CTkLabel(self, text='Created by JOHNPAUL MARTIREZ', font=('Times new roman', 11), text_color='black')
        self.created.pack(pady=15)

        self.view()

    def exit_main(self):
        sys.exit()

    def add_tasks(self):
        task = self.entry.get().title()
        lists = [task]

        if task == '':
            messagebox.showerror('Error', 'Please input tasks')
        else:
            with open('activities.csv', 'a', newline='') as files:
                writers = csv.writer(files)
                writers.writerow(lists)
                files.close()

            self.entry.delete(0, tk.END)

            self.table.insert(parent='', index=tk.END, values=lists)

    def view(self):
        for item in self.table.get_children():
            self.table.delete(item)

        with open('activities.csv') as read_file:
            reader = csv.reader(read_file)
            next(reader)

            for i in reader:
                self.table.insert(parent='', index=tk.END, values=i)

        read_file.close()

    def selects(self, _):
        pass

    def done_task(self):
        selected_items = self.table.selection()
        if selected_items:
            activity = self.table.item(selected_items)['values']

            with open('activities.csv', 'r', newline='') as del_file:
                reader = csv.reader(del_file)
                data = list(reader)

            for sets in data:
                if sets == activity:
                    data.remove(sets)
                    data.remove(['Activities'])

                with open('activities.csv', 'w', newline='') as new_file:
                    writer = csv.DictWriter(new_file, fieldnames=['Activities'])
                    writer.writeheader()

                    for i in data:
                        writer.writerow({'Activities': i[0]})

            del_file.close()
            new_file.close()
            self.view()


        else:
            messagebox.showerror('Error', 'Please select one!')


if __name__ == '__main__':
    if not os.path.exists('activities.csv'):
        with open('activities.csv', 'w', newline='') as file:
            fieldnames = ['Activities']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            file.close()

        app = Main()
        app.mainloop()

    else:
        app = Main()
        app.mainloop()
