import tkinter as tk
from tkinter import messagebox
import json
import os

# File where tasks will be saved
DATA_FILE = "tasks.json"

# --- Data Management Functions ---
def load_tasks():
    """Loads tasks from the JSON file. If it doesn't exist, loads defaults."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    # Default tasks for a first-time user
    return [
        {"text": "Complete Calculus assignment", "completed": False},
        {"text": "Do Wuthering Waves daily quests", "completed": False},
        {"text": "Read up on GATE 2028 syllabus", "completed": False}
    ]

def save_tasks():
    """Saves the current list of tasks to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# --- GUI Update Functions ---
def update_listbox():
    """Clears and redraws the listbox based on the current tasks list."""
    task_listbox.delete(0, tk.END)
    for task in tasks:
        # Add a checkmark if completed, otherwise a cross
        status = "✔️ " if task["completed"] else "⭕ "
        display_text = status + task["text"]
        
        task_listbox.insert(tk.END, display_text)
        
        # Change color for completed tasks to make them look "done"
        if task["completed"]:
            task_listbox.itemconfig(tk.END, {'fg': '#a0a0a0'}) # Grayed out
        else:
            task_listbox.itemconfig(tk.END, {'fg': '#000000'}) # Normal black

# --- Action Functions ---
def add_task():
    task_text = task_entry.get().strip()
    if task_text:
        tasks.append({"text": task_text, "completed": False})
        task_entry.delete(0, tk.END) # Clear the input box
        update_listbox()
        save_tasks()
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def toggle_completed():
    try:
        index = task_listbox.curselection()[0]
        # Flip the boolean value (True becomes False, False becomes True)
        tasks[index]["completed"] = not tasks[index]["completed"]
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task from the list first.")

def delete_task():
    try:
        index = task_listbox.curselection()[0]
        del tasks[index]
        update_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task from the list first.")

# --- Application Setup ---
# 1. Initialize data
tasks = load_tasks()

# 2. Create the main window
root = tk.Tk()
root.title("Student Task Planner")
root.geometry("400x500")
root.configure(bg="#f4f7f6")
root.resizable(False, False)

# 3. Create UI Elements
# Title
title_label = tk.Label(root, text="My Task Planner", font=("Segoe UI", 18, "bold"), bg="#f4f7f6", fg="#2c3e50")
title_label.pack(pady=(20, 10))

# Input Frame (Entry + Add Button)
input_frame = tk.Frame(root, bg="#f4f7f6")
input_frame.pack(pady=10)

task_entry = tk.Entry(input_frame, width=30, font=("Segoe UI", 12))
task_entry.pack(side=tk.LEFT, padx=10)
# Allow pressing Enter to add a task
task_entry.bind('<Return>', lambda event: add_task())

add_btn = tk.Button(input_frame, text="Add", width=8, bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"), command=add_task)
add_btn.pack(side=tk.LEFT)

# Listbox for tasks
listbox_frame = tk.Frame(root)
listbox_frame.pack(pady=10)

task_listbox = tk.Listbox(listbox_frame, width=40, height=15, font=("Segoe UI", 11), selectbackground="#3498db", activestyle="none")
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Scrollbar for the listbox
scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
task_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_listbox.yview)

# Buttons Frame (Mark Done + Delete)
button_frame = tk.Frame(root, bg="#f4f7f6")
button_frame.pack(pady=10)

done_btn = tk.Button(button_frame, text="Mark Done / Undone", width=20, bg="#2ecc71", fg="white", font=("Segoe UI", 10, "bold"), command=toggle_completed)
done_btn.pack(side=tk.LEFT, padx=10)

delete_btn = tk.Button(button_frame, text="Remove", width=10, bg="#e74c3c", fg="white", font=("Segoe UI", 10, "bold"), command=delete_task)
delete_btn.pack(side=tk.LEFT, padx=10)

# 4. Populate the listbox initially and run the app
update_listbox()
root.mainloop()