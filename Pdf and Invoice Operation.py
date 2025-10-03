import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import Menu
import shutil
import os

def choose_excel_file():
    excel_file = filedialog.askopenfilename(title="Select an Excel File", filetypes=[("Excel files", "*.xlsx")])
    if not excel_file:
        print("No Excel file selected.")
        return None
    return excel_file

def choose_pdfs():
    input_files = filedialog.askopenfilenames(title="Select PDF Files", filetypes=[("PDF files", "*.pdf")])
    return input_files

def choose_output_folder():
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        print("No output folder selected.")
        return None
    return output_folder

def copy_pdfs(pdf_filenames, selected_pdfs, output_folder):
    for input_file in selected_pdfs:
        if os.path.basename(input_file) in pdf_filenames:
            try:
                shutil.copy(input_file, output_folder)
                print(f"File '{os.path.basename(input_file)}' copied successfully to '{output_folder}'")
            except Exception as e:
                print(f"Error copying file: {e}")
        else:
            print(f"File '{os.path.basename(input_file)}' is not in the list.")

def make_pdf_copies(file_paths, pdf_filenames, num_copies, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_path in file_paths:
        original_file_name = os.path.basename(file_path)
        if original_file_name in pdf_filenames:
            for i in range(1, num_copies + 1):
                new_file_name = f"{original_file_name.replace('.pdf', '')}_{i}.pdf"
                copy_path = os.path.join(output_dir, new_file_name)
                shutil.copy(file_path, copy_path)
                print(f"Created: {copy_path}")

def on_pdf_copy_button():
    excel_file = choose_excel_file()
    if excel_file:
        df = pd.read_excel(excel_file)
        pdf_filenames = df['pdf_filename'].tolist()
        selected_pdfs = choose_pdfs()

        if selected_pdfs:
            output_folder = choose_output_folder()
            if output_folder:
                copy_pdfs(pdf_filenames, selected_pdfs, output_folder)
                messagebox.showinfo("Success", "PDF copy operation completed.")

def on_duplicate_pdf_button():
    excel_file = choose_excel_file()
    if excel_file:
        try:
            df = pd.read_excel(excel_file)
            
            # Check if the 'pdf_filename' column exists
            if 'pdf_filename' not in df.columns:
                raise ValueError("The 'pdf_filename' column is missing in the selected Excel file.")
            
            pdf_filenames = df['pdf_filename'].tolist()
            selected_pdfs = choose_pdfs()

            if selected_pdfs:
                output_folder = choose_output_folder()
                if output_folder:
                    num_copies = simpledialog.askinteger("Number of Copies", "Enter the number of copies you want to create:",
                                                         minvalue=1, maxvalue=100, initialvalue=2)
                    if num_copies:
                        make_pdf_copies(selected_pdfs, pdf_filenames, num_copies, output_folder)
                        messagebox.showinfo("Success", "Duplicate PDF creation completed.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


def create_rounded_button(canvas, text, x, y, command, color, hover_color):
    def on_enter(e):
        button.config(bg=hover_color)

    def on_leave(e):
        button.config(bg=color)

    button = tk.Button(
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

def Format4():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
        "pdf_filename": ["pdf_filename.pdf", "pdf_filename1.pdf"],
    }

    df = pd.DataFrame(data)
    excel_filename = 'pdf_filename.xlsx'
    df.to_excel(excel_filename, index=False)
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")

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

def Format5():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
        "Invoice Number": ["INV123", "INV456"],
    }

    df = pd.DataFrame(data)
    excel_filename = 'Invoice Number.xlsx'
    df.to_excel(excel_filename, index=False)
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")



def create_main_window():
    window = tk.Tk()
    window.title("PDF and Invoice Operation")

    # Set the window size
    window.geometry("400x300")

    # Create a menubar
    menubar = Menu(window)
    window.config(menu=menubar)

    # Create the 'Excel Format' menu
    Excel_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Excel Format", menu=Excel_menu)

    # Add the 'pdf_filename' command to the menu
    Excel_menu.add_command(label="pdf_filename", command=Format4)
    Excel_menu.add_command(label="Invoice Number", command=Format5)

    # Create a canvas to draw buttons
    canvas = tk.Canvas(window, width=400, height=300)
    canvas.pack()

    # Add rounded buttons using the create_rounded_button function
    create_rounded_button(canvas, "Create PDF Copy", 100, 80, on_pdf_copy_button, "#4CAF50", "#45a049")
    create_rounded_button(canvas, "Create Duplicate PDF", 100, 150, on_duplicate_pdf_button, "#008CBA", "#005f73")
    create_rounded_button(canvas, "Invoice No Duplicate", 100, 220, process_file, "#1D3557", "#457B9D")

    window.mainloop()

create_main_window()
