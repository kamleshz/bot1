import pandas as pd
import numpy as np
import tkinter as tk
from xlsx2html import xlsx2html
import xlsxwriter
import tkinter.filedialog as fd
import time
import os
import easygui
import sys
import datetime
from PyPDF2 import PdfMerger,PdfReader
from pathlib import Path
import pdfkit
import re
from openpyxl.workbook import Workbook
from openpyxl.reader.excel import load_workbook
import pyperclip

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
options = {
    'page-size': 'Letter',
    'orientation': 'Landscape',
    'margin-top': '0.1in',
##    'valign': 'centre',
##    'halign': 'centre',
##    'align': 'center',
    'margin-right': '0.1in',
    'margin-bottom': '0.1in',
    'margin-left': '0.1in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ]
}


def isValidMasterCardNo(str):

    regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}" + "[A-Z]{1}[1-9A-Z]{1}" + "Z[0-9A-Z]{1}$"
     
    # Compile the ReGex
    p = re.compile(regex)
 
    if (str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False



def refine():
    now = datetime.datetime.now()
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose base file')
    file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
    root.destroy()
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        df1['file_name'][i]=file_name
    
    Registration_Type=['registered', 'unregistered']
    Entity_Type=['pwp', 'producer', 'brand owner', 'importer', 'manufacturer', 'other']
    State=['andaman and nicobar islands', 'andhra pradesh', 'arunachal pradesh', 'assam', 'bihar', 'chandigarh', 'chhattisgarh', 'dadra and nagar haveli and daman and diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal pradesh', 'jammu and kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'pondicherry', 'punjab', 'rajasthan', 'sikkim', 'tamil nadu', 'telangana', 'tripura', 'uttar pradesh', 'uttarakhand', 'west bengal']
    Plastic_Material_Type=['hdpe', 'pet', 'pp', 'ps', 'ldpe', 'lldpe', 'mlp', 'others', 'pla', 'pbat']
    Category_of_Plastic=['cat i', 'cat ii', 'cat iii', 'cat iv']
    Category_of_Plastic2=['cat ii', 'cat iii', 'cat iv']
    Financial_Year=['2021-22', '21-22', '2022-23','22-23','2023-24','23-24']
    Container_Capacity=['containers > 0.9l and < 4.9 l', 'containers > 4.9 l', 'containers < 0.9 l']
    Country=['afghanistan', 'aland islands', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas the', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bonaire', ' sint eustatius and saba', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil', 'british indian ocean territory', 'brunei', 'bulgaria', 'burkina faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'cayman islands', 'central african republic', 'chad', 'chile', 'china', 'christmas island', 'cocos (keeling) islands', 'colombia', 'comoros', 'congo', 'congo the democratic republic of the', 'cook islands', 'costa rica', "cote d'ivoire (ivory coast)", 'croatia (hrvatska)', 'cuba', 'curaçao', 'cyprus', 'czech republic', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'east timor', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands', 'faroe islands', 'fiji islands', 'finland', 'france', 'french guiana', 'french polynesia', 'french southern territories', 'gabon', 'gambia the', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guernsey and alderney', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'heard island and mcdonald islands', 'honduras', 'hong kong s.a.r.', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'jamaica', 'japan', 'jersey', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'korea north', 'korea south', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macau s.a.r.', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'man (isle of)', 'marshall islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands the', 'new caledonia', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands', 'norway', 'oman', 'pakistan', 'palau', 'palestinian territory occupied', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'pitcairn island', 'poland', 'portugal', 'puerto rico', 'qatar', 'reunion', 'romania', 'russia', 'rwanda', 'saint helena', 'saint kitts and nevis', 'saint lucia', 'saint pierre and miquelon', 'saint vincent and the grenadines', 'saint-barthelemy', 'saint-martin (french part)', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten (dutch part)', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south georgia', 'south sudan', 'spain', 'sri lanka', 'sudan', 'suriname', 'svalbard and jan mayen islands', 'swaziland', 'sweden', 'switzerland', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks and caicos islands', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'united states minor outlying islands', 'uruguay', 'uzbekistan', 'vanuatu', 'vatican city state (holy see)', 'venezuela', 'vietnam', 'virgin islands (british)', 'virgin islands (us)', 'wallis and futuna islands', 'western sahara', 'yemen', 'zambia', 'zimbabwe']
    login_select = easygui.enterbox('with which id you want to proceed?\na) PRODUCER\nb) BRAND OWNER \nc) IMPORTER')
    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")

    df = pd.read_excel(file, converters={'pdf_filename':str})
    df['Name of Entity'] = df['Name of Entity'].map(lambda x: re.sub(r'[^a-zA-Z0-9\s]+', '', x))
    df['Plastic Material Type'] = df['Plastic Material Type'].map(lambda x : x.strip())
    df['Address'] = df['Address'].map(lambda x : x.replace('-',''))
    df['pdf_filename'] = ''
    df.to_excel(file)
    df2=df
    df2.columns = [x.lower() for x in df2.columns]
    df2=df2.apply(lambda x: x.astype(str).str.lower())
    df2 = df2.astype(str)
    df2=df2.replace('nan','')
    
    
    row=[]
    invoice_no=[]
    error=[]

    if('registration type' in df2.columns):
        for i in range(len(df2)):
            if(df2['registration type'][i] in Registration_Type):
                pass
            else:
                row.append(i+2)
                invoice_no.append(df2['invoice number'][i])
                if(len(df2['registration type'][i])==0):
                    error.append('registration type BLANK')
                else:
                    error.append('registration type WRONG')
    else:
        print('registration type column not found')


    if('mobile number' in df2.columns):
        for i in range(len(df2)):
            if(len(str(df2['mobile number'][i]))==10):
                pass
            else:
                row.append(i+2)
                invoice_no.append(df2['invoice number'][i])
                if(len(str(df2['registration type'][i]))==0):
                    error.append('mobile number BLANK')
                else:
                    error.append('mobile number WRONG')
    else:
        print('mobile number column not found')

        
    if(select.lower()!='a'):
        if('ifsc code' in df2.columns):
            for i in range(len(df2)):
                if(len(str(df2['ifsc code'][i]))==11):
                    pass
                else:
                    row.append(i+2)
                    invoice_no.append(df2['invoice number'][i])
                    if(len(str(df2['ifsc code'][i]))==0):
                        error.append('ifsc code BLANK')
                    else:
                        error.append('ifsc code WRONG')
        else:
            print('ifsc code column not found')
        

    if('entity type' in df2.columns):
        for i in range(len(df2)):
            if(df2['entity type'][i] in Entity_Type):
                pass
            else:
                row.append(i+2)
                invoice_no.append(df2['invoice number'][i])
                if(len(df2['entity type'][i])==0):
                    error.append('entity type BLANK')
                else:
                    error.append('entity type WRONG')
    else:
        print('entity type column not found')
        
    if(login_select.lower()=='c' and select.lower()=='a'):
        pass
    elif('state' in df2.columns):
        for i in range(len(df2)):
            if(df2['state'][i] in State):
                pass
            else:
                row.append(i+2)
                invoice_no.append(df2['invoice number'][i])
                if(len(df2['state'][i])==0):
                    error.append('state BLANK')
                else:
                    error.append('state WRONG')
    else:
        print('state column not found')
        
    if('plastic material type' in df2.columns):
        for i in range(len(df2)):
            if(df2['plastic material type'][i] in Plastic_Material_Type):
                pass
            else:
                row.append(i+2)
                invoice_no.append(df2['invoice number'][i])
                if(len(df2['plastic material type'][i])==0):
                    error.append('plastic material type BLANK')
                else:
                    error.append('plastic material type WRONG')
    else:
        print('plastic material type column not found')
        
    if('category of plastic' in df2.columns):
        for i in range(len(df2)):
            if(df2['category of plastic'][i] in Category_of_Plastic):
                pass
            else:
                row.append(i+2)
                invoice_no.append(df2['invoice number'][i])
                if(len(df2['category of plastic'][i])==0):
                    error.append('category of plastic BLANK')
                else:
                    error.append('category of plastic WRONG')
    else:
        print('category of plastic column not found')
        
    if('financial year' in df2.columns):
        for i in range(len(df2)):
            if(df2['financial year'][i] in Financial_Year):
                pass
            else:
                row.append(i+2)
                invoice_no.append(df2['invoice number'][i])
                if(len(df2['financial year'][i])==0):
                    error.append('financial year BLANK')
                else:
                    error.append('financial year WRONG')
    else:
        print('financial year column not found')
        
    if(select.lower()=='b'):
        if('cat-1 container capacity' in df2.columns):
            for i in range(len(df2)):
                if(df2['cat-1 container capacity'][i] in Container_Capacity or df2['category of plastic'][i] in Category_of_Plastic2):
                    pass
                else:
                    row.append(i+2)
                    invoice_no.append(df2['invoice number'][i])
                    if(len(df2['cat-1 container capacity'][i])==0):
                        error.append('cat-1 container capacity BLANK')
                    else:
                        error.append('cat-1 container capacity WRONG')
        else:
            print('cat-1 container capacity column not found')
        
    if(login_select.lower()=='c' and select.lower()=='a'):
        if('country' in df2.columns):
            for i in range(len(df2)):
                if(df2['country'][i] in Country):
                    pass
                else:
                    row.append(i+2)
                    invoice_no.append(df2['invoice number'][i])
                    if(len(df2['country'][i])==0):
                        error.append('country BLANK')
                    else:
                        error.append('country WRONG')
        else:
            print('country column not found')
            

    if(login_select.lower()=='b'):
        if('cat-1 container capacity' in df2.columns):
            for i in range(len(df2)):
                if(df2['cat-1 container capacity'][i] in Container_Capacity):
                    pass
                else:
                    row.append(i+2)
                    invoice_no.append(df2['invoice number'][i])
                    if(len(df2['cat-1 container capacity'][i])==0):
                        error.append('cat-1 container capacity BLANK')
                    else:
                        error.append('cat-1 container capacity WRONG')
        else:
            print('cat-1 container capacity column not found')
            

    if('gst number' in df2.columns):
        df2['gst number'] = df['gst number'].str.upper()
        df2['gst number'] = df2['gst number'].str.strip()
        for i in range(len(df2)):
            if(isValidMasterCardNo(str(df2['gst number'][i]))==True):
                pass
            else:
                row.append(i+2)
                invoice_no.append(df2['invoice number'][i])
                if(len(str(df2['gst number'][i]))==0):
                    error.append('gst number BLANK')
                else:
                    error.append('gst number WRONG')
    else:
        print('gst number column not found')

    if('pdf_filename' in df2.columns):
        df2['pdf_filename'] = df['pdf_filename']
        for i in range(len(df2)):
            pdf_file_index=''
            try:
                pdf_file_index = df1[df1['file_name']==df2['pdf_filename'][i]].index[0]
            except:
                pass
            if(len(str(pdf_file_index))>0):
                pass
            else:
                row.append(i+2)
                invoice_no.append(df2['invoice number'][i])
                if(len(df2['pdf_filename'][i])==0):
                    error.append('pdf_filename BLANK')
                else:
                    error.append('pdf_filename WRONG')
    else:
        print('pdf_filename column not found')



    df3 = pd.DataFrame({'Row No': row,
                       'Invoice No': invoice_no,
                       'Error Type': error,
                       })
    print(df3)

    df3.to_excel(str(now.strftime("refined %d%m%Y %H%M%S"))+'.xlsx')

    

def hello2():  
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    root.destroy()
    df = pd.read_excel(file, keep_default_na=False, converters={'Mobile Number':str,'Invoice Number':str,'Bank account no':str,'IFSC code':str})
    print(df.columns)
    df.dropna(how='all', axis=1, inplace=True)
    for i in df.columns:
        try:
            df[i] = df[i].replace('\n','')
            df[i] = df[i].str.strip()
        except:
            pass
    df['Name of Entity'] = df['Name of Entity'].str.upper()
    df['Plastic Material Type']=df['Plastic Material Type'].str.upper()
    df['Financial Year']=df['Financial Year'].str.upper()
    df['Category of Plastic']=df['Category of Plastic'].str.upper()
    df['Name of Entity'] = df['Name of Entity'].str.upper()
    df['Name of Entity'] = df['Name of Entity'].map(lambda x: re.sub(r'[^a-zA-Z0-9\s]+', '', x))
    df['GST Number']=df['GST Number'].str.upper()
    df['Other Plastic Material Type']=df['Other Plastic Material Type'].str.upper()
    now = datetime.datetime.now()

    directory = str(now.strftime("%d%m%Y %H%M%S"))
    parent_dir = Path.cwd()
    path = os.path.join(parent_dir, directory)

    os.mkdir(path)

    directory1 = "excel"
    directory2 = "pdf"
      
    parent_dir = path.replace('\\','/')
      
    path1 = os.path.join(parent_dir, directory1)
    path2 = os.path.join(parent_dir, directory2)

    os.mkdir(path1)
    os.mkdir(path2)
    path1 = path1.replace('\\','/') + '/'
    path2 = path2.replace('\\','/') + '/'
    path4 = path.replace('\\','/') + '/'
    df['month'] = [datetime.datetime.strptime(str(x), "%Y%m%d").date().month for x in df['Date of invoice']]    
    
    df = df[['Registration Type', 'Entity Type','Name of Entity','State','Address','Mobile Number','Plastic Material Type','Category of Plastic','Financial Year', 'Date of invoice', 'Quantity (TPA)','Recycled Plastic %','GST Number','GST Paid','Invoice Number','Other Plastic Material Type','Cat-1 Container Capacity','Bank account no','IFSC code','month']]
    
    select = easygui.enterbox('Select one.\na) Create Pivot table WITH GST Number\nb) Create Pivot table WITHOUT GST Number')
    typee2 = easygui.enterbox('Select one.\na) Create normally\nb) Create Month-Wise')

    if(typee2.lower()== 'a'):
        if(select.lower()=='a'):
            p1 = df.groupby(by=["Name of Entity",'Financial Year','Plastic Material Type','Category of Plastic','GST Number','Recycled Plastic %','Other Plastic Material Type','Cat-1 Container Capacity'], dropna=False)[['Quantity (TPA)','GST Paid']].sum()
            df['GST Number'] = df['GST Number'].str.strip()
        elif(select.lower()=='b'):
            p1 = df.groupby(by=["Name of Entity",'Financial Year','Plastic Material Type','Category of Plastic','Recycled Plastic %','Other Plastic Material Type','Cat-1 Container Capacity'], dropna=False)[['Quantity (TPA)','GST Paid']].sum()
        else:
            print('Enter valid option')
            sys.exit()
    elif(typee2.lower()== 'b'):
        if(select.lower()=='a'):
            p1 = df.groupby(by=["Name of Entity",'Financial Year','Plastic Material Type','Category of Plastic','GST Number','Invoice Number','Recycled Plastic %','Other Plastic Material Type','Cat-1 Container Capacity','month'], dropna=False)[['Quantity (TPA)','GST Paid']].sum()
            df['GST Number'] = df['GST Number'].str.strip()
        elif(select.lower()=='b'):
            p1 = df.groupby(by=["Name of Entity",'Financial Year','Plastic Material Type','Category of Plastic','Invoice Number', 'Recycled Plastic %','Other Plastic Material Type','Cat-1 Container Capacity','month'], dropna=False)[['Quantity (TPA)','GST Paid']].sum()
        else:
            print('Enter valid option')
            sys.exit()
    else:
        print('Enter valid option')
        sys.exit()
        
        
    p1 = pd.DataFrame(p1)
    p1 =p1.reset_index()
    pivot_name = parent_dir+'/'+'pivot_table.xlsx'
    p1.to_excel(pivot_name, index=False)
    df.to_excel(path4+'base_file.xlsx')
    start = time.time()
    sss=[]
    for i in range(len(p1)):
        if(typee2.lower()== 'b'):
            if(select.lower()=='b'):
                dff = df[(df['Name of Entity']==p1['Name of Entity'][i]) & (df['Recycled Plastic %']==p1['Recycled Plastic %'][i]) & (df['Financial Year']==p1['Financial Year'][i]) & (df['Plastic Material Type']==p1['Plastic Material Type'][i]) & (df['Category of Plastic']==p1['Category of Plastic'][i]) & (df['Other Plastic Material Type']==p1['Other Plastic Material Type'][i]) & (df['Cat-1 Container Capacity']==p1['Cat-1 Container Capacity'][i])& (df['month']==p1['month'][i]) & (df['Invoice Number']==p1['Invoice Number'][i])]
            elif(select.lower()=='a'):
                dff = df[(df['Name of Entity']==p1['Name of Entity'][i]) & (df['Recycled Plastic %']==p1['Recycled Plastic %'][i]) & (df['Financial Year']==p1['Financial Year'][i]) & (df['Plastic Material Type']==p1['Plastic Material Type'][i]) & (df['Category of Plastic']==p1['Category of Plastic'][i])  & (df['Other Plastic Material Type']==p1['Other Plastic Material Type'][i])& (df['GST Number']==p1['GST Number'][i])& (df['Cat-1 Container Capacity']==p1['Cat-1 Container Capacity'][i])& (df['month']==p1['month'][i]) & (df['Invoice Number']==p1['Invoice Number'][i])]
        elif(typee2.lower()== 'a'):
            if(select.lower()=='b'):
                dff = df[(df['Name of Entity']==p1['Name of Entity'][i]) & (df['Recycled Plastic %']==p1['Recycled Plastic %'][i]) & (df['Financial Year']==p1['Financial Year'][i]) & (df['Plastic Material Type']==p1['Plastic Material Type'][i]) & (df['Category of Plastic']==p1['Category of Plastic'][i]) & (df['Other Plastic Material Type']==p1['Other Plastic Material Type'][i]) & (df['Cat-1 Container Capacity']==p1['Cat-1 Container Capacity'][i])]
            elif(select.lower()=='a'):
                dff = df[(df['Name of Entity']==p1['Name of Entity'][i]) & (df['Recycled Plastic %']==p1['Recycled Plastic %'][i]) & (df['Financial Year']==p1['Financial Year'][i]) & (df['Plastic Material Type']==p1['Plastic Material Type'][i]) & (df['Category of Plastic']==p1['Category of Plastic'][i])  & (df['Other Plastic Material Type']==p1['Other Plastic Material Type'][i])& (df['GST Number']==p1['GST Number'][i])& (df['Cat-1 Container Capacity']==p1['Cat-1 Container Capacity'][i])]
        index = np.arange(1, len(dff) + 1)
        dff.insert(0, "S NO", index, True)
        dff.loc['Total'] = pd.Series(dff['Quantity (TPA)'].sum(), index=['Quantity (TPA)'])
        dff['GST Paid'].iloc[[-1]] = dff['GST Paid'].sum()
        dff['S NO'] = dff['S NO'].fillna(0)
        dff['S NO']=dff['S NO'].astype(int)
        dff=dff.reset_index()
        dff = dff.drop(['index'], axis=1)
        dff['S NO'][len(dff)-1]=dff['S NO'][len(dff)-1]='TOTAL'
        dff['Recycled Plastic %']=dff['Recycled Plastic %'].fillna(0)
        
        dff['Recycled Plastic %']=dff['Recycled Plastic %'].astype(float)
        dff['Recycled Plastic %']=dff['Recycled Plastic %'].astype(int)
        dff['Recycled Plastic %'] = dff['Recycled Plastic %'].astype(str)
        dff['Cat-1 Container Capacity'] = dff['Cat-1 Container Capacity'].astype(str)

        if(typee2.lower()== 'b'):
            if(select.lower()=='b'):
                filename = (str(p1['Name of Entity'][i]) + str(p1['Financial Year'][i]) + str(p1['Plastic Material Type'][i]) + str(p1['Category of Plastic'][i])+str(p1['Recycled Plastic %'][i])+str(p1['Other Plastic Material Type'][i]) +str(p1['Cat-1 Container Capacity'][i])+str(p1['month'][i])+str(p1['Invoice Number'][i])).replace('.','-').replace('<','').replace('>','')
            elif(select.lower()=='a'):
                filename = (str(p1['Name of Entity'][i]) + str(p1['Financial Year'][i]) + str(p1['Plastic Material Type'][i]) + str(p1['Category of Plastic'][i]) + str(p1['GST Number'][i])+str(p1['Recycled Plastic %'][i])+str(p1['Other Plastic Material Type'][i])+str(p1['Cat-1 Container Capacity'][i])+str(p1['month'][i])+str(p1['Invoice Number'][i])).replace('.','-').replace('<','').replace('>','')
        elif(typee2.lower()== 'a'):
            if(select.lower()=='b'):
                filename = (str(p1['Name of Entity'][i]) + str(p1['Financial Year'][i]) + str(p1['Plastic Material Type'][i]) + str(p1['Category of Plastic'][i])+str(p1['Recycled Plastic %'][i])+str(p1['Other Plastic Material Type'][i]) +str(p1['Cat-1 Container Capacity'][i])).replace('.','-').replace('<','').replace('>','')
            elif(select.lower()=='a'):
                filename = (str(p1['Name of Entity'][i]) + str(p1['Financial Year'][i]) + str(p1['Plastic Material Type'][i]) + str(p1['Category of Plastic'][i]) + str(p1['GST Number'][i])+str(p1['Recycled Plastic %'][i])+str(p1['Other Plastic Material Type'][i])+str(p1['Cat-1 Container Capacity'][i])).replace('.','-').replace('<','').replace('>','')
    
        sss.append(filename)
        filename = filename.replace('-'," ")
        filename = filename.replace('/'," ")
        filenameexcel = path1+filename +'.xlsx'
        filenamepdf = path2+filename +'.pdf'
        dff = dff.fillna('')
        dff=dff.replace('nan','')
        dff['Recycled Plastic %'].iloc[[-1]] = ' '
        
        dff['GST Paid'] = dff['GST Paid'].astype(str)
#         if 'Country' in dff.columns:
#             dff = dff.drop(['Cat-1 Container Capacity', 'Recycled Plastic %', 'GST Number', 'GST Paid'], axis=1)
#         else:
#             pass
        print(dff)
    #     ss=dff.to_html(na_rep="",index = False).replace('<th>','<th style="background-color: grey">')
    #     with open("test.html", "w") as file:
    #         file.write(ss)
    #     dff.to_excel(filenameexcel, index=False)
    
        writer_2= pd.ExcelWriter(filenameexcel, engine= 'xlsxwriter')
        dff.to_excel(writer_2, index=False, sheet_name= 'Invoice')
        workbook_2 = writer_2.book
        worksheet_2 = writer_2.sheets['Invoice']
        fmt_header = workbook_2.add_format({
         'bold': True,
         'text_wrap': True,
         'valign': 'centre',
    #      'halign': 'centre',
         'fg_color': '#002060',
         'font_color': '#FFFFFF',
         'border': 1})
        format1 = workbook_2.add_format({"num_format": "#,##0.00000"})
        #Setting the zoom
        worksheet_2.set_zoom(80)
        for col , value in enumerate(dff.columns.values):
            worksheet_2.write(0, col, value, fmt_header)
        worksheet_2.set_column(11, 11, None, format1)
        writer_2.close()
##        writer_2.save()
        try:
            xlsx2html(filenameexcel, 'output.html')
        except:
            ex = pd.read_excel(filenameexcel, keep_default_na=False)
            ex.columns = [x.lower() for x in ex.columns]
            ln=len(ex)
            for j in range(ln):
                ex['address'][j] = ex['address'][j].encode('utf-8')
            ex.to_excel(filenameexcel, index=False)
            xlsx2html(filenameexcel, 'output.html')
            
        with open("output.html", 'r', encoding='utf-8') as file:
            file = file.read()
        file = file.replace("none", "1")
        file = file.replace('<table  style="border-collapse: collapse" border="0" cellspacing="0" cellpadding="0">','<table  style="border-collapse: collapse" border="1" cellspacing="0" cellpadding="0">')
        file = file.replace('cellpadding="0">','cellpadding="1">')
        file = file.replace(': 19pt">',': 19pt;text-align: center">')
        with open("output.html", "w", encoding='utf-8') as file_to_write:
            file_to_write.write(file)
            
        r = pdfkit.PDFKit('output.html', 'html',verbose=True,configuration=config,options=options)
        output = r.to_pdf(filenamepdf)
    
    os.remove("output.html")
    end = time.time()
    print("The time of execution of program is :",
          (end-start), "s")
    print(sss)
    

def pdf_merge():
    now = datetime.datetime.now()

    directory = str(now.strftime("merge_"+"%d-%m-%Y %H-%M-%S")) 
    parent_dir = Path.cwd()
    path = os.path.join(parent_dir, directory)

    os.mkdir(path)

    directory3 = "merge"
      
    parent_dir = path.replace('\\','/')
      
    path3 = os.path.join(parent_dir, directory3)

    os.mkdir(path3)
    path3 = path3.replace('\\','/') + '/'
    
    path4 = path.replace('\\','/')+'/'
    
    root = tk.Tk()
    file1 = fd.askopenfilenames(parent=root, title='Choose invoice pdf')
    file2 = fd.askopenfilenames(parent=root, title='Choose statement pdf')
    root.destroy()
    l1=[]
    l2=[]
    for i in range(len(file1)):
        filename1 = os.path.basename(file1[i]).split('.pdf')[0]
        filename1 = filename1.split('.PDF')[0]
        l1.append(filename1)
    for i in range(len(file2)):
        filename2 = os.path.basename(file2[i]).split('.pdf')[0]
        filename2 = filename2.split('.PDF')[0]
        l2.append(filename2)
    df2 = pd.DataFrame({'file1': l1})
    df3 = pd.DataFrame({'file2': l2})
    root = tk.Tk()
    excel = fd.askopenfilename(parent=root, title='Choose invoice and staement excel')
    root.destroy()
    df1= pd.read_excel(excel, keep_default_na=False)
    a=[]
    b=[]
    for i in range(len(df1)):
        try:
            print(i)
            mergedObject = PdfMerger()
            i1=df2.index[df2['file1'] == str(df1['invoice_pdf'][i])][0]
            mergedObject.append(PdfReader(file1[i1], strict=False))
            i2=df3.index[df3['file2'] == str(df1['statement_pdf'][i])][0]
            mergedObject.append(PdfReader(file2[i2], strict=False))
    ##        filename = df1['invoice_pdf'][i]+' '+df1['settlement_pdf'][i]
            filename = df1['statement_pdf'][i]
    ##        filename = filename.replace('-'," ")
            filename = filename.replace('/'," ")
            filenamemerge = path3+filename+'.pdf'
            mergedObject.write(filenamemerge)
        except:
            a.append(df1['invoice_pdf'][i])
            b.append(df1['statement_pdf'][i])
    data = {'invoice_pdf':a,
            'statement_pdf':b}
    df = pd.DataFrame(data)
    if(len(df)==0):
        pass
    else:
        df.to_excel(path4+"errors.xlsx")

    print("File Generated successfully at",path3)


def create_excel ():
    now = datetime.datetime.now()
    root = tk.Tk()
    file1 = fd.askopenfilename(parent=root, title='Choose a pivot file')
    file2 = fd.askopenfilename(parent=root, title='Choose base file')
    root.destroy()

    df1 = pd.read_excel(file1, keep_default_na=False)
    df2 = pd.read_excel(file2, keep_default_na=False)
    df3=df2.copy()
    df2['Name of Entity'] = df2['Name of Entity'].str.strip()
    df2['Financial Year'] = df2['Financial Year'].str.strip()
    df2['Plastic Material Type'] = df2['Plastic Material Type'].str.strip()
    df2['Plastic Material Type']=df2['Plastic Material Type'].str.upper()
    df2['Category of Plastic'] = df2['Category of Plastic'].str.strip()
    df2['GST Number'] = df2['GST Number'].str.strip()
    df2['Name of Entity'] = df2['Name of Entity'].str.upper()
    df2['Financial Year'] = df2['Financial Year'].str.upper()
    df2['Category of Plastic'] = df2['Category of Plastic'].str.upper()
    df1['Name of Entity'] = df1['Name of Entity'].str.strip()
    df1['Financial Year'] = df1['Financial Year'].str.strip()
    df1['Plastic Material Type'] = df1['Plastic Material Type'].str.strip()
    df1['Plastic Material Type']=df1['Plastic Material Type'].str.upper()
    df1['Category of Plastic'] = df1['Category of Plastic'].str.strip()
    df1['GST Number'] = df1['GST Number'].str.strip()
    df1['Name of Entity'] = df1['Name of Entity'].str.upper()
    df1['Financial Year'] = df1['Financial Year'].str.upper()
    df1['Category of Plastic'] = df1['Category of Plastic'].str.upper()
    try:
        df2['GST Number'] = df2['GST Number'].str.upper()
        df1['GST Number'] = df1['GST Number'].str.upper()
    except:
        pass
    a=[]
    b=[]
    c=[]
    d=[]
    e=[]
    f=[]
    g=[]
    h=[]
    fy=[]
    j=[]
    k=[]
    l=[]
    m=[]
    n=[]
    o=[]
    p=[]
    q=[]
    r=[]
    s=[]
    t=[]
    u=[]
    o1=[]

    select = easygui.enterbox('Select one.\na) Pivot table WITH GST Number\nb) Pivot table WITHOUT GST Number')

    for i in range(len(df1)):
        try:
            if(select.lower()=='a'):
                ind=df2[(df2['Name of Entity']==df1['Name of Entity'][i]) & (df2['Recycled Plastic %']==df1['Recycled Plastic %'][i]) & (df2['Financial Year']==df1['Financial Year'][i]) & (df2['Plastic Material Type']==df1['Plastic Material Type'][i]) & (df2['Category of Plastic']==df1['Category of Plastic'][i])  & (df2['Other Plastic Material Type']==df1['Other Plastic Material Type'][i])& (df2['GST Number']==df1['GST Number'][i])& (df2['Cat-1 Container Capacity']==df1['Cat-1 Container Capacity'][i])& (df2['month']==df1['month'][i]) & (df2['Invoice Number']==df1['Invoice Number'][i])].index.values[0]
                #GST Number
                try:
                    m.append(df1['GST Number'][i])
                except:
                    m.append(' ')
            elif(select.lower()=='b'):
                ind=df2[(df2['Name of Entity']==df1['Name of Entity'][i]) & (df2['Recycled Plastic %']==df1['Recycled Plastic %'][i]) & (df2['Financial Year']==df1['Financial Year'][i]) & (df2['Plastic Material Type']==df1['Plastic Material Type'][i]) & (df2['Category of Plastic']==df1['Category of Plastic'][i])  & (df2['Other Plastic Material Type']==df1['Other Plastic Material Type'][i]) & (df2['Cat-1 Container Capacity']==df1['Cat-1 Container Capacity'][i])& (df2['month']==df1['month'][i]) & (df2['Invoice Number']==df1['Invoice Number'][i])].index.values[0]
                #GST Number
                try:
                    m.append(df2['GST Number'][ind])
                except:
                    m.append(' ')
            else:
                print('choose correct option')
                break

            #Invoice Number
            try:
                o.append(df1['Invoice Number'][i])
            except:
                o.append(' ')

            #Month
            try:
                o1.append(df1['month'][i])
            except:
                o1.append(' ')
            
            #pdf_filename
            try:
                if(select.lower()=='a'):
                    p.append(((df1['Name of Entity'][i]) + str(df1['Financial Year'][i]) + str(df1['Plastic Material Type'][i]) + str(df1['Category of Plastic'][i]) + str(df1['GST Number'][i]) + str(df1['Recycled Plastic %'][i]) + str(df1['Other Plastic Material Type'][i]) + str(df1['Cat-1 Container Capacity'][i]) + str(df1['Invoice Number'][i]) + str(df1['month'][i])).replace('.','-').replace('<','').replace('>',''))
                elif(select.lower()=='b'):
                    p.append(((df1['Name of Entity'][i]) + str(df1['Financial Year'][i]) + str(df1['Plastic Material Type'][i]) + str(df1['Category of Plastic'][i]) + str(df1['Recycled Plastic %'][i]) + str(df1['Other Plastic Material Type'][i]) + str(df1['Cat-1 Container Capacity'][i]) + str(df1['Invoice Number'][i]) + str(df1['month'][i])).replace('.','-').replace('<','').replace('>',''))
                else:
                    print('choose correct option')
                    break
            except:
                p.append(' ')
                    
        except:
            if(select.lower()=='a'):
                ind=df2[(df2['Name of Entity']==df1['Name of Entity'][i]) & (df2['Recycled Plastic %']==df1['Recycled Plastic %'][i]) & (df2['Financial Year']==df1['Financial Year'][i]) & (df2['Plastic Material Type']==df1['Plastic Material Type'][i]) & (df2['Category of Plastic']==df1['Category of Plastic'][i])  & (df2['Other Plastic Material Type']==df1['Other Plastic Material Type'][i])& (df2['GST Number']==df1['GST Number'][i])& (df2['Cat-1 Container Capacity']==df1['Cat-1 Container Capacity'][i])].index.values[0]
                #GST Number
                try:
                    m.append(df1['GST Number'][i])
                except:
                    m.append(' ')
            elif(select.lower()=='b'):
                ind=df2[(df2['Name of Entity']==df1['Name of Entity'][i]) & (df2['Recycled Plastic %']==df1['Recycled Plastic %'][i]) & (df2['Financial Year']==df1['Financial Year'][i]) & (df2['Plastic Material Type']==df1['Plastic Material Type'][i]) & (df2['Category of Plastic']==df1['Category of Plastic'][i])  & (df2['Other Plastic Material Type']==df1['Other Plastic Material Type'][i]) & (df2['Cat-1 Container Capacity']==df1['Cat-1 Container Capacity'][i])].index.values[0]
                #GST Number
                try:
                    m.append(df2['GST Number'][ind])
                except:
                    m.append(' ')
            else:
                print('choose correct option')
                break
            #Invoice Number
            try:
                o.append(df2['Invoice Number'][ind])
            except:
                o.append(' ')

            #Month
            try:
                o1.append(df2['month'][ind])
            except:
                o1.append(' ')
            
            #pdf_filename
            try:
                if(select.lower()=='a'):
                    p.append(((df1['Name of Entity'][i]) + str(df1['Financial Year'][i]) + str(df1['Plastic Material Type'][i]) + str(df1['Category of Plastic'][i]) + str(df1['GST Number'][i]) + str(df1['Recycled Plastic %'][i]) + str(df1['Other Plastic Material Type'][i]) + str(df1['Cat-1 Container Capacity'][i])).replace('.','-').replace('<','').replace('>',''))
                elif(select.lower()=='b'):
                    p.append(((df1['Name of Entity'][i]) + str(df1['Financial Year'][i]) + str(df1['Plastic Material Type'][i]) + str(df1['Category of Plastic'][i]) + str(df1['Recycled Plastic %'][i]) + str(df1['Other Plastic Material Type'][i]) + str(df1['Cat-1 Container Capacity'][i])).replace('.','-').replace('<','').replace('>',''))
                else:
                    print('choose correct option')
                    break
            except:
                p.append(' ')
        
        #Registration Type
        try:
            a.append(df2['Registration Type'][ind])
        except:
            a.append(' ')
            
        #Entity Type
        try:
            b.append(df2['Entity Type'][i])
        except:
            b.append(' ')
        
        #Name of Entity
        try:
            c.append(df1['Name of Entity'][i])
        except:
            c.append(' ')
            
        #State
        try:
            d.append(df2['State'][ind])
        except:
            d.append(' ')
        
        #Address
        try:
            e.append(df2['Address'][ind])
        except:
            e.append(' ')
        
        #Mobile Number
        try:
            f.append(df2['Mobile Number'][ind])
        except:
            f.append(' ')
        
        #Plastic Material Type
        try:
            g.append(df1['Plastic Material Type'][i])
        except:
            g.append(' ')
        
        #Category of Plastic
        try:
            h.append(df1['Category of Plastic'][i])
        except:
            h.append(' ')
        
        #Financial Year
        try:
            fy.append(df1['Financial Year'][i])
        except:
            fy.append(' ')
        
        #Date of invoice
        try:
            j.append(df2['Date of invoice'][ind])
        except:
            j.append(' ')
        
        #Quantity (TPA)
        try:
            k.append(df1['Quantity (TPA)'][i])
        except:
            k.append('0')
        
        #Recycled Plastic %
        try:
            l.append(df1['Recycled Plastic %'][i])
        except:
            l.append(0)
        
##        #GST Number
##        try:
##            m.append(df1['GST Number'][i])
##        except:
##            m.append(' ')
        
        #GST Paid
        try:
            n.append(df1['GST Paid'][i])
        except:
            n.append(0)
        
##        #Invoice Number
##        try:
##            o.append(df1['Invoice Number'][i])
##        except:
##            o.append(' ')
##
##        #Month
##        try:
##            o1.append(df1['month'][i])
##        except:
##            o1.append(' ')
##        
##        #pdf_filename
##        try:
##            if(select.lower()=='a'):
##                p.append(((df1['Name of Entity'][i]) + str(df1['Financial Year'][i]) + str(df1['Plastic Material Type'][i]) + str(df1['Category of Plastic'][i]) + str(df1['GST Number'][i]) + str(df1['Recycled Plastic %'][i]) + str(df1['Other Plastic Material Type'][i]) + str(df1['Cat-1 Container Capacity'][i]) + str(df1['Invoice Number'][i]) + str(df1['month'][i])).replace('.','-').replace('<','').replace('>',''))
##            elif(select.lower()=='b'):
##                p.append(((df1['Name of Entity'][i]) + str(df1['Financial Year'][i]) + str(df1['Plastic Material Type'][i]) + str(df1['Category of Plastic'][i]) + str(df1['Recycled Plastic %'][i]) + str(df1['Other Plastic Material Type'][i]) + str(df1['Cat-1 Container Capacity'][i]) + str(df1['Invoice Number'][i]) + str(df1['month'][i])).replace('.','-').replace('<','').replace('>',''))
##            else:
##                print('choose correct option')
##                break
##        except:
##            p.append(' ')
        
        #Other Plastic Material Type
        try:
            q.append(df1['Other Plastic Material Type'][i])
        except:
            q.append(' ')
        
        #Cat-1 Container Capacity
        try:
            r.append(df1['Cat-1 Container Capacity'][i])
        except:
            r.append(0)
        
        #Country
        try:
            s.append(df2['Country'][ind])
        except:
            s.append(' ')
        
        #Bank account no
        try:
            t.append(df2['Bank account no'][ind])
        except:
            t.append(' ')
        
        #IFSC code
        try:
            u.append(df2['IFSC code'][ind])
        except:
            u.append(' ')
        
        
        

    df = pd.DataFrame({
                       'Registration Type': a,
                       'Entity Type': b,
                       'Name of Entity': c,
                       'State': d,
                       'Address': e,
                       'Mobile Number': f,
                       'Plastic Material Type': g,
                       'Category of Plastic': h,
                       'Financial Year': fy,
                       'Date of invoice': j,
                       'Quantity (TPA)': k,
                       'Recycled Plastic %': l,
                       'GST Number': m,
                       'GST Paid': n,
                       'Invoice Number': o,
                       'pdf_filename': p,
                       'Other Plastic Material Type': q,
                       'Cat-1 Container Capacity': r,
                       'Country': s,
                       'Bank account no': t,
                       'IFSC code': u,
                       })
    
    df['pdf_filename'] = [x.replace('-'," ") for x in df['pdf_filename']]
    df['pdf_filename'] = [x.replace('/'," ") for x in df['pdf_filename']]
    filename = str(now.strftime("BOT_"+"%d%m%Y %H%M%S")) +'.xlsx'
    df.to_excel(filename)
    print('FILE CREATED WITH NAME- ' + filename)





import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tkinter as tk
import tkinter.filedialog as fd
import getpass
import time
import pandas as pd
import tkinter as tk
import easygui
from pathlib import Path
import datetime
import os
import math
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from PyPDF2 import PdfMerger,PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from selenium.webdriver.common.action_chains import ActionChains


def hello ():
    global errors
    global invoicee
    global roww
    global driver
    today = date.today()
    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Edge()
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get('https://eprplastic.cpcb.gov.in/#/plastic/home')
    time.sleep(1)
    
    mail = easygui.enterbox("Enter Email ")
    passs = easygui.enterbox("Enter Password")
    action = ActionChains(driver)
    action.click(on_element = driver.find_element(by=By.XPATH, value='//*[@id="username"]')).perform()
    action.click(on_element = driver.find_element(by=By.XPATH, value='//*[@id="password"]')).perform()
    driver.find_element(by=By.XPATH, value='//*[@id="username"]').send_keys(mail)
    driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(passs)


    errors = []
    invoicee = []
    roww=[]
    c=-1

def ahead3():
    global errors
    global invoicee
    global driver
    global roww
    driver = driver
    login_select = easygui.enterbox('with which id you want to proceed?\na) PRODUCER\nb) BRAND OWNER \nc) IMPORTER')
    driver.implicitly_wait(15)
    errors = []
    invoicee = []
    c=-1
    start = time.time()
    if(login_select.lower() =="a"):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/producer-list')
        driver.refresh()
        producer()
    elif(login_select.lower() =="b"):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/bo-list')
        driver.refresh()
        brand_owner()
    elif(login_select.lower() =="c"):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/importer-list')
        driver.refresh()
        importer()
    else:
        print("PLEASE ENTER CORRECT CHOICE")
    end = time.time()
    print("The time of execution of program is :",
      (end-start), "s")
    error()

def error():
    global df
    now = datetime.datetime.now()
    df.to_excel('errors_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')


def custom_wait_clickable_and_click(elem, attempts=20):
    count = 0
    a='no success'
    while count < attempts:
        try:
            if(a!='success'):
                elem.click()
                a='success'
            elif(a=='success'):
                break
        except:
            time.sleep(1)
            count = count + 1


def pdf_gen(a,b,c,d,e,f,g,h,i,j):
    my_doc = SimpleDocTemplate("table.pdf", pagesize = letter)
    my_obj = []
    # defining Data to be stored on table
    my_data = [
       ["Information", 'Details'],
       ["EPR Invoice no.", a],
       ["Customer Registeration Type", b],
       ["Entity Type", c],
       ["Name of Entity", d],
       ["Plastic Material Type", e],
       ["Other Plastic Material Type", f],
       ["Category of Plastic", g],
       ["Financial Year", h],
       ["Quantity (TPA)", i],
       ["GST Paid", j],
    ]
    # Creating the table with 3 rows
    my_table = Table(my_data, 1 * [3.5 * inch], 11 * [0.5 * inch])
    # setting up style and alignments of borders and grids
    my_table.setStyle(
       TableStyle(
           [
               
               ("ALIGN", (-1, -1), (-1, -1), "LEFT"),
               ("VALIGN", (-1, -1), (-1, -1), "BOTTOM"),
               ("ALIGN", (-1, -1), (-1, -1), "LEFT"),
               ("VALIGN", (-1, -1), (-1, -1), "BOTTOM"),
               ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
               ("BOX", (0, 0), (-1, -1), 1, colors.black),
               ('BACKGROUND',(0,0),(1,0),colors.lightblue),
           ]
       )
    )
    my_obj.append(my_table)
    my_doc.build(my_obj)

           


def producer():
    global roww
    global invoi
    invoi=[]
    global df
    global mail
    global errors
    global invoicee
    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    root.destroy()
    if(select.lower()=='a'):
        root = tk.Tk()
#         file = fd.askopenfilename(parent=root, title='Choose a record file')
        file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
        root.destroy()
        df1 = pd.DataFrame(list(file2), columns =['file_path'])
        df1['file_name']=0
        for i in range(len(df1)):
            file2 = df1['file_path'][i].split("/")
            file_name = file2[-1].split(".pdf")[0]
            df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})

#     now = datetime.datetime.now()
#     val = (str(mail), "producer",str(select),str(len(df)),str(now.strftime("%d/%m/%Y %H-%M-%S")))
#     mycursor.execute(sql, val)
#     mydb.commit()
    
    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    df['bank account no'] = df['bank account no'].str.strip()
    df = df.fillna(0)
    df = df.replace('', 0)
    count=0
    try:
        df.upload_status
    except:
        df['upload_status'] = "no" 
    if(select.lower()=='b'):
        df['epr invoice number'] = "na"
        invoice=[]
        i=-1
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
        time.sleep(2)
        while i < len(df)-1:
#         while(i==0):
            driver.implicitly_wait(20)
            i=i+1
            print(i)
            #Add button
            try:
                time.sleep(1)
                click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
                custom_wait_clickable_and_click(click)
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                custom_wait_clickable_and_click(add)
                time.sleep(1)

                #registration type nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
                    cl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                except:
                    errors.append('registeration error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                if(df['registration type'][i].lower()=='registered'):
                    #Type
                    cl = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/div[2]/input')))
                    custom_wait_clickable_and_click(cl)


                    #financial year
                    try:
                        fy=14
                        time.sleep(0.5)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                        fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div').text)
    #                     time.sleep(0.5)
                    except:
                        errors.append('financial year error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

##                    #GST nn
##                    try:
##                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['gst number'][i])
##                    except:
##                        errors.append('GST error')
##                        invoicee.append(str(df['invoice number'][i]))
##                        pass

                    #bank account no 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['bank account no'][i])
                    except:
                        errors.append('bank account no error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #ifsc code 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['ifsc code'][i])
                    except:
                        errors.append('ifsc code error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #gst paid
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['gst paid'][i])
                    except:
                        errors.append('gst paid error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #Total Quantity (Tons)
                    try:
                        qty = round(float(df['quantity (tpa)'][i]), 3)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(qty)
                    except:
                        errors.append('Total Quantity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #invoice number
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[15]/div/input').send_keys(df['invoice number'][i])
                    except:
                        errors.append('invoice number error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #category of plastic
                    try:
                        if(df['category of plastic'][i].lower()=='cat iv'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                    #% of recycled plastic packaging
                            try:
                                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(str(df['recycled plastic %'][i]))
                            except:
                                errors.append('% of recycled plastic packaging error')
                                invoicee.append(str(df['invoice number'][i]))
                                pass    
                    except:
                        errors.append('category of plastic error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #entity type
                    try:
                        if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                            #cat-1 container capacity nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)

                    except:
                        errors.append('entity type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass
                

                    #plastic material type
                    try:
                        if(df['plastic material type'][i].lower()=='others'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
                            time.sleep(0.5)
                            #other plastic material type nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/input').send_keys(df['other plastic material type'][i])
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
                    except:
                        errors.append('plastic material type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass
                
                    #Name of the Entity Unregistered
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/div/div/div[2]/input').send_keys(str(df['name of entity'][i]).strip())
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass


                    #address nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').clear()
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/input').send_keys('xyz')
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    time.sleep(1)

                    
                    
                    
########################################################################################################################
                else:
                    #Name of the Entity Unregistered nn
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/input').send_keys(df['name of entity'][i])
                        else:
                            pass
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #address nn
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/input').send_keys(df['address'][i])
                        else:
                            pass
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #state nn
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            time.sleep(0.5)
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                            cl=WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(2)
                        else:
                            pass
                    except:
                        errors.append('state error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #mobile number nn 
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                        else:
                            pass
                    except:
                        errors.append('mobile number error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #financial year nn
                    try:
                        fy=14
                        time.sleep(0.5)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                        fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div').text)
    #                     time.sleep(0.5)
                    except:
                        errors.append('financial year error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #GST nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys(df['gst number'][i])
                    except:
                        errors.append('GST error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #bank account no nn 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['bank account no'][i])
                    except:
                        errors.append('bank account no error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #ifsc code nn 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['ifsc code'][i])
                    except:
                        errors.append('ifsc code error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #gst paid nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['gst paid'][i])
                    except:
                        errors.append('gst paid error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #Total Quantity (Tons) nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[1]/div/input').send_keys(df['quantity (tpa)'][i])
                    except:
                        errors.append('Total Quantity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #invoice number nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['invoice number'][i])
                    except:
                        errors.append('invoice number error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #category of plastic nn
                    try:
                        if(df['category of plastic'][i].lower()=='cat iv'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                    #% of recycled plastic packaging nn
                            try:
                                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div[2]/div/input').send_keys(str(df['recycled plastic %'][i]))
                            except:
                                errors.append('% of recycled plastic packaging error')
                                invoicee.append(str(df['invoice number'][i]))
                                pass    
                    except:
                        errors.append('category of plastic error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #entity type nn
                    try:
                        if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                            #cat-1 container capacity nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)

                    except:
                        errors.append('entity type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass


                    #plastic material type nn
                    try:
                        if(df['plastic material type'][i].lower()=='others'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div')))
                            custom_wait_clickable_and_click(cl)
                            time.sleep(0.5)
                            #other plastic material type nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/input').send_keys(df['other plastic material type'][i])
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
                    except:
                        errors.append('plastic material type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass



                
                
#                 break
                #Submit nn
                try:
                    if(fy<14):
#                         import pyperclip
                        #genrate epr invoice number
                        cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[3]/button')))
                        custom_wait_clickable_and_click(cl)

                        #confirm button
                        cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/div/div/div/div[3]/button[2]')))
                        custom_wait_clickable_and_click(cl)

                        #copy epr-e invoice number
                        try:
                            cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/div[1]/div[1]/button')))
                            custom_wait_clickable_and_click(cl)
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/div[1]/div[1]/input').text
                            inv = pyperclip.paste()
                            df['upload_status'][i] = "yes"
                            df['epr invoice number'][i] = inv
                            invoi.append(inv)
                        except:
                            invoi.append('none')

                        #close window
##                        cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button')))
##                        custom_wait_clickable_and_click(cl)
                        driver.refresh()
                        
                    
                except:
#                 try:
                    errors.append('Confirm error')
                    invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
                    try:
                        close = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button')))
                        custom_wait_clickable_and_click(close)
                    except:
                        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
                        time.sleep(3)
            except:
                invoi.append('none')
                driver.refresh()
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                custom_wait_clickable_and_click(add)
                driver.refresh()
                driver.implicitly_wait(15)
##                driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
                time.sleep(3)
##                i=i-1
##        df['epr invoice number'] =0
##        df['epr invoice number'] = invoi
##        df.to_excel('new.xlsx') #creating new excel with the use of main excel
    
    



    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------     
    elif(select=='a'):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
        time.sleep(5)
        df['date of invoice']=df['date of invoice'].astype(str)
        i=-1
        time.sleep(2)
        while i < len(df)-1:
            driver.implicitly_wait(15)
            i=i+1
            print(i)
            #Add button nn
            try:
                time.sleep(1)
                click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
                custom_wait_clickable_and_click(click)
                driver.implicitly_wait(15)
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                                            
                custom_wait_clickable_and_click(add)
##                time.sleep(0.5)
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
                r_select = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(r_select)
    #             except:
    #                 errors.append('add button error')
    #                 pass

                #entity type nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                    time.sleep(0.5)
                    et=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(et)
#                     time.sleep(1.5)
                except:
                    errors.append('entity type error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Name of the Entity unregistred
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[3]/div/input').send_keys(df['name of entity'][i])
                    #driver.find_element(by=By.XPATH, value='').click()
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #state nn
                try:
                    time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(2)
                except:
                    errors.append('state error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #address nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #mobile number nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                except:
                    errors.append('mobile number error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #category of plastic nn
                try:
                    if(df['category of plastic'][i].lower()=='cat iv'):
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(1.5)
                    else:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(1.5)
                #% of recycled plastic packaging nn
                        try:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(str(df['recycled plastic %'][i]))
                        except:
                            errors.append('% of recycled plastic packaging error')
                            invoicee.append(str(df['invoice number'][i]))
                            pass    
                except:
                    errors.append('category of plastic error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #financial year nn
                try:
                    fy=14
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/span[1]').click()
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
                    fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div').text)
#                     time.sleep(0.5)
                except:
                    errors.append('financial year error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #DATE nn
                try:
                    a = str(df['date of invoice'][i])[:8]
                    d = a[:4]+'/'+a[4:6]+'/'+a[6:]
                    datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
                    datetime1 = datetime0.date()
                    datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Total Plastic Quantity nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #GST nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(df['gst number'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #gst paid nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['gst paid'][i]))
                except:
                    errors.append('gst paid error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #invoice number nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[15]/div/input').send_keys(df['invoice number'][i])
                except:
                    errors.append('invoice number error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Upload Invoice / GST E-Invoice nn
                try:
                    upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
                    pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
                    pdf_file = df1['file_path'][pdf_file_index]
                    upload_file.send_keys(pdf_file)
                    time.sleep(1)

                except:
                    errors.append('Invoice upload error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #plastic material type nn
                try:
                    if(df['plastic material type'][i].lower()=='others'):
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
                        #other plastic material type nn
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/input').send_keys(df['other plastic material type'][i])
                    else:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
                except:
                    errors.append('plastic material type error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass
#                 break
                #Submit
                try:
                    if(fy<14):
                        cl=WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
                        custom_wait_clickable_and_click(cl)
                        try:
                            driver.implicitly_wait(1)
                            close = driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[1]/button/span').click()
                            errors.append('Submit error')
                            invoicee.append(str(df['invoice number'][i]))
#                             roww.append(i+2)
                        except:
                            df['upload_status'][i] = "yes" 
                            pass
                        time.sleep(0.5)
                    else:
                        df['upload_status'][i] = "no"
                        raise error
                except:
                    df['upload_status'][i] = "no"
                    errors.append('Submit error')
                    invoicee.append(str(df['invoice number'][i]))
                    close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(close)
                    time.sleep(1)
                    pass
            except:
                df['upload_status'][i] = "no"
                driver.refresh()
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                custom_wait_clickable_and_click(add)
                driver.refresh()
                driver.implicitly_wait(15)
##                driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
                time.sleep(2)
##                i=i-1
                pass
            



def pdf_upload():
    global errors
    global invoicee
    global roww
    now = datetime.datetime.now()
    directory = str(now.strftime("final_pdf"+"%d%m%Y %H%M%S"))
    parent_dir = Path.cwd()
    path = os.path.join(parent_dir, directory)

    os.mkdir(path)  
    parent_dir = path.replace('\\','/')
    parent_dir


    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a newly created record file')
    files = fd.askopenfilenames(parent=root, title='Choose merged pdf files')
    root.destroy()
    df = pd.DataFrame(list(files), columns =['file_path'])
    df1 = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
    df1.columns = (x.lower() for x in df1.columns)
    df['file_name']=0
    for i in range(len(df)):
        file2 = df['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0].split(".PDF")[0]
        df['file_name'][i]=file_name
    for i in range(len(df1)):
        print(i)
        pdf_gen(df1['epr invoice number'][i], df1['registration type'][i], df1['entity type'][i], df1['name of entity'][i], df1['plastic material type'][i], df1['other plastic material type'][i], df1['category of plastic'][i], df1['financial year'][i], round(df1['quantity (tpa)'][i], 3), df1['gst paid'][i])
        #plastic packaging qty, %of recyl plastic
        #remove entity type
        mergedObject = PdfMerger()
        mergedObject.append(PdfReader("table.pdf", 'rb'))
        pdf_file_index = df[df['file_name']==df1['pdf_filename'][i]].index[0]
        mergedObject.append(PdfReader(df['file_path'][pdf_file_index], 'rb'))
        filename = parent_dir+'/'+df1['pdf_filename'][i] + '.pdf'
        mergedObject.write(filename)

    print("ALL FILES GENERATED SUCCESSFULLY, PLEASE CHECK YOUR FOLDER-",parent_dir)

def pdf_upload2():
    driver.implicitly_wait(3)
    global errors
    global invoicee
    errors = []
    invoicee = []
    #Finding epr invoice number using scrapping
    ssa=easygui.enterbox("OPEN THE PAGE ON PORTAL WHERE YOU WANT TO UPLOAD PDF AND THEN PRESS OK")
    job=driver.find_element(by=By.ID, value='ScrollableSimpleTableBody')
    soup=BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
    a=soup.find_all("span",class_="ng-star-inserted")
    z=[]
    for i in a:
    #     print(i.text.replace("\n","").strip())
        z.append(i.text.replace("\n","").strip())

    EPR=[]

    i=0
    while i<len(z):
        EPR.append(z[i+14])
        i=i+19

    df3 = pd.DataFrame({
                   'epr_no': EPR,
                   })
    print(df3)
    
    #Upload Invoice / GST E-Invoice
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
    root.destroy()
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        file_name = file_name.split(".PDF")[0]
        df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})
    for i in range(0,50):
    # for i in range(1):
        try:
            IndexForUpload = df[df['epr invoice number']==int(df3['epr_no'][i])].index[0]
            click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr['+str(i+1)+']/td[17]/span')))
            custom_wait_clickable_and_click(click)
            upload_file = driver.find_element(by=By.XPATH, value='//*[@id="salesInvoiceUpload"]')
            pdfindex = df1[df1['file_name']==str(df['pdf_filename'][IndexForUpload])].index[0]
            pdf_file = df1['file_path'][pdfindex]
            upload_file.send_keys(pdf_file)
            time.sleep(2)
            upload = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[3]/div/div/div[3]/button[1]')))
            custom_wait_clickable_and_click(upload)                              
            time.sleep(1)
        except:
            errors.append('Invoice upload error')
            invoicee.append(str(df['Invoice Number'][i]))
            try:
                close = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[3]/div/div/div[3]/button[2]').click()
            except:
                pass


def brand_owner():
    global errors
    global invoicee
    global roww
    global roww
    driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
    root.destroy()
    df1 = pd.DataFrame(list(file2), columns =['file_path'])
    df1['file_name']=0
    for i in range(len(df1)):
        file2 = df1['file_path'][i].split("/")
        file_name = file2[-1].split(".pdf")[0]
        df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})

#     now = datetime.datetime.now()
#     val = (str(mail), "brand_owner",'',str(len(df)),str(now.strftime("%d/%m/%Y %H-%M-%S")))
#     mycursor.execute(sql, val)
#     mydb.commit()
    
    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    df['date of invoice']=df['date of invoice'].astype(str)
    #     df['date of invoice'] = df['date of invoice'].apply(lambda x: x.replace("-", "/"))
    driver.implicitly_wait(15)
    i=-1
    df = df.fillna(0)
    df = df.replace('', 0)
    try:
        df.upload_status
    except:
        df['upload_status'] = "no" 
    while i < len(df)-1:
        driver.implicitly_wait(15)
        i=i+1
        print(i)
        #Add button
        try:
            time.sleep(1)
            click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
            custom_wait_clickable_and_click(click)
            driver.implicitly_wait(15)
            add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
            custom_wait_clickable_and_click(add)
            time.sleep(0.5)
            r_click = driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys('unregistered')
            r_select = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/ng-dropdown-panel/div/div[2]/div')))
            custom_wait_clickable_and_click(r_select)

    #         except:
    #             errors.append('add button error')
    #             break



            #Name of the Entity unregistred
            try:
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[3]/div/input').send_keys(df['name of entity'][i])
                #driver.find_element(by=By.XPATH, value='').click()
            except:
                errors.append('Name of the Entity error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #state
            try:
                time.sleep(0.5)
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                cl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(cl)
#                 time.sleep(2)
            except:
                errors.append('state error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #address
            try:
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
            except:
                errors.append('Name of the Entity error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #mobile number
            try:
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
            except:
                errors.append('mobile number error')
                invoicee.append(str(df['invoice number'][i]))
                pass



            #financial year
            try:
                fy=21
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(cl)
                fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div').text)
#                 time.sleep(0.5)
            except:
                errors.append('financial year error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #DATE
            try:
                a = str(df['date of invoice'][i])[:8]
                d = a[:4]+'/'+a[4:6]+'/'+a[6:]
                datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
                datetime1 = datetime0.date()
                datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
            except:
                errors.append('GST error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #Total Plastic Quantity
            try:
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
            except:
                errors.append('GST error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #GST
            try:
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(df['gst number'][i])
            except:
                errors.append('GST error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #gst paid
            try:
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['gst paid'][i]))
            except:
                errors.append('gst paid error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #invoice number
            try:
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[15]/div/input').send_keys(df['invoice number'][i])
            except:
                errors.append('invoice number error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #Upload Invoice / GST E-Invoice
            try:
                upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
                pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
                pdf_file = df1['file_path'][pdf_file_index]
                upload_file.send_keys(pdf_file)
                time.sleep(1)

            except:
                errors.append('Invoice upload error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #category of plastic
            try:
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                cl=driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')
                custom_wait_clickable_and_click(cl)

            except:
                errors.append('category of plastic error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            #entity type
            try:
                if(df['category of plastic'][i].lower()=='cat i'):
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1.5)
                    #cat-1 container capacity
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1)
                else:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1.5)

            except:
                errors.append('entity type error')
                invoicee.append(str(df['invoice number'][i]))
                pass
            
            
            #financial year
            try:
                if(df['category of plastic'][i].lower()!='cat i'):
                    fy=21
                    time.sleep(0.5)
                    cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/span[1]')))
                    custom_wait_clickable_and_click(cl)
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
                    fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div').text)
    #                 time.sleep(0.5)
                else:
                    fy=21
                    time.sleep(0.5)
                    cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/div/span[1]')))
                    custom_wait_clickable_and_click(cl)
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
                    fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/ng-select/div').text)
    #                 time.sleep(0.5)
            except:
                errors.append('financial year error')
                invoicee.append(str(df['invoice number'][i]))
                pass
            
            

            #plastic material type
            try:
                time.sleep(1)
                if(df['plastic material type'][i].lower()=='others'):
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                    #other plastic material type
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/input').send_keys(df['other plastic material type'][i])

                else:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
            except:
                errors.append('plastic material type error')
                invoicee.append(str(df['invoice number'][i]))
                pass

            try:
                if(df['plastic material type'][i].lower()=='others' and df['category of plastic'][i].lower()=='cat i'):
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(datetime2)
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['recycled plastic %'][i]))
                elif(df['plastic material type'][i].lower()=='others' and df['category of plastic'][i].lower()!='cat i'):
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(datetime2)
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(str(df['recycled plastic %'][i]))
                    except:
                        pass
                elif(df['category of plastic'][i].lower()=='cat i' and df['plastic material type'][i].lower()!='others'):
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(datetime2)
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(str(df['recycled plastic %'][i]))
                    except:
                        pass
                else:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(str(df['recycled plastic %'][i]))
                    except:
                        pass
            except:
                pass
 
            #Submit
            try:
                if(fy<21):
                    cl=WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
                    custom_wait_clickable_and_click(cl)
                    time.sleep(0.5)
                    try:
                        driver.implicitly_wait(1)
                        driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/div/div[2]/div').click()
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[1]/button/span').click()
                        df['upload_status'][i] = "no" 
                        errors.append('Submit error')
                        invoicee.append(str(df['invoice number'][i]))
    #                     roww.append(i+2)
                    except:
                        df['upload_status'][i] = "yes" 
                        pass
                    time.sleep(0.5)
                else:
                    df['upload_status'][i] = "no"
                    raise error
            except:
                df['upload_status'][i] = "no"
                errors.append('Submit error')
                invoicee.append(str(df['invoice number'][i]))
                close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
                custom_wait_clickable_and_click(close)
        except:
            df['upload_status'][i] = "no"
            driver.refresh()
            add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
            custom_wait_clickable_and_click(add)
            driver.refresh()
            driver.implicitly_wait(15)
##            driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
            time.sleep(2)
##            i=i-1
            pass
            
            


        

def importer():
    global roww
    global invoi
    invoi=[]
    global df
    global mail
    global errors
    global invoicee
    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    root.destroy()
    if(select.lower()=='a'):
        root = tk.Tk()
#         file = fd.askopenfilename(parent=root, title='Choose a record file')
        file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
        root.destroy()
        df1 = pd.DataFrame(list(file2), columns =['file_path'])
        df1['file_name']=0
        for i in range(len(df1)):
            file2 = df1['file_path'][i].split("/")
            file_name = file2[-1].split(".pdf")[0]
            df1['file_name'][i]=file_name
    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str,'Bank account no':str,'Quantity (TPA)':float})

#     now = datetime.datetime.now()
#     val = (str(mail), "producer",str(select),str(len(df)),str(now.strftime("%d/%m/%Y %H-%M-%S")))
#     mycursor.execute(sql, val)
#     mydb.commit()

    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    df['bank account no'] = df['bank account no'].str.strip()
    count=0
    df = df.fillna(0)
    df = df.replace('', 0)
    try:
        df.upload_status
    except:
        df['upload_status'] = "no" 
    if(select.lower()=='b'):
        df['epr invoice number'] = "na"
        invoice=[]
        i=-1
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
        time.sleep(2)
        while i < len(df)-1:
#         while(i==0):
            driver.implicitly_wait(20)
            i=i+1
            print(i)
            #Add button
            try:
                time.sleep(1)
                click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
                custom_wait_clickable_and_click(click)
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                custom_wait_clickable_and_click(add)
                time.sleep(1)

                #registration type nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
                    cl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[1]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(0.5)
                except:
                    errors.append('registeration error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                if(df['registration type'][i].lower()=='registered'):
                    #Type
                    cl = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/div[2]/input')))
                    custom_wait_clickable_and_click(cl)


                    #financial year
                    try:
                        fy=14
                        time.sleep(0.5)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                        fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div').text)
    #                     time.sleep(0.5)
                    except:
                        errors.append('financial year error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #GST nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['gst number'][i])
                    except:
                        errors.append('GST error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #bank account no 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['bank account no'][i])
                    except:
                        errors.append('bank account no error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #ifsc code 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['ifsc code'][i])
                    except:
                        errors.append('ifsc code error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #gst paid
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['gst paid'][i])
                    except:
                        errors.append('gst paid error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #Total Quantity (Tons)
                    try:
                        qty = round(float(df['quantity (tpa)'][i]), 5)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div/div/input').send_keys(qty)
                    except:
                        errors.append('Total Quantity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #invoice number
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[15]/div/input').send_keys(df['invoice number'][i])
                    except:
                        errors.append('invoice number error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #category of plastic
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(1.5)
                    except:
                        errors.append('category of plastic error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #entity type
                    try:
                        if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                            #cat-1 container capacity nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)

                    except:
                        errors.append('entity type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass
                

                    #plastic material type
                    try:
                        if(df['plastic material type'][i].lower()=='others'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
                            time.sleep(0.5)
                            #other plastic material type nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/input').send_keys(df['other plastic material type'][i])
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
                    except:
                        errors.append('plastic material type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass
                
                    #Name of the Entity Unregistered
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/div/div/div[2]/input').send_keys(str(df['name of entity'][i]).strip())
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    time.sleep(1)
                    
                    
########################################################################################################################

                else:
                    #Name of the Entity Unregistered nn
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[3]/div/input').send_keys(df['name of entity'][i])
                        else:
                            pass
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #address nn
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[4]/div/input').send_keys(df['address'][i])
                        else:
                            pass
                    except:
                        errors.append('Name of the Entity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #state nn
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            time.sleep(0.5)
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                            cl=WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[5]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(2)
                        else:
                            pass
                    except:
                        errors.append('state error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #mobile number nn 
                    try:
                        if(df['registration type'][i].lower()=='unregistered'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                        else:
                            pass
                    except:
                        errors.append('mobile number error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #financial year nn
                    try:
                        fy=14
                        time.sleep(0.5)
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                        cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
                        fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div').text)
    #                     time.sleep(0.5)
                    except:
                        errors.append('financial year error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #GST nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys(df['gst number'][i])
                    except:
                        errors.append('GST error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #bank account no nn 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['bank account no'][i])
                    except:
                        errors.append('bank account no error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #ifsc code nn 
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys(df['ifsc code'][i])
                    except:
                        errors.append('ifsc code error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #gst paid nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[13]/div/input').send_keys(df['gst paid'][i])
                    except:
                        errors.append('gst paid error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #Total Quantity (Tons) nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[2]/div/div/input').send_keys(("{:f}".format(float(df['quantity (tpa)'][0]))))
                    except:
                        errors.append('Total Quantity error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #invoice number nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[14]/div/input').send_keys(df['invoice number'][i])
                    except:
                        errors.append('invoice number error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #category of plastic nn
                    try:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(1.5)
                    except:
                        errors.append('category of plastic error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass

                    #entity type nn
                    try:
                        if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)
                            #cat-1 container capacity nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['cat-1 container capacity'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1)
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(1.5)

                    except:
                        errors.append('entity type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass


                    #plastic material type nn
                    try:
                        if(df['plastic material type'][i].lower()=='others'):
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
                            time.sleep(0.5)
                            #other plastic material type nn
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[8]/div/input').send_keys(df['other plastic material type'][i])
                        else:
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                            cl=WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                            custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
                    except:
                        errors.append('plastic material type error')
                        invoicee.append(str(df['invoice number'][i]))
                        pass
                
#                 break
                #Submit nn
                try:
                    if(fy<14):
#                         import pyperclip
                        #genrate epr invoice number
                        cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[3]/button')))
                        custom_wait_clickable_and_click(cl)

                        #confirm button
                        cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/div/div/div/div[3]/button[2]')))
                        custom_wait_clickable_and_click(cl)

                        #copy epr-e invoice number
                        try:
                            cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/div[1]/div[1]/button')))
                            custom_wait_clickable_and_click(cl)
                            driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/div[1]/div[1]/input').text
                            inv = pyperclip.paste()[2:-2]
                            df['upload_status'][i] = "yes"
                            df['epr invoice number'][i] = inv
                            invoi.append(inv)
                        except:
                            invoi.append('none')

                        #close window
                        cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button')))
                        custom_wait_clickable_and_click(cl)

                        
                except:
#                 try:
                    errors.append('Confirm error')
                    invoicee.append(str(df['invoice number'][i]))
#                     roww.append(i+2)
                    try:
                        close = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button')))
                        custom_wait_clickable_and_click(close)
                    except:
                        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
                        time.sleep(3)
            except:
                invoi.append('none')
                driver.refresh()
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                custom_wait_clickable_and_click(add)
                driver.refresh()
                driver.implicitly_wait(15)
##                driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
                time.sleep(3)
##                i=i-1
    
    



    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------    
    #----------------------------------------------------------------------------------------------------------------------     
    elif(select=='a'):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
        time.sleep(5)
        df['date of invoice']=df['date of invoice'].astype(str)
        i=-1
        while i < len(df)-1:
            driver.implicitly_wait(15)
            i=i+1
            print(i)
            #Add button nn
            try:
                time.sleep(1)
                click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
                custom_wait_clickable_and_click(click)
                driver.implicitly_wait(15)
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                                            
                custom_wait_clickable_and_click(add)
##                time.sleep(0.5)
                driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/div/div/div[2]/input').send_keys(df['registration type'][i])
                r_select = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                custom_wait_clickable_and_click(r_select)
    #             except:
    #                 errors.append('add button error')
    #                 pass

                #entity type nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/div/div/div[2]/input').send_keys(df['entity type'][i])
                    time.sleep(0.5)
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[2]/div/ng-select/ng-dropdown-panel/div/div[2]/div')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(1.5)
                except:
                    errors.append('entity type error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Name of the Entity unregistred
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[3]/div/input').send_keys(df['name of entity'][i])
                    #driver.find_element(by=By.XPATH, value='').click()
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #country nn
                try:
                    time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/ng-select/div/div/div[2]/input').send_keys(df['state'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                     time.sleep(2)
                except:
                    errors.append('state error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #address nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[5]/div/input').send_keys(df['address'][i])
                except:
                    errors.append('Name of the Entity error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #mobile number nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[6]/div/input').send_keys(str(df['mobile number'][i])[:10])
                except:
                    errors.append('mobile number error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #category of plastic nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/div/div/div[2]/input').send_keys(df['category of plastic'][i])
                    cl=WebDriverWait(driver, 10).until(
EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
#                         time.sleep(1.5)
                except:
                    errors.append('category of plastic error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #financial year nn
                try:
                    fy=14
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/span[1]').click()
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div/div/div[2]/input').send_keys(df['financial year'][i])
                    cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/ng-dropdown-panel/div/div[2]/div[1]')))
                    custom_wait_clickable_and_click(cl)
                    fy=len(driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[9]/div/ng-select/div').text)
#                     time.sleep(0.5)
                except:
                    errors.append('financial year error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #DATE nn
                try:
                    a = str(df['date of invoice'][i])[:8]
                    d = a[:4]+'/'+a[4:6]+'/'+a[6:]
                    datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
                    datetime1 = datetime0.date()
                    datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[10]/div/input').send_keys(datetime2)
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Total Plastic Quantity nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[11]/div/input').send_keys(df['quantity (tpa)'][i])
                except:
                    errors.append('GST error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

#                 #GST nn
#                 try:
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[13]/div/input').send_keys(df['gst number'][i])
#                 except:
#                     errors.append('GST error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #gst paid nn
#                 try:
#                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[14]/div/input').send_keys(str(df['gst paid'][i]))
#                 except:
#                     errors.append('gst paid error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

                #invoice number nn
                try:
                    driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[12]/div/input').send_keys(df['invoice number'][i])
                except:
                    errors.append('invoice number error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #Upload Invoice / GST E-Invoice nn
                try:
                    upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
                    pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
                    pdf_file = df1['file_path'][pdf_file_index]
                    upload_file.send_keys(pdf_file)
                    time.sleep(1)

                except:
                    errors.append('Invoice upload error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass

                #plastic material type nn
                try:
                    if(df['plastic material type'][i].lower()=='others'):
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
                        #other plastic material type nn
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[8]/div/input').send_keys(df['other plastic material type'][i])
                    else:
                        driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/div/div/div[2]/input').send_keys(df['plastic material type'][i])
                        cl=WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/div/div[7]/div/ng-select/ng-dropdown-panel/div/div[2]/div')))
                        custom_wait_clickable_and_click(cl)
#                         time.sleep(0.5)
                except:
                    errors.append('plastic material type error')
                    invoicee.append(str(df['invoice number'][i]))
                    pass
#                 break
                #Submit
                try:
                    if(fy<14):
                        cl=WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form/div/form/button')))
                        custom_wait_clickable_and_click(cl)
                        try:
                            driver.implicitly_wait(1)
                            close = driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[1]/button/span').click()
                            errors.append('Submit error')
                            invoicee.append(str(df['invoice number'][i]))
#                             roww.append(i+2)
                        except:
                            df['upload_status'][i] = "yes" 
                            pass
                        time.sleep(0.5)
                    else:
                        df['upload_status'][i] = "no"
                        raise error
                except:
                    df['upload_status'][i] = "no"
                    errors.append('Submit error')
                    invoicee.append(str(df['invoice number'][i]))
                    close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
                    custom_wait_clickable_and_click(close)
                    time.sleep(1)
                    pass
            except:
                df['upload_status'][i] = "no"
                driver.refresh()
                add = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
                custom_wait_clickable_and_click(add)
                driver.refresh()
                driver.implicitly_wait(15)
                time.sleep(2)
##                i=i-1
                pass
            
            


####################################################################################################################################################################################


def get_details():
    job=driver.find_element(by=By.ID, value='ScrollableSimpleTableBody')
    soup=BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
    a=soup.find_all("span",class_="ng-star-inserted")
    z=[]
    for i in a:
    #     print(i.text.replace("\n","").strip())
        z.append(i.text.replace("\n","").strip())

    gstpaid=[]
    invoice_no=[]

    i=0
    while i<len(z):
        gstpaid.append(z[i+13])
        invoice_no.append(z[i+15])
        i=i+19

    df3 = pd.DataFrame({
                   'gstpaid': gstpaid,
                   'invoice_no': invoice_no,
                   })
    df3['gstpaid'] = df3['gstpaid'].map(lambda x: round(float(x), 4))
    return df3

def delete_items():
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose Records deletion File')
    root.destroy()
    df = pd.read_excel(file, converters={'Invoice Number':str})
    df['GST Paid'] = df['GST Paid'].map(lambda x: round(float(x), 4))
    for _ in range(50):
        time.sleep(1)
        df3 = get_details()
        i=0
        while i<50:
            IndexForUpload = df[(df['GST Paid']==df3['gstpaid'][i]) & (df['Invoice Number']==df3['invoice_no'][i])].index
            IndexForUpload=list(IndexForUpload)
            if(len(IndexForUpload)>0):
                binn = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr['+str(i+1)+']/td[19]/span')
                custom_wait_clickable_and_click(binn)
                yes = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[2]/div/div/div[2]/button[1]')
                time.sleep(1)
                custom_wait_clickable_and_click(yes)
                click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
                custom_wait_clickable_and_click(click)
                time.sleep(0.5)
                df3 = get_details()
            else:
                i=i+1
        nextt = driver.find_elements(by=By.CLASS_NAME, value='action-button')[1]
        custom_wait_clickable_and_click(nextt)
        click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
        custom_wait_clickable_and_click(click)





####################################################################################################################################################################################

def scrape():
    ssa=easygui.enterbox('What you want to scrape? Select one option -\na) Data Entry\nb) Credit Transactions')
    if(ssa.lower()=='a'):
        a2,b,c,d,e,f,g,h,i2,j,k,l,m,n,o,p=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        stop=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/kl-simple-table-with-pagination/div[1]/div/div[2]/table/tbody/tr/td/div[1]/div/span').text
        res = [int(i) for i in stop.split() if i.isdigit()]
        stop=res[-1]
        stop=stop/50
        stop=math.ceil(stop)
        print(stop)
        count=0
        df = pd.DataFrame()
        while count<stop:
            a2,b,c,d,e,f,g,h,i2,j,k,l,m,n,o,p=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
            try:
                time.sleep(1)
                count=count+1
                job=driver.find_element(by=By.ID, value='ScrollableSimpleTableBody')
                soup=BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
                a=soup.find_all("span",class_="ng-star-inserted")
                if(len(a)==0):
                    a=soup.find_all("td",class_="row-item")
                z=[]
                for i in a:
                #     print(i.text.replace("\n","").strip())
                    z.append(i.text.replace("\n","").strip())
                i=0
                if(count==stop):
                    while i<len(z):
                        a2.append(z[i])
                        b.append(z[i+1])
                        c.append(z[i+2])
                        d.append(z[i+3])
                        e.append(z[i+4])
                        f.append(z[i+5])
                        g.append(z[i+6])
                        h.append(z[i+7])
                        i2.append(z[i+8])
                        j.append(z[i+9])
                        k.append(z[i+10])
                        l.append(z[i+11])
                        m.append(z[i+12])
                        n.append(z[i+13])
                        o.append(z[i+14])
                        p.append(z[i+15])
                        if((len(z[16])==0) & (len(z[17])==0) & (len(z[18])==0)):
                            i=i+19
                        elif(len(z[16])==0 and len(z[17])==0):
                            i=i+18
                        else:
                            i=i+16
                        print(i)
                    df1 = pd.DataFrame({
                               'Registration Type': a2,
                               'Entity Type': b,
                               'Name of the Entity': c,
                               'State': d,
                               'Address': e,
                               'Mobile Number': f,
                               'Plastic Material Type': g,
                               'Category of Plastic': h,
                               'Financial Year': i2,
                               'Date': j,
                               'Total Plastic Qty (Tons)': k,
                               'Recycled Plastic %': l,
                               'GST': m,
                               'GST Paid': n,
                               'EPR invoice No': o,
                               'GST E-Invoice No': p,
                               })
                    df = pd.concat([df, df1],ignore_index=True)

                else:
                    while i<len(z):
                        a2.append(z[i])
                        b.append(z[i+1])
                        c.append(z[i+2])
                        d.append(z[i+3])
                        e.append(z[i+4])
                        f.append(z[i+5])
                        g.append(z[i+6])
                        h.append(z[i+7])
                        i2.append(z[i+8])
                        j.append(z[i+9])
                        k.append(z[i+10])
                        l.append(z[i+11])
                        m.append(z[i+12])
                        n.append(z[i+13])
                        o.append(z[i+14])
                        p.append(z[i+15])
                        if((len(z[16])==0) & (len(z[17])==0) & (len(z[18])==0)):
                            i=i+19
                        elif(len(z[16])==0 and len(z[17])==0):
                            i=i+18
                        else:
                            i=i+16
                        print(i)
                    df1 = pd.DataFrame({
                               'Registration Type': a2,
                               'Entity Type': b,
                               'Name of the Entity': c,
                               'State': d,
                               'Address': e,
                               'Mobile Number': f,
                               'Plastic Material Type': g,
                               'Category of Plastic': h,
                               'Financial Year': i2,
                               'Date': j,
                               'Total Plastic Qty (Tons)': k,
                               'Recycled Plastic %': l,
                               'GST': m,
                               'GST Paid': n,
                               'EPR invoice No': o,
                               'GST E-Invoice No': p,
                               })
                    if(count==1):
                        comp= pd.DataFrame({'aa':['0']})
                    else:
                        new = df.tail(50).reset_index()
                        new = new.drop(['index'], axis=1)
                        comp=new.compare(df1)
                    if(comp.empty==False):
                        df = pd.concat([df, df1],ignore_index=True)
                        nextt = driver.find_elements(by=By.CLASS_NAME, value='action-button')[1]
                        custom_wait_clickable_and_click(nextt)
                        click = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[3]/div/div/div/div/div[2]/input')
                        custom_wait_clickable_and_click(click)
                        time.sleep(1)
                    else:
                        df.to_excel('Scrapped_Data_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
                        break
            except:
                break
        now = datetime.datetime.now()
        df.to_excel('Scrapped_Data_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        print("Your file is generated by name - "+'Scrapped_Data_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        
    elif(ssa.lower()=='b'):
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-wallet')
        time.sleep(5)
        driver.implicitly_wait(15)
        a2,b,c,d,e,f,g,h,i2,j,k,l,m,n,o,p=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        x=1
        while True:
            try:
                sno=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-wallet/div[1]/div/section[2]/div/div[3]/div/div[2]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr['+str(x)+']/td[1]').text
                date=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-wallet/div[1]/div/section[2]/div/div[3]/div/div[2]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr['+str(x)+']/td[2]/span').text
                credit=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-wallet/div[1]/div/section[2]/div/div[3]/div/div[2]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr['+str(x)+']/td[5]/span').text
                click=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-wallet/div[1]/div/section[2]/div/div[3]/div/div[2]/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody/tr['+str(x)+']/td[8]/span/span/em').click()
                # try:     
                job=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-wallet/div[2]/div/div/div[2]/div/div/kl-simple-table-with-pagination/div[1]/div/div[1]/table/tbody')
                soup=BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
                a=soup.find_all("span",class_="ng-star-inserted")
                z=[]
                for i in a:
                    z.append(i.text.replace("\n","").strip())
                i=0
                while i<len(z):
                    a2.append(sno)
                    b.append(date)
                    c.append(credit)
                    d.append(z[i])
                    e.append(z[i+1])
                    f.append(z[i+2])
                    g.append(z[i+3])
                    h.append(z[i+4])
                    i2.append(z[i+5])
                    j.append(z[i+6])
                    k.append(z[i+7])
                    l.append(z[i+8])
                    m.append(z[i+9])
                    n.append(z[i+10])
                    o.append(z[i+11])
                    p.append(z[i+12])
                    i=i+15
                df = pd.DataFrame({
                           'SL.No': a2,
                           'Date': b,
                           'Credited From': c,
                           'Certificate ID': d,
                           'Value': e,
                           'Certificate Owner': f,
                           'Category': g,
                           'Processing Type': h,
                           'Transaction ID': i2,
                           'Available Potential Prior Generation': j,
                           'Available Potential After Generation': k,
                           'Used Potential Prior Generation': l,
                           'Used Potential After Generation': m,
                           'Cumulative Potential': n,
                           'Generated At': o,
                           'Validity': p,
                           })
                time.sleep(1)
                close=driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-wallet/div[2]/div/div/div[1]/button/span').click()
                x+=1
            except:
                break
        now = datetime.datetime.now()
        df.to_excel('Scrapped_CT_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        print("Your file is generated by name - "+'Scrapped_CT_'+str(now.strftime("%d%m%Y %H%M%S"))+'.xlsx')
        
    else:
        print("Please choose correct option.")
def Format():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
        "Registration Type": ["Type1", "Type2"],
        "Entity Type": ["Entity1", "Entity2"],
        "Name of Entity": ["Name1", "Name2"],
        "State": ["State1", "State2"],
        "Address": ["Address1", "Address2"],
        "Mobile Number": ["1234567890", "0987654321"],
        "Plastic Material Type": ["Type1", "Type2"],
        "Category of Plastic": ["Cat1", "Cat2"],
        "Financial Year": ["2023-24", "2024-25"],
        "Date of invoice": ["2023-01-01", "2023-06-01"],
        "Quantity (TPA)": [10, 20],
        "Recycled Plastic %": [50, 60],
        "GST Number": ["GST123", "GST456"],
        "GST Paid": [1000, 2000],
        "Invoice Number": ["INV123", "INV456"],
        "pdf_filename": ["file1.pdf", "file2.pdf"],
        "Other Plastic Material Type": ["OtherType1", "OtherType2"],
        "Cat-1 Container Capacity": [100, 200],
        "Country": ["Country1", "Country2"],
        "Bank account no": ["ACC123", "ACC456"],
        "IFSC code": ["IFSC123", "IFSC456"]
    }

    df = pd.DataFrame(data)
    excel_filename = 'Base_Data_Format.xlsx'
    df.to_excel(excel_filename, index=False)
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")

def Format2():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
        "Registration Type": ["Type1", "Type2"],
        "Entity Type": ["Entity1", "Entity2"],
        "Name of Entity": ["Name1", "Name2"],
        "State": ["State1", "State2"],
        "Address": ["Address1", "Address2"],
        "Mobile Number": ["1234567890", "0987654321"],
        "Plastic Material Type": ["Type1", "Type2"],
        "Category of Plastic": ["Cat1", "Cat2"],
        "Financial Year": ["2023-24", "2024-25"],
        "Date of invoice": ["2023-01-01", "2023-06-01"],
        "Quantity (TPA)": [10, 20],
        "Recycled Plastic %": [50, 60],
        "GST Number": ["GST123", "GST456"],
        "GST Paid": [1000, 2000],
        "Invoice Number": ["INV123", "INV456"],
        "pdf_filename": ["file1.pdf", "file2.pdf"],
        "Other Plastic Material Type": ["OtherType1", "OtherType2"],
        "Cat-1 Container Capacity": [100, 200],
        "Country": ["Country1", "Country2"],
        "Bank account no": ["ACC123", "ACC456"],
        "IFSC code": ["IFSC123", "IFSC456"],
        "epr invoice number":["EInv1","EINV2"]
    }

    df = pd.DataFrame(data)
    excel_filename = 'Info_Format.xlsx'
    df.to_excel(excel_filename, index=False)
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")

def Format3():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
        "GST Paid": [1000, 2000],
        "Invoice Number": ["INV123", "INV456"],
##        "pdf_filename": ["file1.pdf", "file2.pdf"],
##        "Other Plastic Material Type": ["OtherType1", "OtherType2"],
##        "Cat-1 Container Capacity": [100, 200],
##        "Country": ["Country1", "Country2"],
##        "Bank account no": ["ACC123", "ACC456"],
##        "IFSC code": ["IFSC123", "IFSC456"],
##        "epr invoice number":["EInv1","EINV2"]
    }

    df = pd.DataFrame(data)
    excel_filename = 'Delete_Format.xlsx'
    df.to_excel(excel_filename, index=False)
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")

##root= tk.Tk()
##
##canvas1 = tk.Canvas(root, width = 180, height = 80)
##canvas1.pack()
##canvas5 = tk.Canvas(root, width = 180, height = 80)
##canvas5.pack()
##canvas6 = tk.Canvas(root, width = 180, height = 80)
##canvas6.pack()
##canvas4 = tk.Canvas(root, width = 180, height = 80)
##canvas4.pack()
##canvas2 = tk.Canvas(root, width = 180, height = 80)
##canvas2.pack()
##canvas7 = tk.Canvas(root, width = 180, height = 80)
##canvas7.pack()
##canvas3 = tk.Canvas(root, width = 180, height = 150)
##canvas3.pack()
##
##
##
##button1 = tk.Button(text='open browser', command=hello, bg='brown',fg='white')
##canvas1.create_window(75, 75, window=button1)
##button5 = tk.Button(text='Generate pdfs', command=pdf_upload, bg='brown',fg='white')
##canvas5.create_window(75, 75, window=button5)
##button6 = tk.Button(text='Upload pdfs', command=pdf_upload2, bg='brown',fg='white')
##canvas6.create_window(75, 75, window=button6)
##button4 = tk.Button(text='Continue Data Entry', command=ahead3, bg='brown',fg='white')
##canvas4.create_window(75, 75, window=button4)
##button2 = tk.Button(text='show errors', command=error, bg='brown',fg='white')
##canvas2.create_window(75, 75, window=button2)
##button7 = tk.Button(text='Delete Records', command=delete_items, bg='brown',fg='white')
##canvas7.create_window(75, 75, window=button7)
##button3 = tk.Button(text='Scrape details', command=scrape, bg='brown',fg='white')
##canvas3.create_window(75, 75, window=button3)
##
##
##
##root.mainloop()

def about():
    messagebox.showinfo("About", "Contact A A GARG AND CO. for the license.")

def quit_app():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()

from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter import messagebox
import os


root = Tk()
root.title("EPR SYNC")
##root.iconbitmap(default=r)
root.geometry("750x500")
root.configure(bg="#FFFFFF")
root.resizable(width=True, height=True)

# Create a menu bar
menubar = Menu(root)
root.config(menu=menubar)

# Create a File menu
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=file_menu)
Excel_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Excel Format", menu=Excel_menu)

file_menu.add_command(label="Quit", command=quit_app)
file_menu.add_command(label="About", command=about)
Excel_menu.add_command(label="Base Data_Format", command=Format)
Excel_menu.add_command(label="Info Sheet", command=Format2)
Excel_menu.add_command(label="Delete Format", command=Format3)

img = Image.open("src/img/main image.png")
img = img.resize((750, 500), Image.LANCZOS)
img = ImageTk.PhotoImage(img)
panel = Label(root, image=img)
panel.image = img
panel.pack()
##
##img = Image.open("main image.png")
##img = img.resize((250, 250), Image.LANCZOS)
##img = ImageTk.PhotoImage(img)
##panel = Label(root, image=img)
##panel.image = img
##panel.pack()
##panel.place(x=600, y=0)

##btn1 = Button(root, text='Refine excel', command=refine, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn1.place(x=100, y=320)
##btn2 = Button(root, text='create invoices', command=hello2, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn2.place(x=220, y=320)
##btn3 = Button(root, text='create upload file', command=create_excel, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn3.place(x=365, y=320)
##btn4 = Button(root, text='merge pdfs', command=pdf_merge, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn4.place(x=530, y=320)
##btn5 = Button(root, text='open browser', command=hello, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn5.place(x=130, y=370)
##btn6 = Button(root, text='Continue Data Entry', command=ahead3, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn6.place(x=260, y=370)
##btn7 = Button(root, text='Generate pdfs(sales)', command=pdf_upload, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn7.place(x=445, y=370)
##btn8 = Button(root, text='Upload pdfs(sales)', command=pdf_upload2, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn8.place(x=80, y=420)
##btn9 = Button(root, text='Scrape details', command=scrape, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn9.place(x=255, y=420)
##btn10 = Button(root, text='show errors', command=error, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn10.place(x=390, y=420)
##btn11 = Button(root, text='Delete Records', command=delete_items, bg='#0A0D15', fg='black', font=('Verdana', 12))
##btn11.place(x=505, y=420)
def on_click(event):
    hello()

btn_width = 1 * 10  # Adjust this multiplier as needed
btn_height = 2

btn1 = Button(root, text='Refine File', command=refine, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn1.place(x=40, y=320)
btn2 = Button(root, text='Generate Invoices', command=hello2, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn2.place(x=160, y=320)
btn3 = Button(root, text='create upload file', command=create_excel, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn3.place(x=40, y=385)
btn4 = Button(root, text='merge pdfs', command=pdf_merge, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn4.place(x=160, y=385)

lbl_clickable_text = tk.Label(root, text='open browser', bg='#FFFFFF', fg='black', font=('Verdana', 12), cursor='hand2')
lbl_clickable_text.place(x=310, y=392)
lbl_clickable_text.bind('<Button-1>', on_click)

btn6 = Button(root, text='Data Upload', command=ahead3, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn6.place(x=480, y=320)
btn9 = Button(root, text='Export Data', command=scrape, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn9.place(x=600, y=320)
btn7 = Button(root, text='Generate pdfs(sales)', command=pdf_upload, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn7.place(x=480, y=385)
btn8 = Button(root, text='Upload pdfs(sales)', command=pdf_upload2, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn8.place(x=600, y=385)

btn10 = Button(root, text='show errors', command=error, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn10.place(x=480, y=445)
btn11 = Button(root, text='Delete Records', command=delete_items, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=100)
btn11.place(x=600, y=445)


root.mainloop()















































