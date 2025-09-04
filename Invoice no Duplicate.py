import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, Canvas, Button, Menu

def create_rounded_button(canvas, text, x, y, command, color, hover_color):
    def on_enter(e):
        button.config(bg=hover_color)

    def on_leave(e):
        button.config(bg=color)

    button = Button(
        canvas,
        text=text,
        command=command,
        font=('Verdana', 12, 'bold'),
        fg="#FFFFFF",
        bg=color,
        activebackground=hover_color,
        activeforeground="#FFFFFF",
        relief='flat',
        bd=0,
        width=20,
        height=2
    )
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.place(x=x, y=y)

def process_file():
    file_path = filedialog.askopenfilename(title='Select Invoice Number')
    
    if not file_path:
        messagebox.showwarning("Warning", "No file selected!")
        return
    
    try:
        data = pd.read_excel(file_path)
        df = pd.DataFrame(data)

        # Add unique suffixes to duplicate invoice numbers
        df['Unique_Invoice_Number'] = df['Invoice Number'].astype(str) + '_' + (df.groupby('Invoice Number').cumcount() + 1).astype(str)


        # Save the updated DataFrame to a new Excel file
        output_path = 'updated_invoices.xlsx'
        df.to_excel(output_path, index=False)
        
        messagebox.showinfo("Success", f"File processed and saved as {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def Format4():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
        "Invoice Number": ["INV123", "INV456"],
    }

    df = pd.DataFrame(data)
    excel_filename = 'Invoice Number.xlsx'
    df.to_excel(excel_filename, index=False)
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")

# Set up the main application window
root = tk.Tk()
root.title("Invoice Number Processor")
root.geometry("400x400")

# Create a menu bar
menubar = Menu(root)
root.config(menu=menubar)

Excel_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Excel Format", menu=Excel_menu)

Excel_menu.add_command(label="Invoice Number", command=Format4)

# Create and configure the Canvas
canvas = Canvas(root, bg="#ECECEC", width=400, height=400)
canvas.pack(fill="both", expand=True)

# Add title text to the Canvas
canvas.create_text(200, 80, text="Invoice Number Processor", font=("Arial", 18, "bold"), fill="#333333")

# Add the rounded button to choose and process the file
create_rounded_button(canvas, "Choose File and Process", 100, 200, process_file, "#1D3557", "#457B9D")

# Run the application
root.mainloop()
