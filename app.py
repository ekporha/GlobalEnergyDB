import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import os
import webbrowser
import csv
import datetime # Import datetime for the PDF export timestamp
from urllib.parse import quote # Import quote for URL encoding

# Try to import reportlab for PDF generation
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib import colors
    from reportlab.lib.units import inch # Import inch for spacing
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("ReportLab not found. PDF export will be disabled. Install with 'pip install reportlab'")

# --- Database Setup ---
DB_FILE = "global_energy_db.sqlite"

def create_db_and_table():
    """Creates the database file and the 'producers' table if they don't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS producers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE, -- Added UNIQUE constraint for name
                contact TEXT,
                address TEXT,
                products TEXT,
                category TEXT
            )
        """)
        conn.commit()
        # messagebox.showinfo("Database Info", "Database and 'producers' table ensured to exist.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to create database/table: {e}")
    finally:
        if conn:
            conn.close()

# Ensure DB and table exist on startup
create_db_and_table()

# Connect to database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# --- GUI App ---
root = tk.Tk() # <--- THIS IS THE CRUCIAL LINE THAT MUST BE PRESENT
root.title("Global Energy Producers Database")
root.geometry("1000x800") # Increased window size for new elements

# --- Functions for CRUD Operations ---

def clear_fields():
    """Clears all input entry fields."""
    entry_name.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_products.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    # Clear selection in treeview
    for item in tree.selection():
        tree.selection_remove(item)

def load_data(search_term="", search_by=""):
    """
    Loads data from the 'producers' table into the Treeview,
    with optional search filtering.
    """
    for item in tree.get_children():
        tree.delete(item) # Clear existing data

    query = "SELECT * FROM producers"
    params = []

    if search_term and search_by:
        if search_by == "Name":
            query += " WHERE name LIKE ?"
            params.append(f"%{search_term}%")
        elif search_by == "Category":
            query += " WHERE category LIKE ?"
            params.append(f"%{search_term}%")
    
    try:
        cursor.execute(query, params)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to load data: {e}")

# Helper function to check for existing producer by name
def producer_exists(name):
    cursor.execute("SELECT 1 FROM producers WHERE name = ?", (name,))
    return cursor.fetchone() is not None

def add_producer():
    """Adds a new producer record to the database."""
    name = entry_name.get().strip()
    contact = entry_contact.get().strip()
    address = entry_address.get().strip()
    products = entry_products.get().strip()
    category = entry_category.get().strip()

    if not name:
        messagebox.showwarning("Input Error", "Producer Name cannot be empty.")
        return

    # Check for duplicates
    if producer_exists(name):
        messagebox.showwarning("Duplicate Entry", f"A producer with the name '{name}' already exists.")
        return

    try:
        cursor.execute("INSERT INTO producers (name, contact, address, products, category) VALUES (?, ?, ?, ?, ?)",
                       (name, contact, address, products, category))
        conn.commit()
        messagebox.showinfo("Success", "Producer added successfully!")
        clear_fields()
        load_data() # Refresh data
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to add producer: {e}")

def update_producer():
    """Updates the selected producer record in the database."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a producer to update.")
        return

    producer_id = tree.item(selected_item, 'values')[0] # Get ID from selected row

    name = entry_name.get().strip()
    contact = entry_contact.get().strip()
    address = entry_address.get().strip()
    products = entry_products.get().strip()
    category = entry_category.get().strip()

    if not name:
        messagebox.showwarning("Input Error", "Producer Name cannot be empty.")
        return
    
    # Check for duplicates when updating if the name is changed to an existing one
    original_name = tree.item(selected_item, 'values')[1]
    if name != original_name and producer_exists(name):
        messagebox.showwarning("Duplicate Entry", f"A producer with the name '{name}' already exists. Cannot update to a duplicate name.")
        return

    try:
        cursor.execute("UPDATE producers SET name=?, contact=?, address=?, products=?, category=? WHERE id=?",
                       (name, contact, address, products, category, producer_id))
        conn.commit()
        messagebox.showinfo("Success", "Producer updated successfully!")
        clear_fields()
        load_data() # Refresh data
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to update producer: {e}")

def delete_producer():
    """Deletes the selected producer record from the database."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a producer to delete.")
        return

    producer_id = tree.item(selected_item, 'values')[0] # Get ID from selected row

    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete producer ID {producer_id}?"):
        try:
            cursor.execute("DELETE FROM producers WHERE id=?", (producer_id,))
            conn.commit()
            messagebox.showinfo("Success", "Producer deleted successfully!")
            clear_fields()
            load_data() # Refresh data
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete producer: {e}")

def on_tree_select(event):
    """Populates input fields when a row in the Treeview is selected."""
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, 'values')
        clear_fields() # Clear first to avoid appending
        entry_name.insert(0, values[1])
        entry_contact.insert(0, values[2])
        entry_address.insert(0, values[3])
        entry_products.insert(0, values[4])
        entry_category.insert(0, values[5])

def search_producers():
    """Triggers data loading with search filters."""
    search_term = entry_search.get().strip()
    search_by = search_by_combobox.get()
    load_data(search_term, search_by)

def show_all_producers():
    """Resets search fields and loads all data."""
    entry_search.delete(0, tk.END)
    search_by_combobox.set("Name") # Reset to default search by
    load_data()

def web_search_producer():
    """Opens a Google search for the selected producer's product name."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a producer to perform a web search.")
        return

    # Get the product name (index 4 in the values tuple)
    product_name = tree.item(selected_item, 'values')[4] 
    
    if product_name:
        # Add "energy product" to narrow down the search
        search_query = f"{product_name} energy product" 
        webbrowser.open_new_tab(f"https://www.google.com/search?q={quote(search_query)}")
    else:
        messagebox.showinfo("Web Search", "No product name found for web search for the selected producer.")

def web_search_product_keyword():
    """
    Performs a general web search for companies producing a given product keyword.
    """
    keyword = entry_web_search_keyword.get().strip()
    if not keyword:
        messagebox.showwarning("Input Error", "Please enter a keyword for product web search.")
        return

    # Construct a search query to find companies producing the keyword
    search_query = f"companies producing {keyword}" 
    webbrowser.open_new_tab(f"https://www.google.com/search?q={quote(search_query)}")

def export_to_csv():
    """Exports current Treeview data to a CSV file."""
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not filepath:
        return # User cancelled

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["ID", "Name", "Contact", "Address", "Products", "Category"])
            # Write data
            cursor.execute("SELECT * FROM producers")
            for row in cursor.fetchall():
                writer.writerow(row)
        messagebox.showinfo("Export Success", f"Data successfully exported to {filepath}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export to CSV: {e}")

def export_to_pdf():
    """Exports current Treeview data to a PDF file using ReportLab."""
    if not REPORTLAB_AVAILABLE:
        messagebox.showerror("Error", "ReportLab library not found. PDF export is disabled. Please install it using 'pip install reportlab'.")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    if not filepath:
        return # User cancelled

    try:
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("Global Energy Producers Database", styles['h1']))
        elements.append(Spacer(1, 0.2 * inch))

        # Table Data
        data = [["ID", "Name", "Contact", "Address", "Products", "Category"]] # Table header
        cursor.execute("SELECT * FROM producers")
        for row in cursor.fetchall():
            data.append(list(row)) # Convert tuple to list for modification if needed

        table = Table(data)

        # Table Style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elements.append(Paragraph(f"Exported on: {current_time}", styles['Normal']))

        doc.build(elements)
        messagebox.showinfo("Export Success", f"Data successfully exported to {filepath}")

    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export to PDF: {e}")
    
# --- Import CSV to Database ---
def import_csv_to_database():
    """
    Imports data from a selected CSV file into the 'producers' table.
    Assumes CSV columns are: Name, Contact, Address, Products, Category.
    Checks for and skips duplicate producer names.
    """
    filepath = filedialog.askopenfilename(
        title="Select CSV File to Import",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not filepath:
        return # User cancelled

    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) # Skip header row

            imported_count = 0
            skipped_duplicates = 0
            skipped_malformed = 0

            for i, row in enumerate(reader):
                if len(row) >= 5: # Ensure row has enough columns
                    name = row[0].strip()
                    contact = row[1].strip()
                    address = row[2].strip()
                    products = row[3].strip()
                    category = row[4].strip()

                    if producer_exists(name):
                        skipped_duplicates += 1
                        print(f"Skipping row {i+2} (Name: '{name}') due to duplicate. Information already exists.") # +2 for header and 0-index
                    else:
                        cursor.execute("INSERT INTO producers (name, contact, address, products, category) VALUES (?, ?, ?, ?, ?)",
                                       (name, contact, address, products, category))
                        imported_count += 1
                else:
                    skipped_malformed += 1
                    print(f"Skipping row {i+2} due to insufficient columns: {row}") # +2 for header and 0-index
        conn.commit()
        
        summary_message = f"CSV import complete:\n" \
                          f"  - Successfully imported: {imported_count} records.\n" \
                          f"  - Skipped (Duplicates): {skipped_duplicates} records.\n" \
                          f"  - Skipped (Malformed rows): {skipped_malformed} records."
        messagebox.showinfo("Import Summary", summary_message)
        
        load_data() # Refresh data in the Treeview
    except Exception as e:
        conn.rollback() # Rollback changes if an error occurs
        messagebox.showerror("Import Error", f"Failed to import CSV: {e}")

# --- GUI Layout ---

# Input Frame
input_frame = tk.LabelFrame(root, text="Producer Details", padx=10, pady=10)
input_frame.pack(pady=10, padx=10, fill="x")

tk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
entry_name = tk.Entry(input_frame, width=40)
entry_name.grid(row=0, column=1, pady=2, padx=5)

tk.Label(input_frame, text="Contact:").grid(row=1, column=0, sticky="w", pady=2)
entry_contact = tk.Entry(input_frame, width=40)
entry_contact.grid(row=1, column=1, pady=2, padx=5)

tk.Label(input_frame, text="Address:").grid(row=2, column=0, sticky="w", pady=2)
entry_address = tk.Entry(input_frame, width=40)
entry_address.grid(row=2, column=1, pady=2, padx=5)

tk.Label(input_frame, text="Products:").grid(row=0, column=2, sticky="w", pady=2, padx=10)
entry_products = tk.Entry(input_frame, width=40)
entry_products.grid(row=0, column=3, pady=2, padx=5)

tk.Label(input_frame, text="Category:").grid(row=1, column=2, sticky="w", pady=2, padx=10)
entry_category = tk.Entry(input_frame, width=40)
entry_category.grid(row=1, column=3, pady=2, padx=5)

# CRUD Buttons Frame
button_frame = tk.Frame(root, padx=10, pady=5)
button_frame.pack(pady=5, padx=10, fill="x")

btn_add = tk.Button(button_frame, text="Add New Producer", command=add_producer)
btn_add.pack(side="left", padx=5)

btn_update = tk.Button(button_frame, text="Update Selected", command=update_producer)
btn_update.pack(side="left", padx=5)

btn_delete = tk.Button(button_frame, text="Delete Selected", command=delete_producer)
btn_delete.pack(side="left", padx=5)

btn_clear = tk.Button(button_frame, text="Clear Fields", command=clear_fields)
btn_clear.pack(side="left", padx=5)

# Search Frame
search_frame = tk.LabelFrame(root, text="Search Database", padx=10, pady=5)
search_frame.pack(pady=5, padx=10, fill="x")

entry_search = tk.Entry(search_frame, width=50)
entry_search.pack(side="left", padx=5)

search_by_combobox = ttk.Combobox(search_frame, values=["Name", "Category"], state="readonly")
search_by_combobox.set("Name") # Default value
search_by_combobox.pack(side="left", padx=5)

btn_search = tk.Button(search_frame, text="Search", command=search_producers)
btn_search.pack(side="left", padx=5)

btn_show_all = tk.Button(search_frame, text="Show All", command=show_all_producers)
btn_show_all.pack(side="left", padx=5)

# Web Search Options Frame
web_search_frame = tk.LabelFrame(root, text="Web Search Options", padx=10, pady=5)
web_search_frame.pack(pady=5, padx=10, fill="x")

btn_web_search_product_of_producer = tk.Button(web_search_frame, text="Web Search Selected Product (from DB)", command=web_search_producer)
btn_web_search_product_of_producer.pack(side="left", padx=5)

tk.Label(web_search_frame, text="  OR  Search Product Keyword:").pack(side="left", padx=15)
# Corrected: Parent for entry_web_search_keyword should be web_search_frame
entry_web_search_keyword = tk.Entry(web_search_frame, width=30) 
entry_web_search_keyword.pack(side="left", padx=5)

btn_web_search_keyword_general = tk.Button(web_search_frame, text="Search Companies on Web", command=web_search_product_keyword)
btn_web_search_keyword_general.pack(side="left", padx=5)


# Treeview for displaying data
tree_frame = tk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Contact", "Address", "Products", "Category"), show="headings", yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.yview)

# Define column headings and widths
columns = {
    "ID": 50,
    "Name": 150,
    "Contact": 120,
    "Address": 200,
    "Products": 150,
    "Category": 100
}

for col, width in columns.items():
    tree.heading(col, text=col, anchor="w")
    tree.column(col, width=width, minwidth=width, stretch=tk.NO)

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_tree_select) # Bind selection event

# Export/Import Buttons Frame (New)
data_io_frame = tk.Frame(root, padx=10, pady=5)
data_io_frame.pack(pady=5, padx=10, fill="x")

btn_export_csv = tk.Button(data_io_frame, text="Export to CSV", command=export_to_csv)
btn_export_csv.pack(side="left", padx=5)

btn_export_pdf = tk.Button(data_io_frame, text="Export to PDF", command=export_to_pdf)
btn_export_pdf.pack(side="left", padx=5)

btn_import_csv = tk.Button(data_io_frame, text="Import from CSV", command=import_csv_to_database)
btn_import_csv.pack(side="left", padx=5)


# Load data on start
load_data()

# Start GUI loop
root.mainloop()

# Close database connection when the app closes
conn.close()