
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt
import csv
import matplotlib.pyplot as plt
from collections import Counter

# Root window setup
root = tk.Tk()
root.title("Gym Management System Form")
root.state("zoomed")  
root.config(bg="#F0F0F0")

def update_datetime():
    current_date = datetime.now().strftime("%d %B %Y")  
    current_time = datetime.now().strftime("%H:%M:%S")  
    date_label.config(text=f"Date: {current_date}")
    time_label.config(text=f"Time: {current_time}")
    time_label.after(1000, update_datetime)

# Header frame
header_frame = tk.Frame(root, bg="#003366", height=80)
header_frame.pack(fill="x")

tk.Label(header_frame, text="Gym Management System", font=("Arial", 20, "bold"), fg="white", bg="#003366").pack(pady=20)
clock_label = tk.Label(header_frame, font=("Arial", 12), fg="white", bg="#003366")
clock_label.place(relx=0.95, rely=0.2, anchor="ne")


date_label = tk.Label(header_frame, font=("Arial", 12), fg="white", bg="#003366")
date_label.place(relx=0.85, rely=0.1, anchor="ne")

time_label = tk.Label(header_frame, font=("Arial", 12), fg="white", bg="#003366")
time_label.place(relx=0.85, rely=0.5, anchor="ne")
update_datetime()

# Scrollable frame setup
canvas = tk.Canvas(root, bg="#DDE6F1")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Form fields
entries = []
combo_fields = []


# Function to add form fields dynamically
def add_field(label_text, var_type="entry", values=None, column_count=3):
    total_fields = len(entries) + len(combo_fields)
    row = total_fields // column_count
    col = total_fields % column_count
    tk.Label(scrollable_frame, text=label_text, font=("Arial", 12), bg="#DDE6F1").grid(row=row, column=col * 2, padx=10, pady=5, sticky="e")
    if var_type == "entry":
        entry = tk.Entry(scrollable_frame, width=25)
        entry.grid(row=row, column=col * 2 + 1, padx=10, pady=5, sticky="w")
        entries.append(entry)
        return entry
    elif var_type == "combo":
        var = tk.StringVar()
        combo = ttk.Combobox(scrollable_frame, textvariable=var, values=values, state="readonly", width=23)
        combo.grid(row=row, column=col * 2 + 1, padx=10, pady=5, sticky="w")
        combo_fields.append(combo)
        return combo
    elif var_type == "date":
        date_entry = DateEntry(scrollable_frame, width=22, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        date_entry.grid(row=row, column=col * 2 + 1, padx=10, pady=5, sticky="w")
        entries.append(date_entry)
        return date_entry

# Adding form fields
name_entry = add_field("Name")
email_entry = add_field("Email")
health_status_var = add_field("Health Status", var_type="combo", values=["Good", "Average", "Bad"])
location_var = add_field("Gym Location", var_type="combo", values=["Downtown", "Uptown", "Suburb"])
workoutzone_var = add_field("Workout Zone", var_type="combo", values=["Cardio", "Strength", "HIIT"])
member_id_entry = add_field("Member ID")
appointment_id_entry = add_field("Appointment ID")
trainer_id_entry = add_field("Trainer ID")
appointment_date_entry = add_field("Appointment Date", var_type="date")
appointment_time_var = add_field("Appointment Time", var_type="combo", values=["Morning", "Afternoon", "Evening"])
staff_var = add_field("Staff Name")
attendance_var = add_field("Attendance", var_type="combo", values=["Present", "Absent"])
payment_var = add_field("Payment Status", var_type="combo", values=["Paid", "Unpaid"])
class_schedule_entry = add_field("Class Schedule", var_type="date")
membership_type_var = add_field("Membership Type", var_type="combo", values=["Standard", "Premium", "VIP"])
subscription_start_entry = add_field("Subscription Start Date", var_type="date")
subscription_end_entry = add_field("Subscription End Date", var_type="date")
appointment_type_var = add_field("Appointment Type", var_type="combo", values=["Consultation", "Training", "Evaluation"])
status_var = add_field("Status", var_type="combo", values=["Active", "Inactive", "Suspended"])



# Start the Tkinter loop
if __name__ == "__main__":
    root.mainloop()