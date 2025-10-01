import pandas as pd
import numpy as np
import tkinter as tk
from xlsx2html import xlsx2html
import xlsxwriter
import tkinter.filedialog as fd
import time
import os
import sys
import datetime
from PyPDF2 import PdfMerger, PdfReader
from pathlib import Path
import pdfkit
import re
from openpyxl.workbook import Workbook
from tkinter import messagebox, Menu, Button, Label
from PIL import ImageTk, Image

# Path to wkhtmltopdf (Ensure installed)
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# PDFKit Options
options = {
    'page-size': 'Letter',
    'orientation': 'Landscape',
    'margin-top': '0.1in',
    'margin-right': '0.1in',
    'margin-bottom': '0.1in',
    'margin-left': '0.1in',
    'encoding': "UTF-8",
    'custom-header': [('Accept-Encoding', 'gzip')]
}

def hello2():
    root = tk.Tk()
    root.withdraw()
    file = fd.askopenfilename(parent=root, title='Choose a Base file')
    if not file:
        print("No file selected. Exiting.")
        sys.exit()
    print(f"Selected file: {file}")

    df = pd.read_excel(file, keep_default_na=False)

    # Extracting required columns and cleaning up line breaks and spaces
    df = df[['Entity Name (to whom oil sold)',
             'Address of the Entity (to whom oil sold)',
             'GST Number of the Entity (to whom oil sold)',
             'Quantity of Oil Sold (in MT)',
             'Email id of the Entity',
             'Contact number of the Entity',
             'Type Of Producer',
             'Type of Oil']]

    for col in df.columns:
        df[col] = df[col].astype(str).str.replace('\n', '').str.strip().str.upper()

    df['Email id of the Entity'] = df['Email id of the Entity'].apply(lambda x: x.replace(',', ',<br>').strip())
    df['Quantity of Oil Sold (in MT)'] = pd.to_numeric(df['Quantity of Oil Sold (in MT)'], errors='coerce').fillna(0)

    now = datetime.datetime.now()
    directory = now.strftime("%d%m%Y_%H%M%S")
    parent_dir = Path.cwd()
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    path1, path2 = os.path.join(path, "excel"), os.path.join(path, "pdf")
    os.mkdir(path1)
    os.mkdir(path2)
    print(f"Output directory created: {path}")

    pivot_table = df.groupby(['Entity Name (to whom oil sold)', 'Type Of Producer', 'Type of Oil'], dropna=False)[
        ["Quantity of Oil Sold (in MT)"]].sum().reset_index()

    pivot_name = os.path.join(path, 'pivot_table.xlsx')
    with pd.ExcelWriter(pivot_name, engine='xlsxwriter') as writer:
        pivot_table.to_excel(writer, sheet_name="Pivot Data", index=False)
        worksheet = writer.sheets['Pivot Data']
        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 2, 20)
        worksheet.set_column(3, 3, 25)
    print(f"Pivot table saved: {pivot_name}")

    sales_pivot = df.pivot_table(
        index='Type of Oil',
        columns='Type Of Producer',
        values='Quantity of Oil Sold (in MT)',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    sales_pivot_name = os.path.join(path, 'sales_data_upload.xlsx')
    with pd.ExcelWriter(sales_pivot_name, engine='xlsxwriter') as writer:
        sales_pivot.to_excel(writer, sheet_name="Sales Data", index=False)
        worksheet = writer.sheets['Sales Data']
        worksheet.set_column(0, 0, 20)
        for i, col in enumerate(sales_pivot.columns[1:]):
            worksheet.set_column(i + 1, i + 1, 18)
    print(f"Sales data upload file saved: {sales_pivot_name}")

    def generate_reports(data, producer_type, oil_type):
        if data.empty:
            return

        data = df.groupby([
            'Entity Name (to whom oil sold)',
            'Address of the Entity (to whom oil sold)',
            'GST Number of the Entity (to whom oil sold)',
            'Email id of the Entity',
            'Contact number of the Entity',
            'Type Of Producer',
            'Type of Oil'
        ], dropna=False)[["Quantity of Oil Sold (in MT)"]].sum().reset_index()

        # Ensure Quantity column is numeric
        data['Quantity of Oil Sold (in MT)'] = pd.to_numeric(data['Quantity of Oil Sold (in MT)'], errors='coerce')

        # Add Serial Number
        data.insert(0, "S. NO.", np.arange(1, len(data) + 1), True)

        # Create TOTAL row
        total_row = {col: '' for col in data.columns}
        total_row["S. NO."] = "TOTAL"
        total_row["Quantity of Oil Sold (in MT)"] = data['Quantity of Oil Sold (in MT)'].sum()

        # Append TOTAL row
        data = pd.concat([data, pd.DataFrame([total_row])], ignore_index=True)

        # Drop unwanted columns
        data = data.drop(columns=['Type Of Producer', 'Type of Oil'])

        # Generate filename
        filename = f"{producer_type} {oil_type}"
        filename = re.sub(r'[^a-zA-Z0-9 ]', '', filename).strip()

        filenameexcel = os.path.join(path1, filename + '.xlsx')
        filenamepdf = os.path.join(path2, filename + '.pdf')

        # Save to Excel
        writer = pd.ExcelWriter(filenameexcel, engine='xlsxwriter')
        data.to_excel(writer, index=False, sheet_name='Report')
        workbook = writer.book
        worksheet = writer.sheets['Report']

        # Formatting Styles
        fmt_header = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'fg_color': '#002060',
            'font_color': '#FFFFFF',
            'border': 1
        })
        format1 = workbook.add_format({"num_format": "#,##0.00000"})
        worksheet.set_zoom(80)

        # Apply header formatting dynamically (No extra blue line)
        for col_num, column_name in enumerate(data.columns):
            worksheet.write(0, col_num, column_name, fmt_header)

        # Apply number format to Quantity column dynamically
        quantity_col_index = data.columns.get_loc("Quantity of Oil Sold (in MT)")
        worksheet.set_column(quantity_col_index, quantity_col_index, 15, format1)

        # OPTIONAL: Auto adjust column width based on data length
        # for idx, col in enumerate(data.columns):
        #     max_length = max([len(str(s)) for s in data[col].astype(str)] + [len(col)]) + 2
        #     worksheet.set_column(idx, idx, max_length)

        writer.close()
        print(f"Excel file saved: {filenameexcel}")

        # Convert Excel to HTML for PDF conversion
        xlsx2html(filenameexcel, 'output.html')
        with open("output.html", "r", encoding="utf-8") as file:
            file_content = file.read()

        # Modify HTML for better PDF formatting
        file_content = file_content.replace("none", "1").replace(
            '<table  style="border-collapse: collapse" border="0" cellspacing="0" cellpadding="0">',
            '<table  style="border-collapse: collapse" border="1" cellspacing="0" cellpadding="0">'
        ).replace('cellpadding="0">', 'cellpadding="1">').replace(': 19pt">', ': 19pt;text-align: center">')

        with open("output.html", "w", encoding="utf-8") as file_to_write:
            file_to_write.write(file_content)

        # Convert HTML to PDF
        try:
            r = pdfkit.PDFKit('output.html', 'html', verbose=True, configuration=config, options=options)
            r.to_pdf(filenamepdf)
            print(f"PDF file saved: {filenamepdf}")
        except Exception as e:
            print(f"PDF conversion failed for {filename}: {e}")

        os.remove("output.html")


    # Process normal producers
    for i in range(len(pivot_table)):
        df_filtered = df[
            (df["Type Of Producer"] == pivot_table.loc[i, "Type Of Producer"]) &
            (df["Type of Oil"] == pivot_table.loc[i, "Type of Oil"])
        ]
        generate_reports(df_filtered, pivot_table.loc[i, "Type Of Producer"], pivot_table.loc[i, "Type of Oil"])

def Format():
    data = {
        "S. No.": [1, 2, 3, 4],
        "Entity Name (to whom oil sold)": ["Entity 1", "Entity 2", "Entity 3", "Entity 4"],
        "Address of the Entity (to whom oil sold)": ["Address 1", "Address 2", "Address 3", "Address 4"],
        "GST Number of the Entity (to whom oil sold)": ["GST123", "GST456", "GST789", "GST012"],
        "Quantity of Oil Sold (in MT)": [10.5, 20.3, 15.0, 8.7],
        "Email id of the Entity": ["email1@gmail.com", "email2@gmail.com", "email3@gmail.com", "email4@gmail.com"],
        "Contact number of the Entity": [9876543210, 8765432109, 7654321098, 6543210987],
        "Type Of Producer": ["Producer 1", "Producer 2", "Producer 3", "Producer 4"],
        "Type of Oil": ["Type of Oil1", "Type of Oil2", "Type of Oil3", "Type of Oil4"]
    }
    pd.DataFrame(data).to_excel('Base_Data_Format.xlsx', index=False)
    messagebox.showinfo("Success", "Excel file 'Base_Data_Format.xlsx' has been created successfully.")

root = tk.Tk()
root.title("USED OIL BOT")
root.geometry("400x200")
root.configure(bg="#3498DB")

menubar = Menu(root)
root.config(menu=menubar)
Excel_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Excel Format", menu=Excel_menu)
Excel_menu.add_command(label="Base Data_Format", command=Format)

Label(root, text="USED OIL BOT", bg="#3498DB", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
Button(root, text="Generate PDF", command=hello2, bg="#1ABC9C", fg="#FFFFFF", font=('Verdana', 12, "bold"), width=15, height=2).pack(pady=30)
Label(root, text="© AA Garg & Co. All Rights Reserved.", bg="#3498DB", fg="white", font=("Arial", 10, "italic")).pack(side="bottom", pady=5)
root.mainloop()
