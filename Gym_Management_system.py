from tkinter import Tk, Frame, Button, Label, Entry, messagebox, ttk, Scrollbar
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE_PATH = "gym_management.csv"

SCHEMA = {
    
    "Member": [
        "Member_ID", "Name", "Email", "Health_Status", "Gym_Location", 
        "Workout_Zone", "Join_Date", "Membership_Type", "Subscription_Start", "Subscription_End"
    ],
    "Attendance": ["Attendance_ID", "Member_ID", "Class_ID", "Date_Time", "Attendance"],
    "Gym_Location": ["Location_ID", "Name", "Address", "Phone"],
    "Workout_Zone": ["Zone_ID", "Location_ID", "Name", "Type"],
    "Payment": ["Payment_ID", "Member_ID", "Amount", "Date", "Method"],
    "Appointment": ["Appointment_ID", "Member_ID", "Trainer_ID", "Type", "Date_Time"],
    "Staff": ["Staff_ID", "Name", "Role", "Zone_ID"],
}

DATE_FIELDS = ["Join_Date", "Subscription_Start", "Subscription_End", "Date", "Date_Time"]
member_data = {}

def validate_unique_entries(table_name, data):
    """
    Validate that certain fields (e.g., Member_ID, Email) are unique within the table.
    Returns a tuple (True/False, field_name) indicating whether the data is valid.
    """
    unique_fields = ["Member_ID", "Email", "Phone", "Appointment_ID"]
    if table_name == "Appointment":
        unique_fields.append("Appointment_ID")

    try:
        with open(FILE_PATH, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == table_name:
                    for idx, field in enumerate(SCHEMA[table_name]):
                        if field in unique_fields and row[idx + 1] == data[idx]:
                            return False, field
    except Exception:
        pass
    return True, ""


def initialize_csv():
    """
    Initialize the CSV file if it does not exist.
    Creates the file and writes the header row.
    """
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Table"] + ["Field"] * 10)


def get_foreign_key_options(table_name, foreign_key):
    """
    Retrieve options for a foreign key field by reading related entries from the CSV file.
    Returns a list of options for the foreign key.
    """
    options = []
    try:
        with open(FILE_PATH, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == foreign_key:
                    options.append(row[1])
    except Exception:
        pass
    return options

def create_date_picker(parent, field):
    """
    reates a date picker widget for selecting or displaying the current date.

    Parameters:
        parent (tk.Widget): The parent widget to attach the date picker.
        field (str): The name of the field for which the date picker is created.

    Returns:
        ttk.Combobox: A combobox pre-filled with the current date.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_combobox = ttk.Combobox(parent, values=[current_date], state="readonly")
    date_combobox.set(current_date)
    return date_combobox

def populate_fields_with_member_data(member_id):
    """
    Populates global member data with records corresponding to a given Member ID.

    Parameters:
        member_id (str): The ID of the member whose data needs to be fetched.

    Returns:
        None
    """
    global member_data
    member_data = {table: [] for table in SCHEMA.keys()}

    with open(FILE_PATH, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] in SCHEMA.keys() and row[1] == member_id:
                member_data[row[0]].append(row[1:])

def validate_unique_entries(table_name, data):
    """
    Validates the uniqueness of specific fields (e.g., Member_ID, Email) in the table.

    Parameters:
        table_name (str): The name of the table being validated.
        data (list): The data row to check for uniqueness.

    Returns:
        tuple:
            - bool: True if the data is valid, False otherwise.
            - str: The name of the field causing the validation failure (if any).
    """
    unique_fields = ["Member_ID", "Email", "Phone", "Appointment_ID"]
    if table_name == "Appointment":
        unique_fields.append("Appointment_ID")
    
    try:
        with open(FILE_PATH, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == table_name:
                    for idx, field in enumerate(SCHEMA[table_name]):
                        if field in unique_fields and row[idx + 1] == data[idx]:
                            return False, field
    except Exception:
        pass
    return True, ""
def open_crud_window(table_name):
    """
    Opens a CRUD (Create, Read, Update, Delete) window for the specified table.

    Parameters:
        table_name (str): The name of the table for which the CRUD window is opened.

    Returns:
        None
    """
    for widget in right_frame.winfo_children():
        widget.destroy()

    fields = SCHEMA[table_name]
    member_info = member_data.get(table_name, [])

    def load_data():
        """
        Loads the data into the tree view widget.
        """
        tree.delete(*tree.get_children())
        for record in member_info:
            tree.insert("", "end", values=record)

    def clear_fields():
        """
        Clears all input fields in the form.
        """
        for entry in entries:
            entry.set("") if isinstance(entry, ttk.Combobox) else entry.delete(0, 'end')

    def add_record():
        """
        Adds a new record to the table.
        """
        data = []
        for field, entry in zip(fields, entries):
            if isinstance(entry, ttk.Combobox):
                data.append(entry.get())
            else:
                data.append(entry.get())

        if "" in data:
            messagebox.showwarning("Warning", "All fields must be filled.")
            return

        # Validate member ID for Attendance table
        if table_name == "Attendance":
            member_id = data[1]
            with open(FILE_PATH, mode="r") as file:
                reader = csv.reader(file)
                member_exists = False
                for row in reader:
                    if row[0] == "Member" and row[1] == member_id:
                        member_exists = True
                        break
                if not member_exists:
                    messagebox.showwarning("Warning", "Invalid Member ID. This member does not exist in the gym.")
                    return
            data[3] = datetime.now().strftime("%H:%M:%S")

        try:
            with open(FILE_PATH, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([table_name] + data)
            populate_fields_with_member_data(data[0])  # Refresh member data
            load_data()
            messagebox.showinfo("Success", "Record added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add record: {str(e)}")

    def update_record():
        """
        Updates an existing record in the table.
        """
        member_id = member_id.get()  # Get the member_id from the entry
        updated_data = [entry.get() for entry in entries]  # Get updated data from entries
        if "" in updated_data:
            messagebox.showwarning("Warning", "All fields must be filled.")
            return

        try:
            rows = []
            with open(FILE_PATH, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == table_name and row[1] == member_id:
                        rows.append([table_name] + updated_data)
                    else:
                        rows.append(row)
            with open(FILE_PATH, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            populate_fields_with_member_data(member_id)  # Refresh member data with member_id
            load_data()
            messagebox.showinfo("Success", "Record updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update record: {str(e)}")



    entries = []
    for i, field in enumerate(fields):
        ttk.Label(right_frame, text=field).grid(row=i, column=0, padx=5, pady=5)
        if field.endswith("_ID") and field != fields[0]:
            foreign_table = [key for key in SCHEMA if field.startswith(key[:-1])]
            if foreign_table:
                options = get_foreign_key_options(table_name, foreign_table[0])
                combobox = ttk.Combobox(right_frame, values=options)
                combobox.grid(row=i, column=1, padx=5, pady=5)
                if member_info:
                    combobox.set(member_info[0][i])
                entries.append(combobox)
                continue
        if field in DATE_FIELDS:
            combobox = create_date_picker(right_frame, field)
            combobox.grid(row=i, column=1, padx=5, pady=5)
            if member_info:
                combobox.set(member_info[0][i])
            entries.append(combobox)
            continue
        entry = ttk.Entry(right_frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        if member_info:
            entry.insert(0, member_info[0][i])
        entries.append(entry)

    ttk.Button(right_frame, text="Add", command=add_record).grid(row=len(entries), column=0, pady=10)
    ttk.Button(right_frame, text="Update", command=update_record).grid(row=len(entries), column=1, pady=10)
    ttk.Button(right_frame, text="Clear", command=clear_fields).grid(row=len(entries), column=3, pady=10)

    tree = ttk.Treeview(right_frame, columns=fields, show="headings")
    for field in fields:
        tree.heading(field, text=field)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    x_scrollbar = Scrollbar(right_frame, orient="horizontal", command=tree.xview)
    x_scrollbar.pack(side="bottom", fill="x")
    y_scrollbar = Scrollbar(right_frame, orient="vertical", command=tree.yview)
    y_scrollbar.pack(side="right", fill="y")
    tree.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

    load_data()
def delete_member(member_id):
    """
    Deletes a member and their associated data from the CSV file.

    Args:
        member_id (str): The ID of the member to delete.
    """
    if not member_id:
        messagebox.showwarning("Warning", "Please enter a valid Member ID to delete.")
        return

    try:
        rows = []
        with open(FILE_PATH, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] != member_id or row[0] == "Appointment":  # Exclude appointment data
                    rows.append(row)
        with open(FILE_PATH, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        # Refresh member data
        populate_fields_with_member_data("dummy_id")
        for widget in right_frame.winfo_children():
            widget.destroy()
        messagebox.showinfo("Success", "Member and associated data deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete member: {str(e)}")

def show_attendance(member_id):
    """
    Displays the attendance records of a member in a Treeview.

    Args:
        member_id (str): The ID of the member whose attendance is displayed.
    """
    for widget in right_frame.winfo_children():
        widget.destroy()

    fields = SCHEMA["Attendance"]
    attendance_info = []

    # Read attendance records from the CSV file
    with open(FILE_PATH, mode="r") as file:
        reader = csv.reader(file)
        attendance_dates = set()
        for row in reader:
            if row[0] == "Attendance" and row[1] == member_id:
                date = row[3].split()[0]  
                if date not in attendance_dates:
                    attendance_dates.add(date)
                    attendance_info.append(row[1:])

    if not attendance_info:
        messagebox.showinfo("Info", "No attendance records found for this member.")
        return

    # Create Treeview to display attendance records
    tree = ttk.Treeview(right_frame, columns=fields, show="headings")
    for field in fields:
        tree.heading(field, text=field, anchor='center') 
        tree.column(field, anchor='center')
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Add scrollbars to the Treeview
    x_scrollbar = Scrollbar(right_frame, orient="horizontal", command=tree.xview)
    x_scrollbar.pack(side="bottom", fill="x")
    y_scrollbar = Scrollbar(right_frame, orient="vertical", command=tree.yview)
    y_scrollbar.pack(side="right", fill="y")
    tree.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

    # Insert attendance records into the Treeview
    for record in attendance_info:
        tree.insert("", "end", values=record)


def create_final_sheet():
    """
    Creates a summary sheet of all members and displays it in a Treeview.
    """
    for widget in right_frame.winfo_children():
        widget.destroy()

    data_dict = {table: [] for table in SCHEMA.keys()}

    with open(FILE_PATH, mode="r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row[0] in SCHEMA.keys():
                data_dict[row[0]].append(row[1:])

    member_data = []
    for member in data_dict["Member"]:
        member_id = member[0]
        member_info = member[:10]  # Include only the first 10 fields from the Member table

        member_data.append(member_info)

    headers_combined = SCHEMA["Member"][:10]  # Include only the first 10 fields from the Member table

    tree = ttk.Treeview(right_frame, columns=headers_combined, show="headings")
    for header in headers_combined:
        tree.heading(header, text=header, anchor='center')
        tree.column(header, anchor='center')  # Center-align the columns
    tree.pack(fill="both", expand=True)

    x_scrollbar = Scrollbar(right_frame, orient="horizontal", command=tree.xview)
    x_scrollbar.pack(side="bottom", fill="x")
    y_scrollbar = Scrollbar(right_frame, orient="vertical", command=tree.yview)
    y_scrollbar.pack(side="right", fill="y")
    tree.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

    for member_info in member_data:
        tree.insert("", "end", values=member_info)



def search_member():
    """
    Visualizes gym data using a horizontal bar chart.

    Args:
        member_id (str, optional): Filter data for a specific member. Defaults to None.
    """
    search_term = search_entry.get()
    if not search_term:
        messagebox.showwarning("Warning", "Please enter a search term.")
        return

    for widget in right_frame.winfo_children():
        widget.destroy()

    found_member = False
    with open(FILE_PATH, mode="r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row[0] == "Member" and row[1] == search_term:
                found_member = True
                populate_fields_with_member_data(row[1])  # Populate fields with found member data
                break  # Stop after finding the matching member

    if not found_member:
        messagebox.showinfo("Info", "No matching member found.")
        return

    # Auto-fill the management fields for the found member (excluding Attendance)
    for table in SCHEMA.keys():
        if table != "Attendance" and table in member_data:
            open_crud_window(table)

def visualize_gym_data(member_id=None):
    """
    Initializes the main user interface of the gym management system.
    """
    # Hide entry forms
    for widget in right_frame.winfo_children():
        widget.destroy()

    data_dict = {table: [] for table in SCHEMA.keys()}
    with open(FILE_PATH, mode="r") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row[0] in SCHEMA.keys():
                data_dict[row[0]].append(row[1:])

    # If member_id is provided, filter data for that member
    if member_id:
        member_data = [member for member in data_dict["Member"] if member[0] == member_id]
        if not member_data:
            messagebox.showinfo("Info", "No matching member found.")
            return
    else:
        member_data = data_dict["Member"]

    member_names = [member[1] for member in member_data]
    join_dates = [datetime.strptime(member[6], "%Y-%m-%d") for member in member_data]

    plt.figure(figsize=(10, 6))
    plt.barh(member_names, join_dates)
    plt.xlabel("Join Date")
    plt.ylabel("Member Names")
    plt.title("Gym Member Join Dates")
    plt.grid(True)
    plt.tight_layout()

    plt.show()

def main_ui():
    global root, right_frame, search_entry
    root = Tk()
    root.title("Gym Management System")
    root.geometry("1200x800")

    left_frame = Frame(root, width=200, bg="lightgray")
    left_frame.pack(side="left", fill="y")

    top_frame = Frame(root, height=50, bg="lightblue")
    top_frame.pack(side="top", fill="x")

    search_label = Label(top_frame, text="Search Member:", bg="lightblue")
    search_label.pack(side="left", padx=5)
    search_entry = Entry(top_frame, width=30)
    search_entry.pack(side="left", padx=5)
    search_button = Button(top_frame, text="Search", command=search_member, bg="lightblue", fg="white", font=("Arial", 10, "bold"))
    search_button.pack(side="left", padx=5)
    
    # Add the Show Attendance button next to the Search button
    attendance_button = Button(top_frame, text="Show Attendance", command=lambda: show_attendance(search_entry.get()), bg="lightblue", fg="white", font=("Arial", 10, "bold"))
    attendance_button.pack(side="left", padx=5)

    # Add the Delete Member button
    delete_member_button = Button(top_frame, text="Delete Member", command=lambda: delete_member(search_entry.get()), bg="red", fg="white", font=("Arial", 10, "bold"))
    delete_member_button.pack(side="left", padx=5)

    # Add the Visualize Data button
    visualize_button = Button(top_frame, text="Visualize Data", command=lambda: visualize_gym_data(search_entry.get()), bg="lightgreen", fg="black", font=("Arial", 10, "bold"))
    visualize_button.pack(side="left", padx=5)

    right_frame = Frame(root, bg="white")
    right_frame.pack(side="right", fill="both", expand=True)

    for table in SCHEMA.keys():
        button = Button(left_frame, text=f"Manage {table}", command=lambda t=table: open_crud_window(t), width=20, bg="lightgray", fg="black", font=("Arial", 10, "bold"))
        button.pack(padx=10, pady=5)

    final_data_button = Button(left_frame, text="Show Data", command=create_final_sheet, width=20, bg="lightgray", fg="black", font=("Arial", 10, "bold"))
    final_data_button.pack(padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    initialize_csv()
    main_ui()
