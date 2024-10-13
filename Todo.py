import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import Toplevel, Label, Entry, Button
from datetime import datetime, timedelta
import json
import os
import threading
import time

class TaskDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, task=None):
        self.task = task or {}
        super().__init__(parent, title)

    def body(self, master):
        self.name_label = Label(master, text="Task Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = Entry(master)
        self.name_entry.grid(row=0, column=1)
        self.name_entry.insert(0, self.task.get("name", ""))

        self.date_label = Label(master, text="Due Date (YYYY-MM-DD):")
        self.date_label.grid(row=1, column=0)
        self.date_entry = Entry(master)
        self.date_entry.grid(row=1, column=1)

       # Handle missing or malformed due_datetime
        due_datetime = self.task.get("due_datetime", "")
        if due_datetime:
            parts = due_datetime.split()
            self.date_entry.insert(0, parts[0] if len(parts) > 0 else "")
            # Ensure time_entry is defined
            self.time_entry = Entry(master)
            self.time_entry.grid(row=2, column=1)
            self.time_entry.insert(0, parts[1] if len(parts) > 1 else "")
        else:
            self.date_entry.insert(0, "")
            # Ensure time_entry is defined
            self.time_entry = Entry(master)
            self.time_entry.grid(row=2, column=1)
            self.time_entry.insert(0, "")

        self.time_label = Label(master, text="Due Time (HH:MM):")
        self.time_label.grid(row=2, column=0)
    
        self.priority_label = Label(master, text="Priority (High, Medium, Low):")
        self.priority_label.grid(row=3, column=0)
        self.priority_entry = Entry(master)
        self.priority_entry.grid(row=3, column=1)
        self.priority_entry.insert(0, self.task.get("priority", "Medium"))

        self.creator_label = Label(master, text="Creator:")
        self.creator_label.grid(row=4, column=0)
        self.creator_entry = Entry(master)
        self.creator_entry.grid(row=4, column=1)
        self.creator_entry.insert(0, self.task.get("creator", ""))

        self.assignee_label = Label(master, text="Assignee:")
        self.assignee_label.grid(row=5, column=0)
        self.assignee_entry = Entry(master)
        self.assignee_entry.grid(row=5, column=1)
        self.assignee_entry.insert(0, self.task.get("assignee", ""))

        self.description_label = Label(master, text="Description:")
        self.description_label.grid(row=6, column=0)
        self.description_entry = Entry(master)
        self.description_entry.grid(row=6, column=1)
        self.description_entry.insert(0, self.task.get("description", ""))

        return self.name_entry

    def validate(self):
        self.result = {
            "name": self.name_entry.get(),
            "due_datetime": f"{self.date_entry.get()} {self.time_entry.get()}",
            "priority": self.priority_entry.get(),
            "creator": self.creator_entry.get(),
            "assignee": self.assignee_entry.get(),
            "description": self.description_entry.get(),
            "completed": self.task.get("completed", False)
        }
        return True

    def apply(self):
        self.task.update(self.result)

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("450x700")
        self.tasks = []
        self.root.config(bg="white")
        self.search_var = tk.StringVar()

        # Dark mode variable
        self.dark_mode = False

        # Create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.config(bg="white")

        # Create the canvas
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)

        # Add a scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Create the buttons frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill="x")

        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, fill="x", expand=True)

        self.remove_button = tk.Button(self.button_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(side=tk.LEFT, fill="x", expand=True)

        self.complete_button = tk.Button(self.button_frame, text="Mark Completed", command=self.complete_task)
        self.complete_button.pack(side=tk.LEFT, fill="x", expand=True)

        self.edit_button = tk.Button(self.button_frame, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(side=tk.LEFT, fill="x", expand=True)

        self.search_toggle_frame = tk.Frame(self.root)
        self.search_toggle_frame.pack(fill="x")

        self.search_entry = tk.Entry(self.search_toggle_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill="x", expand=True)
        self.search_var.trace("w", self.update_displayed_tasks)

        # self.dark_mode_button = tk.Button(self.search_toggle_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        # self.dark_mode_button.pack(side=tk.LEFT, fill="x", expand=True)

        self.load_tasks()
        self.start_notification_thread()

        # Bind to root click events to deselect task
        self.root.bind("<Button-1>", self.deselect_task)

    def add_task(self):
        task_dialog = TaskDialog(self.root, title="Add Task")
        if task_dialog.result:
            task = task_dialog.result
            self.tasks.append(task)
            self.display_task(task, index=len(self.tasks)-1)
            self.save_tasks()

    def validate_datetime(self, date_str, time_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    def remove_task(self):
        selected_task = self.get_selected_task()
        if selected_task:
            self.tasks.remove(selected_task)
            self.update_displayed_tasks()
            self.save_tasks()

    def complete_task(self):
        selected_task = self.get_selected_task()
        if selected_task:
            selected_task["completed"] = True
            self.update_displayed_tasks()
            self.save_tasks()

    def edit_task(self):
        selected_task = self.get_selected_task()
        if selected_task:
            task_dialog = TaskDialog(self.root, title="Edit Task", task=selected_task)
            if task_dialog.result:
                self.update_displayed_tasks()
                self.save_tasks()

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
                self.update_displayed_tasks()

    def display_task(self, task, index=None):
        row = index // 2
        col = index % 2
        task_frame = tk.Frame(self.scrollable_frame, bd=20, relief="groove", width=500)
        task_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        self.scrollable_frame.grid_columnconfigure(col, weight=1)
        self.scrollable_frame.grid_rowconfigure(row, weight=1)

        task_name = tk.Label(task_frame, text=task["name"], font=("Arial", 14, "bold"), width=20, anchor="w")
        task_due = tk.Label(task_frame, text=f"Due: {task['due_datetime']}", font=("Arial", 10), width=20, anchor="w")
        task_priority = tk.Label(task_frame, text=f"Priority: {task['priority']}", font=("Arial", 10), width=20, anchor="w")
        task_creator = tk.Label(task_frame, text=f"Creator: {task['creator']}", font=("Arial", 10), width=20, anchor="w")
        task_assignee = tk.Label(task_frame, text=f"Assignee: {task['assignee']}", font=("Arial", 10), width=20, anchor="w")
        task_description = tk.Label(task_frame, text=f"Description: {task['description']}", font=("Arial", 10), width=20, anchor="w")
        task_status = tk.Label(task_frame, text="Completed" if task["completed"] else "Not Completed", font=("Arial", 10), width=20, anchor="w")

    # Pack labels with the same width

        task_name.pack(fill="x")
        task_due.pack(fill="x")
        task_priority.pack(fill="x")
        task_creator.pack(fill="x")
        task_assignee.pack(fill="x")
        task_description.pack(fill="x")
        task_status.pack(fill="x")

        bg_color, fg_color = self.get_task_colors(task)
        task_frame.config(bg=bg_color)
        for widget in task_frame.winfo_children():
            widget.config(bg=bg_color, fg=fg_color)

        task_frame.bind("<Button-1>", lambda e: self.on_task_click(task_frame, task))
        task_name.bind("<Button-1>", lambda e: self.on_task_click(task_frame, task))
        task_due.bind("<Button-1>", lambda e: self.on_task_click(task_frame, task))
        task_priority.bind("<Button-1>", lambda e: self.on_task_click(task_frame, task))
        task_creator.bind("<Button-1>", lambda e: self.on_task_click(task_frame, task))
        task_assignee.bind("<Button-1>", lambda e: self.on_task_click(task_frame, task))
        task_description.bind("<Button-1>", lambda e: self.on_task_click(task_frame, task))
        task_status.bind("<Button-1>", lambda e: self.on_task_click(task_frame, task))

    def get_task_colors(self, task):
        if task["completed"]:
            return 'lightgreen', 'gray'
        else:
            due_datetime = None
            if task["due_datetime"]:
                try:
                    due_datetime = datetime.strptime(task["due_datetime"], "%Y-%m-%d %H:%M")
                except ValueError:
                    print(f"Error parsing date-time: {task['due_datetime']}")

            if due_datetime:
                if due_datetime < datetime.now():
                    return 'red', 'white'
                elif due_datetime.date() == datetime.now().date():
                    return 'yellow', 'black'

            if task["priority"] == "High":
                return 'pink', 'black'
            elif task["priority"] == "Medium":
                return 'lightblue', 'black'
            elif task["priority"] == "Low":
                return 'lightgray', 'black'

            return 'white', 'black'

    def update_displayed_tasks(self, *args):
        search_term = self.search_var.get().lower()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for i, task in enumerate(self.tasks):
            if search_term in task["name"].lower():
                self.display_task(task, index=i)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.root.config(bg="black")
            self.main_frame.config(bg="black")
            self.button_frame.config(bg="black")
            self.search_toggle_frame.config(bg="black")
            self.canvas.config(bg="black")
            for task_frame in self.scrollable_frame.winfo_children():
                bg_color, fg_color = self.get_task_colors(self.tasks[self.scrollable_frame.winfo_children().index(task_frame)])
                task_frame.config(bg=bg_color)
                for widget in task_frame.winfo_children():
                    widget.config(bg=bg_color, fg=fg_color)
        else:
            self.root.config(bg="white")
            self.main_frame.config(bg="white")
            self.button_frame.config(bg="white")
            self.search_toggle_frame.config(bg="white")
            self.canvas.config(bg="white")
            for task_frame in self.scrollable_frame.winfo_children():
                bg_color, fg_color = self.get_task_colors(self.tasks[self.scrollable_frame.winfo_children().index(task_frame)])
                task_frame.config(bg=bg_color)
                for widget in task_frame.winfo_children():
                    widget.config(bg=bg_color, fg=fg_color)

    def on_task_click(self, frame, task):
            if hasattr(self, 'selected_frame'):
                try:
                    self.selected_frame.config(relief="groove")
                except tk.TclError:
                    # The selected_frame no longer exists
                    pass
            self.selected_task = task
            self.selected_frame = frame
            frame.config(relief="sunken")
            # Prevent root click event from firing
            return "break"


    def get_selected_task(self):
        if hasattr(self, 'selected_task'):
            return self.selected_task
        else:
            messagebox.showerror("No Task Selected", "Please select a task first.")
            return None

    def start_notification_thread(self):
        self.check_notifications()

        # Start the periodic notification thread
        notification_thread = threading.Thread(target=self.notification_loop)
        notification_thread.daemon = True
        notification_thread.start()
    def check_notifications(self):
        now = datetime.now()
        for task in self.tasks:
            if not task["completed"] and task["due_datetime"]:
                try:
                    due_datetime = datetime.strptime(task["due_datetime"], "%Y-%m-%d %H:%M")
                    if now >= due_datetime - timedelta(minutes=30) and now < due_datetime:
                        self.show_notification(task)
                except ValueError:
                    print(f"Error parsing date-time: {task['due_datetime']}")


    def notification_loop(self):
        while True:
            # Check for notifications every 30 minutes
            self.check_notifications()
            time.sleep(1800)
        

    def show_notification(self, task):
        messagebox.showinfo("Task Reminder", f"Task '{task['name']}' is due soon!")

    def deselect_task(self, event):
        if event.widget != self.root:
            return
        if hasattr(self, 'selected_frame'):
            self.selected_frame.config(relief="groove")
            del self.selected_task
            del self.selected_frame

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
