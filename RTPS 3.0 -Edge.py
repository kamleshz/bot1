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
import datetime

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
    df.to_excel('newbasefile.xlsx')
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
##    df['Name of Entity'] = df['Name of Entity'].map(lambda x: re.sub(r'[^a-zA-Z0-9\s/\\]+', '', x))
    df['GST Number']=df['GST Number'].str.upper()
    df['Other Plastic Material Type']=df['Other Plastic Material Type'].str.upper()
    now = datetime.now()

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
##    df['month'] = [datetime.datetime.strptime(str(x), "%Y%m%d").date().month for x in df['Date of invoice']]    
    
    df = df[['Registration Type', 'Entity Type','Name of Entity','State','Address','Mobile Number','Plastic Material Type','Category of Plastic','Financial Year', 'Date of invoice', 'Quantity (TPA)','Recycled Plastic %','GST Number','GST Paid','Invoice Number','Other Plastic Material Type','Cat-1 Container Capacity','Bank account no','IFSC code']]
    
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
        df['month'] = [datetime.datetime.strptime(str(x), "%Y%m%d").date().month for x in df['Date of invoice']] 
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
            
        try:
            try:
                with open("output.html") as file:
                    file = file.read()
            except:
                with open("output.html", 'r', encoding='utf-8') as file:
                    file = file.read()
        except:
                with open("output.html", 'r', encoding='latin-1') as file:
                    file = file.read()
        file = file.replace("none", "1")
        file = file.replace('<table  style="border-collapse: collapse" border="0" cellspacing="0" cellpadding="0">','<table  style="border-collapse: collapse" border="1" cellspacing="0" cellpadding="0">')
        file = file.replace('cellpadding="0">','cellpadding="1">')
        file = file.replace(': 19pt">',': 19pt;text-align: center">')
        try:
            try:
                with open("output.html", "w") as file_to_write:
                    file_to_write.write(file)

            except:
                with open("output.html", 'w', encoding='utf-8') as file_to_write:
                    file_to_write.write(file)

        except:
                with open("output.html", 'w', encoding='latin-1') as file_to_write:
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
            filename = str(df1['invoice_pdf'][i])
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
    df3=df2
    df2['Name of Entity'] = df2['Name of Entity'].str.strip()
    df2['Financial Year'] = df2['Financial Year'].str.strip()
    df2['Plastic Material Type'] = df2['Plastic Material Type'].str.strip()
    df2['Plastic Material Type']=df2['Plastic Material Type'].str.upper()
    df2['Category of Plastic'] = df2['Category of Plastic'].str.strip()
    # df2['GST Number'] = df2['GST Number'].str.strip()
    df2['Name of Entity'] = df2['Name of Entity'].str.upper()
    df2['Financial Year'] = df2['Financial Year'].str.upper()
    df2['Category of Plastic'] = df2['Category of Plastic'].str.upper()
    df1['Name of Entity'] = df1['Name of Entity'].str.strip()
    df1['Financial Year'] = df1['Financial Year'].str.strip()
    df1['Plastic Material Type'] = df1['Plastic Material Type'].str.strip()
    df1['Plastic Material Type']=df1['Plastic Material Type'].str.upper()
    df1['Category of Plastic'] = df1['Category of Plastic'].str.strip()
    # df1['GST Number'] = df1['GST Number'].str.strip()
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

    select = easygui.enterbox('Select one.\na) Pivot table WITH GST Number\nb) Pivot table WITHOUT GST Number')

    for i in range(len(df1)):
        if(select.lower() == 'a'):
            # Check if 'GST Number' exists in both df1 and df2
            if 'GST Number' in df1.columns and 'GST Number' in df2.columns:
                ind = df2[(df2['Name of Entity'] == df1['Name of Entity'][i]) &
                          (df2['Financial Year'] == df1['Financial Year'][i]) &
                          (df2['Plastic Material Type'] == df1['Plastic Material Type'][i]) &
                          (df2['Other Plastic Material Type'] == df1['Other Plastic Material Type'][i]) &
                          (df2['Category of Plastic'] == df1['Category of Plastic'][i]) &
                          (df2['GST Number'] == df1['GST Number'][i]) &
                          (df2['Recycled Plastic %'] == df1['Recycled Plastic %'][i]) &
                          (df2['Cat-1 Container Capacity'] == df1['Cat-1 Container Capacity'][i])].index.values[0]
            else:
                ind = df2[(df2['Name of Entity'] == df1['Name of Entity'][i]) &
                          (df2['Financial Year'] == df1['Financial Year'][i]) &
                          (df2['Plastic Material Type'] == df1['Plastic Material Type'][i]) &
                          (df2['Other Plastic Material Type'] == df1['Other Plastic Material Type'][i]) &
                          (df2['Category of Plastic'] == df1['Category of Plastic'][i]) &
                          (df2['Recycled Plastic %'] == df1['Recycled Plastic %'][i]) &
                          (df2['Cat-1 Container Capacity'] == df1['Cat-1 Container Capacity'][i])].index.values[0]
        elif(select.lower() == 'b'):
            ind = df2[(df2['Name of Entity'] == df1['Name of Entity'][i]) &
                      (df2['Financial Year'] == df1['Financial Year'][i]) &
                      (df2['Plastic Material Type'] == df1['Plastic Material Type'][i]) &
                      (df2['Other Plastic Material Type'] == df1['Other Plastic Material Type'][i]) &
                      (df2['Category of Plastic'] == df1['Category of Plastic'][i]) &
                      (df2['Recycled Plastic %'] == df1['Recycled Plastic %'][i]) &
                      (df2['Cat-1 Container Capacity'] == df1['Cat-1 Container Capacity'][i])].index.values[0]
        else:
            print('choose correct option')
            break
       
        #Registration Type
        try:
            a.append(df2['Registration Type'][ind])
        except:
            a.append(' ')
            
        #Entity Type
        try:
            b.append(df2['Entity Type'][ind])
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
            l.append(df2['Recycled Plastic %'][ind])
        except:
            l.append(0)
        
        #GST Number
        try:
            m.append(df1['GST Number'][i])
        except:
            m.append(' ')
        
        #GST Paid
        try:
            n.append(df1['GST Paid'][i])
        except:
            n.append(0)
        
        #Invoice Number
        try:
            o.append(df2['Invoice Number'][ind])
        except:
            o.append(' ')
        
        #pdf_filename
        try:
            if(select.lower()=='a'):
                p.append((df1['Name of Entity'][i]) + str(df1['Financial Year'][i]) + str(df1['Plastic Material Type'][i]) + str(df1['Category of Plastic'][i]) + str(df1['GST Number'][i]) + str(df1['Recycled Plastic %'][i]) + str(df1['Other Plastic Material Type'][i]) + str(df1['Cat-1 Container Capacity'][i]).replace('.','-').replace('<','').replace('>',''))
            elif(select.lower()=='b'):
                p.append((df1['Name of Entity'][i]) + str(df1['Financial Year'][i]) + str(df1['Plastic Material Type'][i]) + str(df1['Category of Plastic'][i]) + str(df1['Recycled Plastic %'][i]) + str(df1['Other Plastic Material Type'][i]) + str(df1['Cat-1 Container Capacity'][i]).replace('.','-').replace('<','').replace('>',''))
            else:
                print('choose correct option')
                break
        except:
            p.append(' ')
        
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
import requests
import json
import math
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from PyPDF2 import PdfMerger,PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from selenium.webdriver.common.action_chains import ActionChains
from email.message import EmailMessage
##import gspread
##from oauth2client.service_account import ServiceAccountCredentials
##from google.oauth2.service_account import Credentials
from requests.exceptions import ConnectTimeout
import smtplib, ssl
from datetime import datetime, date
from PIL import Image
from tkinter import Button
import platform


def hello ():
    windows_username = os.getlogin()
    global errors, invoicee, roww, driver
    errors = []
    invoicee = []
    roww = []
    c = -1

    today = date.today()
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get('https://eprplastic.cpcb.gov.in/#/plastic/home')
    time.sleep(1)

    # Updated credentials dictionary with entity details

    credentials = {
        "simran.mansukhani@abhishri.co.in": {
            "password": "Packaging@2024",
            "entity_name": "Abhishir Packaging Pvt Ltd",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
            "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"] 
        },
        "ravi.joshi@abhishri.co.in": {
            "password": "Abhi@123",
            "entity_name": "Abhishir Packaging Pvt Ltd",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
            "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Varun@allied-plastics.com": {
            "password": "Global@123",
            "entity_name": "Allied Global",
            "plant": "Daman & Diu",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan",
            "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Vijay@allied-plastics.com": {
            "password": "Propack@123",
            "entity_name": "Allied Propack",
            "plant": "Dadara & Nagar",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "shamuaalparmar@chemcogroup.com": {
            "password": "PrU1@190624",
            "entity_name": "Chemco Unit I",
            "plant": "Gujarat",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Anil.kale@amcor.com": {
            "password": "Rewa@@2583",
            "entity_name": "Amcor Flexibles",
            "plant": "Mumbai",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "yatinkakodkar@apexpacking.in": {
            "password": "Apex@19062024",
            "entity_name": "Apex Packaging",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "info@aquent.in": {
            "password": "AQUENT@may24",
            "entity_name": "Aquent",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "plasticepr@chemcogroup.com": {
            "password": "PrU2@190624",
            "entity_name": "Chemco Unit II",
            "plant": "Silavasa",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "jayantranka@gauravpet.com": {
            "password": "PrGC@190624",
            "entity_name": "Chemco - GCL",
            "plant": "Daman",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Hr@chemcogroup.com": {
            "password": "ImCH@190624",
            "entity_name": "Chemco - IMP",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "SHUBHAM.AGRAWAL@AVGOL.COM": {
            "password": "Mandideep@123",
            "entity_name": "Avgol Non Woven",
            "plant": "Madhya Pradesh",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Sudhir.Singh@avgol.com": {
            "password": "Raisen@2024",
            "entity_name": "Avgol Non Woven",
            "plant": "Gujarat",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "bhattasali@gmail.com": {
            "password": "Bpspl2023!",
            "entity_name": "Bhattasali",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "bo.epr@chemcogroup.com": {
            "password": "ChemcoBO@2024",
            "entity_name": "Chemco Brand Owner",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "prashantgulhane@rmgroup501.com": {
            "password": "Rmc@2023",
            "entity_name": "R M Chemical (HUL 2P)",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Rishik",
            "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "niruban.sam@eplglobal.com": {
            "password": "Epl@Goa@2024",
            "entity_name": "EPL Limited",
            "plant": "Goa",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "jalindar.pokale@eplglobal.com": {
            "password": "Epl@Vasind@2024",
            "entity_name": "EPL Limited",
            "plant": "Vasind",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ram.singh@eplglobal.com": {
            "password": "Epl@Nala@2024",
            "entity_name": "EPL Limited",
            "plant": "Nalagarh",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "tushar.wakale@eplglobal.com": {
            "password": "Epl@Wada@2024",
            "entity_name": "EPL Limited",
            "plant": "Wada",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "dhiraj.mazumder@eplglobal.com": {
            "password": "Epl@Assam@2024",
            "entity_name": "EPL Limited",
            "plant": "Assam",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "miraj.ahir@eplglobal.com": {
            "password": "Epl@Vapi@2024",
            "entity_name": "EPL Limited",
            "plant": "Vapi",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ankush.acharya@eplglobal.com": {
            "password": "Epl@12345",
            "entity_name": "EPL Limited",
            "plant": "Manpura",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "paramananda.parab@eplglobal.com": {
            "password": "Epl@1100",
            "entity_name": "EPL Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "dinesh.paliwal@jaicorpindia.com": {
            "password": "Jaicorp@1234",
            "entity_name": "Jai Corp",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "abbas@parampackaging.com": {
            "password": "Param@123",
            "entity_name": "Param Packaging",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "thillai.mandagini@gmail.com": {
            "password": "Mandagini@2022",
            "entity_name": "Mandagini Seals",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "expo@omblowplastt.com": {
            "password": "Omblow@24",
            "entity_name": "Om Blow Plast",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "himanshu@sai-enterprises.com": {
            "password": "Admin@1234",
            "entity_name": "Sai Enterprises - Pantnagar",
            "plant": "Pantnagar",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "payra.shanti@gmail.com": {
            "password": "Sai@2024",
            "entity_name": "Sai Enterprises - Assam",
            "plant": "Assam",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "spectrafoods@gmail.com": {
            "password": "Spectra@1134",
            "entity_name": "Spectra Foods & Beverages Private Limited",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
            "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "hemendratongia@gmail.com": {
            "password": "Swastik@12345",
            "entity_name": "Swastik Polytex",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ishwar.prajapati@in.tpacpackaging.com": {
            "password": "Ishv@1234",
            "entity_name": "TPAC Packaging India Pvt Ltd ",
            "plant": "Silvassa",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "arun.chaudhari@in.tpacpackaging.com": {
            "password": "Arun@123",
            "entity_name": "TPAC Packaging India Pvt Ltd ",
            "plant": "Umbergaon",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "kamal.mishra@in.tpacpackaging.com": {
            "password": "Tpac@123456#",
            "entity_name": "TPAC Packaging India Pvt Ltd ",
            "plant": "Haridwar",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "tpac.haridwar@in.tpacpackaging.com": {
            "password": "Tpac@4321# ",
            "entity_name": "TPAC Packaging India Pvt Ltd ",
            "plant": "Haridwar",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "kamlesh.mishra@in.tpacpackaging.com": {
            "password": "Sunpet@1mporter",
            "entity_name": "TPAC Packaging India Pvt Ltd ",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "senthilkumar.r@in.tpacpackaging.com": {
            "password": "Skypet@1a",
            "entity_name": "TPAC Skypet India Pvt Ltd ",
            "plant": "Coimbatore 1A",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "a.jeyaraj@in.tpacpackaging.com": {
            "password": "Tpac@1234 ",
            "entity_name": "TPAC Skypet India Pvt Ltd ",
            "plant": "Coimbatore 1B",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "senthurvignesh@in.tpacpackaging.com": {
            "password": "Skypet@1b",
            "entity_name": "TPAC Skypet India Pvt Ltd ",
            "plant": "Coimbatore 2",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "tamilarasan.k@in.tpacpackaging.com": {
            "password": "Tpac@1234 ",
            "entity_name": "TPAC Skypet India Pvt Ltd ",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "hitesh.shah@in.tpacpackaging.com": {
            "password": "Tpac@321 ",
            "entity_name": "TPAC Custom Solutions Pvt Ltd ",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "tushar.pimple@in.tpacpackaging.com": {
            "password": "Tpac@123",
            "entity_name": "TPAC Custom Solutions Pvt Ltd ",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Satish.jadhav@vvfltd.com": {
            "password": "Jan@2024",
            "entity_name": "VVF India",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Pi",
            "person_name": "Harshna",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sunil.katekari@vvfltd.com": {
            "password": "Vvfltd@2024",
            "entity_name": "VVF India",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Harshna",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "manoj.kumar5@wabtec.com": {
            "password": "Wabtec@2023",
            "entity_name": "Wabtec Locomotives Private Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Not provided",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "info@parampackaging.com": {
            "password": "Param@1313",
            "entity_name": "Param Packaging",
            "plant": "Mumbai",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Aniket",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "info@apexpacking.in": {
            "password": "Apex2@30062024",
            "entity_name": "Apex Packing Products Unit I",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "manoj.behera@jhaveriflexo.com": {
            "password": "Jfipl@123",
            "entity_name": "Jhaveri Flexo India",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ruchika@hectorbeverages.com": {
            "password": "Hector@2024",
            "entity_name": "Hector Bevrages",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
            "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sunilsonawane@hectorbeverages.com": {
            "password": "Hector@123",
            "entity_name": "Hector Bevrages",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
            "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Office@radhanplastics.in": {
            "password": "RpEpr@8469tb",
            "entity_name": "Radhan Pastic",
            "plant": "Maharashtra",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Kartiki",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "purchase2@rajivplastics.com": {
            "password": "R@jiv2024",
            "entity_name": "Rajiv Plastic Industries ",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Tushar",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ANAND@RAMMYINDIA.COM": {
            "password": "Rtspl@1234",
            "entity_name": "Rammy India",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Tushar",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "asolanki@sapat.com": {
            "password": "Parivar@1897",
            "entity_name": "Sapat International",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "apexstorm.infracon@gmail.com": {
            "password": "Storm@1234",
            "entity_name": "Storm Infracon",
            "plant": "Uttar Pradesh",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Ishika",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "storm.infracon@gmail.com": {
            "password": "Storm@1234",
            "entity_name": "Storm Infracon",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Ishika",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "vinod.kumar1@valvolinecummins.com": {
            "password": "Valvoline@123",
            "entity_name": "Valvoline",
            "plant": "Ambernath, Maharashtra",
            "entity_type": "Producer",
            "team_name": "Team Beta",
            "person_name": "Tushar",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Legal@valvolinecummins.com": {
            "password": "Valvoline@1234",
            "entity_name": "Valvoline",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Tushar",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ashoksharma@archidply.com": {
            "password": "Ashok@1234",
            "entity_name": "Archidply",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Tushar",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "kavita@toray-intl.in": {
            "password": "Toray@2024",
            "entity_name": "Toray International India",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "anmol.g@continental.coffee": {
            "password": "Continental@2022",
            "entity_name": "Continental Coffee (CCL)",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprcompliancepaints.brandowner@jsw.in": {
            "password": "Smokegrey@456",
            "entity_name": "JSW Paints",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprcompliancepaints.importer@jsw.in": {
            "password": "JSWpaintsimp@123",
            "entity_name": "JSW Paints",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "intimation@inbrew.com": {
            "password": "Inbrew@imp2024",
            "entity_name": "Inbrew Beverages",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "kishore.wable@inbrew.com": {
            "password": "Inbrew@2024",
            "entity_name": "Inbrew Beverages",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sanjaykumar@kuantumpapers.com": {
            "password": "Kuantum@2024",
            "entity_name": "Kuantum Papers",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "deepenerdev@kuantumpapers.com": {
            "password": "Kuantumpapers@2024",
            "entity_name": "Kuantum Papers",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "production@siddhomal.com": {
            "password": "Siddhomal@2420",
            "entity_name": "Siddhomal",
            "plant": "Uttar Pradesh",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "smpatel@tatachemicals.com": {
            "password": "Tata@123",
            "entity_name": "Tata Chemicals",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "avinash.singh@tatachemicals.com": {
            "password": "Tata@123",
            "entity_name": "Tata Chemicals",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "complianceindia@cmrsurgical.com": {
            "password": "CMRsreenivas@2023",
            "entity_name": "CMR Surgical India",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "avtcpdepr@avtcpd.co.in": {
            "password": "AVt@2022",
            "entity_name": "AVT",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr@marico.com": {
            "password": "Marico$2025",
            "entity_name": "Marico India",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sandip.gupta@marico.com": {
            "password": "Marico!2024",
            "entity_name": "Marico India",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "pradeep.ahuja@marico.com": {
            "password": "Marico!2024",
            "entity_name": "Marico India",
            "plant": "",
            "entity_type": "Producer - Perandurai",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "marico.sanand@marico.com": {
            "password": "Marico!2024",
            "entity_name": "Marico India",
            "plant": "",
            "entity_type": "Producer - Sanand",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "bharat.vanidani@purplle.com": {
            "password": "Faces@2022",
            "entity_name": "Purplle / Faces Cosmetics",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "shweta.jaidka@purplle.com": {
            "password": "Faces@2022",
            "entity_name": "Purplle / Faces Cosmetics",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "rahul.dash@purplle.com": {
            "password": "Purplle@2022",
            "entity_name": "Manash",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "regulatoryindia@hersheys.com": {
            "password": "Regulatory@789",
            "entity_name": "Hershey India",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "SParab1@hersheys.com": {
            "password": "Regulatory@789",
            "entity_name": "Hershey India",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "bimal@packprintind.com": {
            "password": "PackP@123",
            "entity_name": "Pack Print Industries (India)",
            "plant": "Dadara & Nagar",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "nitin@pramahikvision.com": {
            "password": "Arkca@2023",
            "entity_name": "Prama Hikvision",
            "plant": "",
            "entity_type": "BWMR",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "accounts@pramaindia.in": {
            "password": "Prama@123",
            "entity_name": "Prama India",
            "plant": "",
            "entity_type": "BWMR",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "rohit@creativeoffset.in": {
            "password": "Creativeimp@2024",
            "entity_name": "TCPL CREATIVES OFFSET PRINTERS PVT. LTD",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "naha@tcpl.in": {
            "password": "Accura#123",
            "entity_name": "TCPL Accura Inks",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "dewansu.agarwal@creativeoffset.in": {
            "password": "Creative@123",
            "entity_name": "TCPL Creative Offset",
            "plant": "Uttar Pradesh",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "pankaj@tcpl.in": {
            "password": "Thpl#1234",
            "entity_name": "TCPL- Halma",
            "plant": "Goa",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "santosh.gawali@tcplhalma.com": {
            "password": "Halma@i1234",
            "entity_name": "TCPL- Halma",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "mohit.kapoor@tcpl.in": {
            "password": "Inno@regn2023",
            "entity_name": "TCPL Innofilms",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "harshil.raut@tcpl.in": {
            "password": "Inno@regn2023",
            "entity_name": "TCPL Innofilms",
            "plant": "Dadara & Nagar",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "mukti@tcpl.in": {
            "password": "TCPLimp@2024",
            "entity_name": "TCPL Packaging",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "satya@tcpl.in": {
            "password": "TcpLpR@2022",
            "entity_name": "TCPL Packaging",
            "plant": "Assam,Goa,Uttarakhand,Dadara",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ws.legal@trent-tata.com": {
            "password": "Trent@123",
            "entity_name": "Trent",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.trent@trent-tata.com": {
            "password": "Trent@123",
            "entity_name": "Trent",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprp.j1@uflexltd.com": {
            "password": "Uflex@108",
            "entity_name": "Uflex J1",
            "plant": "Jammu Kashmir 1",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprp.j2@uflexltd.com": {
            "password": "Uflex@108",
            "entity_name": "Uflex J2",
            "plant": "Jammu Kashmir 2",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprp.j3@uflexltd.com": {
            "password": "Uflex@108",
            "entity_name": "Uflex J3",
            "plant": "Jammu Kashmir 3",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprp.dharwad@uflexltd.com": {
            "password": "Uflex@108",
            "entity_name": "Uflex Dharwad",
            "plant": "Dharwad",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprp.a1@uflexltd.com": {
            "password": "Uflex@108",
            "entity_name": "Uflex A1",
            "plant": "Noida A1",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprp.a2am@uflexltd.com": {
            "password": "Uflex@108",
            "entity_name": "Uflex A2",
            "plant": "Noida A2",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprp.c4m@uflexltd.com": {
            "password": "Uflex@1089",
            "entity_name": "Uflex C4",
            "plant": "Noida C4",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprp.d1@uflexltd.com": {
            "password": "Uflex@108",
            "entity_name": "Uflex D1",
            "plant": "Noida d1",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprp.sanand@uflexltd.com": {
            "password": "Uflex@108",
            "entity_name": "Uflex Sanand",
            "plant": "Sanand",
            "entity_type": "Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.brandowner@uflexltd.com": {
            "password": "Uflex@108",
            "entity_name": "Uflex Brand Owner",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.importer@uflexltd.com": {
            "password": "Uflex@1089",
            "entity_name": "Uflex Importer",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "dkj@uflexltd.com": {
            "password": "Abcd1234@",
            "entity_name": "Uflex PWP Noida",
            "plant": "Noida",
            "entity_type": "PWP",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "recycler.l1@uflexltd.com": {
            "password": "Abcd1234#",
            "entity_name": "Uflex PWP Malanpur",
            "plant": "Malanpur",
            "entity_type": "PWP",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sheonarayan.prasad@uflexltd.com": {
            "password": "Sheo@25283",
            "entity_name": "Uflex PWP Jammu",
            "plant": "Jammu",
            "entity_type": "PWP",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "tejas@fabbag.com": {
            "password": "Latke@1234",
            "entity_name": "Sugar Cosmetics (Vellvette)",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "biplab.chatterjee@abbott.com": {
            "password": "Abbott@123",
            "entity_name": "Abbott Healthcare (Abbott)",
            "plant": "",
            "entity_type": "",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "demosha@gmail.com": {
            "password": "Demosha@123",
            "entity_name": "Demosha Chemicals",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "arup@globusgroup.in": {
            "password": "Globus@2024",
            "entity_name": "Globus Spirit",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "hrd@goodrichworld.org": {
            "password": "Goodrich@23",
            "entity_name": "Goodrich Carbohydrates",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "navnath.subhashpatole@abbott.com": {
            "password": "Sjmipl@2006",
            "entity_name": "St. Judes Medical (Abbott)",
            "plant": "",
            "entity_type": "E Waste Producer",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sppljsr@gmail.com": {
            "password": "Shaurya@123",
            "entity_name": "Shaurya Plasto",
            "plant": "Jharkhand",
            "entity_type": "PWP",
            "team_name": "Team Theta",
            "person_name": "Rudrashish",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "huzefa@biostadt.com": {
            "password": "Biostadt@1234",
            "entity_name": "Biostadt India Limited",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Theta",
            "person_name": "Prachi Doyale",
                "recipient_email": ["toufeeq.mulani@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "cileprbrandowner@castrol.com": {
            "password": "Castrolbo@1234",
            "entity_name": "Castrol",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Shalaka",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "cileprimporter@castrol.com": {
            "password": "Castrolimporter@123",
            "entity_name": "Castrol",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Shalaka",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ind_custserv@promega.com": {
            "password": "Promega@123",
            "entity_name": "Promega",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Shalaka",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "vidhya.bprabhu@promega.com": {
            "password": "Promegabo@123",
            "entity_name": "Promega",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Shalaka",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "customersupport@croma.com": {
            "password": "Croma@2024",
            "entity_name": "Infinity Croma",
            "plant": "",
            "entity_type": "PWMR (BO)",
            "team_name": "Team Beta",
            "person_name": "Shalaka",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sthiradhi.das@gmail.com": {
            "password": "Croma@2024",
            "entity_name": "Infinity Croma",
            "plant": "",
            "entity_type": "PWMR (IMP)",
            "team_name": "Team Beta",
            "person_name": "Shalaka",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Sustainabilitych.im@pg.com": {
            "password": "Pghl@2024",
            "entity_name": "PGHL",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "IMPORTER.IM@PG.COM": {
            "password": "Pghl@12324",
            "entity_name": "PGHL",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "harshita.sharma@perfettivanmelle.com": {
            "password": "Saupra@2001",
            "entity_name": "Perfetti van melle india pvt ltd",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Tushar",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "foodimports@in.pvmgrp.com": {
            "password": "Pwm@regn22",
            "entity_name": "Perfetti van melle india pvt ltd",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Tushar",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "regulatorycompliance@cavinkare.com": {
            "password": "Cavins@4321",
            "entity_name": "Cavin kare Pvt Ltd",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Tushar",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "nishanth.s@cavinkare.com": {
            "password": "",
            "entity_name": "Cavin kare Pvt Ltd",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Tushar",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sanjeeb_sahu@colpal.com": {
            "password": "Colgate@2024",
            "entity_name": "Colgate Palmolive (India) Limited",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "raghu_nath@colpal.com": {
            "password": "Colgate@2024",
            "entity_name": "Colgate Palmolive (India) Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "siddhesh.desai@glenmarkpharma.com": {
            "password": "Glenmark@PWM100",
            "entity_name": "Glenmark Pharmaceuticals Limited",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ravindra.dhatrak@glenmarkpharma.com": {
            "password": "Ravindra@2024",
            "entity_name": "Glenmark Pharmaceuticals Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprgil.im@pg.com": {
            "password": "GILBrandOwner@2024",
            "entity_name": "Gillette India Ltd.",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "patel.n.24@pg.com": {
            "password": "GIL@Importer@2024",
            "entity_name": "Gillette India Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "srivastava.r@pg.com": {
            "password": "PGHPBrandOwner@2024",
            "entity_name": "Procter & Gamble Hygiene And Health Care Limited",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprpghhcl.im@pg.com": {
            "password": "PGHHBrandOwner@879",
            "entity_name": "Procter & Gamble Home Products Pvt. Ltd.",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sharma.sv@pg.com": {
            "password": "Pghhi@2022",
            "entity_name": "Procter & Gamble Home Products Pvt. Ltd.",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "eprpghp.im@pg.com": {
            "password": "PGHPImporter@879",
            "entity_name": "Procter & Gamble Hygiene And Health Care Ltd.",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Siddharth.Salunke@shell.com": {
            "password": "Simpl@t5",
            "entity_name": "Shell India Markets Private Limited",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Kaustubh.Sinha@shell.com": {
            "password": "Shell@123",
            "entity_name": "Shell India Markets Private Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "gandharoil92@gmail.com": {
            "password": "Goril_2024",
            "entity_name": "Gandhar Oil",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "20244B00109": {
            "password": "Gandharoil@2024",
            "entity_name": "Gandhar Oil",
            "plant": "",
            "entity_type": "Producer(UO)",
            "team_name": "Team Beta",
            "person_name": "Pooja",
                "recipient_email": ["bharat.gaggar@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "dscpl.grn@dsgroup.com": {
            "password": "Dsfl@2024",
            "entity_name": "DS Foods Limited",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "dsl.nda@dsgroup.com": {
            "password": "Dsl@2024",
            "entity_name": "DS Limited",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ds.spicecogrn@dsgroup.com": {
            "password": "April@2024",
            "entity_name": "DS Spice co",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "harish.kashyap@dsgroup.com": {
            "password": "DSRetail@2024",
            "entity_name": "DS Retail",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "pwmp1@dow.com": {
            "password": "DowChem@2425",
            "entity_name": "Dow Chemicals ",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "pwmbo@dow.com": {
            "password": "DowChem@2024",
            "entity_name": "Dow Chemicals ",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "apac-hso-cs.india@hoya.com": {
            "password": "Hoya@Oct2024",
            "entity_name": "Hoya Medical ",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Rishik",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "info.India@hoya.com": {
            "password": "Hoya@Oct2024",
            "entity_name": "Hoya Medical ",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Rishik",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "intimateflexipack@gmail.com": {
            "password": "Ravi@123",
            "entity_name": "Initimate Flexipack",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Ishika",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "EHS.India@kellogg.com": {
            "password": "Kellanova@2024",
            "entity_name": "Kellogg India",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "suresh.babu@kellogg.com": {
            "password": "Kellanova@2024",
            "entity_name": "Kellogg India",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "vijay.bhartia@lvpvl.com": {
            "password": "Sap@@1234",
            "entity_name": "Laxmi Vinayak (LVPL) (HUL 2P)",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Rishik",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "shailendragusain@clarionindia.in": {
            "password": "Lotus@123",
            "entity_name": "Lotus Beauty Care Products (HUL 2P)",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "fm@herbalmail.in": {
            "password": "Herbal@2024",
            "entity_name": "Herbal Cosmetics (HUL 2P)",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "gaurav.gupta@rhpgroup.in": {
            "password": "PWM@regn2023",
            "entity_name": "RHP Health Care (HUL 2P)",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "amit.badola@rhpgroup.in": {
            "password": "Rishiveda@2015",
            "entity_name": "Rishiveda Herbal Products (HUL 2P)",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra",
                "recipient_email": ["prathmesh.chitroda@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "anil@siliconinfotech.co": {
            "password": "Silicon@2023",
            "entity_name": "Silicon Infotech",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Ishika",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "gokul.aware@sterlite.com": {
            "password": "Stltech@2023",
            "entity_name": "Sterlite Technologies",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Ishika",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ranchi.accounts@waxpol.com": {
            "password": "Waxpol@2024",
            "entity_name": "Waxpol Industries",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Rishik",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "kk.dubey@coolcosmetics.in": {
            "password": "Cool@2023",
            "entity_name": "Cool Cosmetics",
            "plant": "Haridwar, Uttrakhand",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "gourav@kpmanish.com": {
            "password": "KPMGIepr@108",
            "entity_name": "K.P.Manish Global Ingredients",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Ishika",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "hr@stella-indusstries.com": {
            "password": "Stella@123",
            "entity_name": "Stella Indusstries",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "ramnath.vaidyanathan@godrejinds.com": {
            "password": "Godrej@2023",
            "entity_name": "GCPL",
            "plant": "",
            "entity_type": "BWMR",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "jinal.manek@godrejcp.com": {
            "password": "Gcpl@2023",
            "entity_name": "GCPL",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "jakkuva.rao@mdlz.com": {
            "password": "Cadbury2@",
            "entity_name": "MDLZ",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Sangram.Joshi@mdlz.com": {
            "password": "Mdlz@2022",
            "entity_name": "MDLZ",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "qa@tatastarbucks.com": {
            "password": "Welcome@#123",
            "entity_name": "Tata Starbucks",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "vinay.prajapati@tatastarbucks.com": {
            "password": "Welcome@#123",
            "entity_name": "Tata Starbucks",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Iota",
            "person_name": "Abhishek",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sukhendrakumar@mdpet.in": {
            "password": "Tppl$2024@@@",
            "entity_name": "Technoplast Packaging (Sagar Unit)",
            "plant": "Sagar, Madhya pradesh",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "rakesh.verma@bharatgroup.co.in": {
            "password": "Rakesh@2109",
            "entity_name": "BR Agrotech",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "accounts.tppl@mdpet.in": {
            "password": "Tppl@2024%%%",
            "entity_name": "Technoplast (Pithampur Unit)",
            "plant": "Pritampur, Madhya Pradsh",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "info@mdpet.in": {
            "password": "Tppl@2024$$$",
            "entity_name": "Technoplast (Kathua Unit)",
            "plant": "Kathua, Jammu & Kashmir",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "mdenterprises.office@gmail.com": {
            "password": "Tppl@54321",
            "entity_name": "MD Enterprises",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "chandan.jha@mdpet.in": {
            "password": "Mdpack@123",
            "entity_name": "MD Packaging",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sahil@mdpet.in": {
            "password": "Flex@2024$$",
            "entity_name": "Technoflex",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "accounts.tppl1@mdpet.in": {
            "password": "Corpbiz@123",
            "entity_name": "Technoplast Pacakging (Kathua Unit 2)",
            "plant": "Kathua, Jammu & Kashmir",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "shivalik.pack@gmail.com": {
            "password": "Satish@1234",
            "entity_name": "Shivalik Packaging",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Iota",
            "person_name": "Prachi Ghatge",
                "recipient_email": ["ishika.sisodia@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "k.ganesh@bisleri.co.in": {
            "password": "Sandeep@123",
            "entity_name": "Bisleri",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Alpha",
            "person_name": "Dhaval/Aayushi",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "devendra.garg@dlecta.com": {
            "password": "Dlecta@2024",
            "entity_name": "Dlecta",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Alpha",
            "person_name": "Kartiki",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "swati.salvi@dlecta.com": {
            "password": "Dlectalm@2024",
            "entity_name": "Dlecta",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Alpha",
            "person_name": "Kartiki",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "antara.kapoor@pepsico.com": {
            "password": "PepsiCo@2024",
            "entity_name": "PepsiCo",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "harpreet.bhatia@pepsico.com": {
            "password": "Pepsico@importer12",
            "entity_name": "PepsiCo",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.mandhala1@ssfplastics.com": {
            "password": "Net@2432",
            "entity_name": "SSF PLASTICS INDIA PVT LTD - MANDHALA",
            "plant": "Mandhala",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.baddi1@ssfplastics.com": {
            "password": "Net@2432",
            "entity_name": "SSF PLASTICS INDIA PVT LTD - BADDI UNIT1",
            "plant": "Baddi Unit1",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.technoplast4@ssfplastics.com": {
            "password": "Net@2432",
            "entity_name": "SSF TECHNOPLAST",
            "plant": "Himachal Pradesh",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.convertor@ssfplastics.com": {
            "password": "Net@2432@",
            "entity_name": "SSF CONVERTOR",
            "plant": "Himachal Pradesh",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.hp@ssfplastics.com": {
            "password": "Net@2432@",
            "entity_name": "SSF PLASTICS HP",
            "plant": "Baddi, Himachal Pradesh",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.hosur2@ssfplastics.com": {
            "password": "Net@2432@",
            "entity_name": "SSF PLASTICS INDIA PVT LTD - HOSUR",
            "plant": "Hosur",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.moulders5@ssfplastics.com": {
            "password": "Net@2432#",
            "entity_name": "SSF PLASTICS MOULDER ",
            "plant": "Dadara & Nagar",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.ssfpackaging.1@ssfplastics.com": {
            "password": "Neeraj@2023",
            "entity_name": "SSF Packaging - Unit1 ",
            "plant": "Baddi Unit 2",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.packaging2@ssfplastics.com": {
            "password": "Net@2432#",
            "entity_name": "SSF Packaging - Unit2",
            "plant": "Baddi Unit 3",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.u1.daman@ssfplastics.com": {
            "password": "Net@2432",
            "entity_name": "SSF PLASTICS INDIA PVT LTD - Daman 1",
            "plant": "Daman 1",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.u2.daman@ssfplastics.com": {
            "password": "Net@2432",
            "entity_name": "SSF PLASTICS INDIA PVT LTD - Daman 2",
            "plant": "Daman 2",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.u3.daman@ssfplastics.com": {
            "password": "Net@2432",
            "entity_name": "SSF PLASTICS INDIA PVT LTD - Daman 3",
            "plant": "Daman 3",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.daman@ssfplastics.com": {
            "password": "Net@2432",
            "entity_name": "SSF PLASTICS INDIA PVT LTD - Daman 4",
            "plant": "Daman4",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "epr.hyderabad@ssfplastics.com": {
            "password": "Net@2432#",
            "entity_name": "SSF PLASTICS INDIA PVT LTD - Hyderabad",
            "plant": "Hyderabad5",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "harshal.marathe@unilever.com": {
            "password": "HULBrandOwner@786",
            "entity_name": "HUL ",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Alpha",
            "person_name": "Aayushi",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "hul.plasticcompliance@unilever.com": {
            "password": "HUL@Importer@786",
            "entity_name": "HUL ",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Alpha",
            "person_name": "Aayushi",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "accounts@SMA-India.com": {
            "password": "Solar@123",
            "entity_name": "SMA Solar India Private Limited ",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Alpha",
            "person_name": "Kartiki",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "srikanth.ankala@sterlite.com": {
            "password": "Stl@2024",
            "entity_name": "Sterlite Technologies",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Alpha",
            "person_name": "Dhaval",
            "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "jayvant.jadhav@sterlite.com": {
            "password": "Stcsl@2023",
            "entity_name": "Sterlite Tech Cables",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Alpha",
            "person_name": "Aayushi",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "Daniele.perottino@ferrero.com": {
            "password": "Ferrero@2023",
            "entity_name": "Ferrero India Private Limited",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Alpha",
            "person_name": "Aayushi",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "sagar.yele@ferrero.com": {
            "password": "Ferrero@2022",
            "entity_name": "Ferrero India Private Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Alpha",
            "person_name": "Aayushi",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "VINOD.KUSHWAHA@WALLACEPHARMA.NET": {
            "password": "Vinod@1234",
            "entity_name": "Wallace Pharmaceuticals Private Limited",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Alpha",
            "person_name": "Aayushi",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "girishfire.safety@gmail.com": {
            "password": "Safety@1",
            "entity_name": "Matter Mobility Pvt Ltd",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Aayushi",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "accounts@matter.in": {
            "password": "MatterAera@786",
            "entity_name": "Matter Energy",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Alpha",
            "person_name": "Aayushi",
                "recipient_email": ["aayushi.agarwal@aagarg.co.in","Tech.support@aagarg.co.in"]
        },
        "alok.rusia@alpla.com": {
            "password": "Baddi1@2024",
            "entity_name": "Alpla",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "arvind.banyal@alpla.com": {
            "password": "Baddi2@2024",
            "entity_name": "Alpla",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "Nardev.thakur@alpla.com": {
            "password": "Baddi3@2024",
            "entity_name": "Alpla",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "aranyak.hazra@alpla.com": {
            "password": "Pasha@2024",
            "entity_name": "Alpla",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "kaustubha.nand@alpla.com": {
            "password": "Sita@2024",
            "entity_name": "Alpla",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "Sanjeev.kumar@alpla.com": {
            "password": "Silvasa@2024",
            "entity_name": "Alpla",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "agmaccounts@aquaproofindia.com": {
            "password": "Chemical@8591",
            "entity_name": "Aquaproof Construction Chemical India Pvt Ltd - Kalol",
            "plant": "",
            "entity_type": "SIMP",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "kirti@aquaproofindia.com": {
            "password": "Importer@1219",
            "entity_name": "Aquaproof Construction Chemical India Pvt Ltd - Kalol",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "accountsexecutive@aquaproofindia.com": {
            "password": "Aqua_cbe@2025",
            "entity_name": "Aquaproof wall care i private limited coimbatore",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "mumbaiaccounts@aquaproofindia.com": {
            "password": "Aqua_hyderabad",
            "entity_name": "Aquaproof wall care i private limited Hyderabad",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "account@aquaproofindia.com": {
            "password": "Kalol@wallcare98",
            "entity_name": "Aquaproof wall care i private limited Kalol",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "rawcaccounts@aquaproofindia.com": {
            "password": "Domesh@4321",
            "entity_name": "Aquaproof wall care i private limited Raipur",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "accountsmumbai@aquaproofindia.com": {
            "password": "Accounts@85",
            "entity_name": "Aquaproof wallcare India Pvt Ltd. Alwar A-320",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "vatsal@aquaproofindia.com": {
            "password": "Vatsal@26",
            "entity_name": "Aquaproof wallcare India Pvt Ltd. Alwar E-12",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "viraj.bavisakar@aquaproofindia.com": {
            "password": "Viraj@aqua25",
            "entity_name": "Aquaproof wallcare India Pvt Ltd. PLOT NO G 1052",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "md@aquaproofindia.com": {
            "password": "MD@aqua25",
            "entity_name": "Aquaproof wallcare India Pvt Ltd. PLOT NO G 1052",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "Ravindra.SinghChauhan@avgol.com": {
            "password": "India@2024",
            "entity_name": "Avgol India Private Limited",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Aniket"
        },
        "Soumitra.Shrivastava@avgol.com": {
            "password": "Bhopal@123",
            "entity_name": "Avgol India Private Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Aniket"
        },
        "accountsmanager@aquaproofindia.com": {
            "password": "Manager@aqua26",
            "entity_name": "Avon Building Product Pvt Ltd- Kalol",
            "plant": "",
            "entity_type": "SIMP",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "rammaccounts@aquaproofindia.com": {
            "password": "Rama@Accounts85",
            "entity_name": "Avon Building Product Pvt Ltd- Raipur",
            "plant": "",
            "entity_type": "SIMP",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "hoaccounts@aquaproofindia.com": {
            "password": "Avon@Jhar12",
            "entity_name": "Avon Building Product Pvt Ltd- Ranchi",
            "plant": "",
            "entity_type": "SIMP",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "finance@beardo.in": {
            "password": "Beardo@7777",
            "entity_name": "Beardo",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "Ronak.Baphna@beardo.in": {
            "password": "Zlpl@2024",
            "entity_name": "Beardo(ZLPL)",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "finance@eastea.in": {
            "password": "Ecpl@2023",
            "entity_name": "Eastea",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "operation@ebullientpack.com": {
            "password": "99300_Ebu*1",
            "entity_name": "EBULLIENT PACKAGING PRIVATE LIMITED",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "commercial@ebullientpack.com": {
            "password": "99300_Ebu*2",
            "entity_name": "EBULLIENT PACKAGING PRIVATE LIMITED",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "support@ebullientpack.com": {
            "password": "99300_Ebu*3",
            "entity_name": "EBULLIENT PACKAGING PRIVATE LIMITED",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "hr.ecoplastprithla@gmail.com": {
            "password": "99997_Eco*1",
            "entity_name": "Eco Plast",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "raman.goel@edelmann-group.com ": {
            "password": "Edemann@2023",
            "entity_name": "Edelmann",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "tejas@fabbag.com": {
            "password": "",
            "entity_name": "Fab",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "  shweta.jaidka@faces-india.com": {
            "password": "Faces@2022",
            "entity_name": "Faces Cosmetics India Private limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "g.rajamani196@gmail.com": {
            "password": "Eprfci@23",
            "entity_name": "FCI OEN CONNECTOR ",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "dinesh@gmpolyplast.com": {
            "password": "Gmp@123#",
            "entity_name": "GMPolyplast",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "anandakumarv@hersheys.com": {
            "password": "HersheyIMP@2022",
            "entity_name": "Hershey India Private Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "vd@aquaproofindia.com": {
            "password": "Vimal@aqua26",
            "entity_name": "hindustan tiles & wallcare LLP - Raipur",
            "plant": "",
            "entity_type": "SIMP",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "sonia@aquaproofindia.com": {
            "password": "Importer@LLP12",
            "entity_name": "hindustan tiles & wallcare LLP - Raipur",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "dv.iyer@huhtamaki.com": {
            "password": "Huhtamaki#2024",
            "entity_name": "Huhtamaki",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "cdadmin@chemexindia.com": {
            "password": "Chemex@2023",
            "entity_name": "HUL 2P - Chemex Detergents",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "prashant.gulhane@rmgroup501.com": {
            "password": "Rmc@2023",
            "entity_name": "HUL 2P - R M Chemical",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "aquaaccounts@aquaproofindia.com": {
            "password": "Sonali@aqua25",
            "entity_name": "Inland Building Product Private Limited Alwar",
            "plant": "",
            "entity_type": "SIMP",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "accounts@aquaproofindia.com": {
            "password": "Yamini@aqua25",
            "entity_name": "Inland Building Product Private Limited Satra",
            "plant": "",
            "entity_type": "SIMP",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "shivendru.mathur@itc.in": {
            "password": "ITClimited@123",
            "entity_name": "ITC",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "Pranav.K@itcfibre.in": {
            "password": "Itc@2024",
            "entity_name": "ITC FIBRE",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "epr.producer@itc.in": {
            "password": "Itcproducer@2024",
            "entity_name": "ITC Limited (Producer)",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "Gupta.Ankit@itc.in": {
            "password": "ITClimited@2001",
            "entity_name": "ITC limited Importer",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "nagarajshetty@jnsneopac.in": {
            "password": "Jns@2022",
            "entity_name": "JNS Neopack",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "eprimp@jdl.in": {
            "password": "Jdplblr@1234",
            "entity_name": "JOHN DISTILLERIES PRIVATE LIMITED",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "param@kventures.co.in": {
            "password": "Kabir@2023",
            "entity_name": "KABIR VENTURES",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Aniket"
        },
        "shailendra.gusain@gmail.com": {
            "password": "Lotus@123",
            "entity_name": "Lotus Beauty Care Products Private Limited",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "maharajapolyfabpvtltd@gmail.com": {
            "password": "",
            "entity_name": "Maharaja Polyfab",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "dey.biswajit@mahindra.com": {
            "password": "Masl@123",
            "entity_name": "MAHINDRA AUTO STEEL PRIVATE LIMITED",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "mrktmgr16@gmail.com": {
            "password": "Mandagini@2022",
            "entity_name": "Mandagini Seals",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "viren.w@mepro.in": {
            "password": "Mepro@24",
            "entity_name": "Mepro Pharmaceuticals",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "alpesh.patel@nfil.in": {
            "password": "Nfasl@2023",
            "entity_name": "NAVIN FLUORINE ADVANCED SCIENCES LIMITED",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "manoj.patil@nfil.in": {
            "password": "Nfil@2023",
            "entity_name": "NAVIN FLUORINE INTERNATIONAL LIMITED",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "newagepkg@gmail.com": {
            "password": "VasaiNAP@2024",
            "entity_name": "New age packaging",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "archana@nap-india.com": {
            "password": "8689@NewAge@2024",
            "entity_name": "New age packaging",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "hr.howrah@nationalgroup.in": {
            "password": "Howrah@2024",
            "entity_name": "NPIPL",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "ngpl@nufab.co.in": {
            "password": "Pawan#2023",
            "entity_name": "Nufab",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "expo@omblowplastt.com": {
            "password": "Omblow@24",
            "entity_name": "OM BLOW PLAST",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "Pradumansinh.Atodaria@amcor.com": {
            "password": "Phoenix@1234",
            "entity_name": "Phoneix Flexible",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "rajeshsharma@pinetreepackaging.com": {
            "password": "Pinetree@1313",
            "entity_name": "Pinetree Packaging",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "corporate.in@puig.com": {
            "password": "Puig@2023",
            "entity_name": "Puig India",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "eprbdd@richprinters.com   ": {
            "password": "Eprbdd@24@",
            "entity_name": "Rich Printers - Baddi 1",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "eprbhd@richprinters.com": {
            "password": "Eprbhd@24@",
            "entity_name": "Rich Printers - Bhiladh",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "eprslg@richprinters.com": {
            "password": "Eprslg@24@",
            "entity_name": "Rich Printers - Siliguri",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "svpvinyl@hotmail.com": {
            "password": "Sharma@2000",
            "entity_name": "S V Plasto Films",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "info@sarvodayaind.com": {
            "password": "Paresh@123 ",
            "entity_name": "Sarvodaya",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "legal.india@scholleipn.com": {
            "password": "Scholle#7",
            "entity_name": "Scholle IPN India Packaging Private Limited",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "Polytex007@gmail.com": {
            "password": "Poly@2024",
            "entity_name": "Shrigovind Polytex",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "reshma@shrotra.in ": {
            "password": "Arha@2020",
            "entity_name": "Shrota",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "accounts@siddharthagroup.net": {
            "password": "Siipl@0707",
            "entity_name": "Siddhartha Innopack Industries Pvt Ltd. Unit I",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "kpvemuri@siddharthainnopack.com": {
            "password": "Unit3@@0707",
            "entity_name": "Siddhartha Innopack Industries Pvt Ltd. Unit II",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "finance@spraytecindia.com": {
            "password": "SPRAYTEC@2023",
            "entity_name": "Spraytec",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Aniket"
        },
        "corp.admin@sri-pack.com": {
            "password": "Abcd@123",
            "entity_name": "SRI HARI PACKAGING INDUSTRIES PVT. LTD.",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "dharamlal.sunchitenterprises@gmail.com": {
            "password": "Sunchit@16758",
            "entity_name": "SUNCHIT ENTERPRISES",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "ehs.communications@tdsgj.co.in": {
            "password": "EHS@tdsg22",
            "entity_name": "TDSG",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "karajgam.accounts@techfabindia.com": {
            "password": "Techfab@2023",
            "entity_name": "Tech Fab",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Pi",
            "person_name": "Darshan"
        },
        "aamir@paperprintproduct.com": {
            "password": "Paperprint@2022",
            "entity_name": "TPPP",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Harshna"
        },
        "hrmanager@vijaykantdairy.com": {
            "password": "Vijaykant@123",
            "entity_name": "Vijaykant Dairy & Foods",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Pi",
            "person_name": "Aniket"
        },
        "deepak.shrivastav@mithilapacktech.com": {
            "password": "Deepak@1234",
            "entity_name": "Vinayak",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "wellmacdaman@gmail.com": {
            "password": "Well@1624",
            "entity_name": "Wellmac",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "admin@wellmacplastics.com": {
            "password": "Wppl@0524",
            "entity_name": "Wellmac Importer",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Jayendra"
        },
        "admin.corp@whiteteak.com": {
            "password": "Whiteteak@2020",
            "entity_name": "White Teak (BO)",
            "plant": "",
            "entity_type": "Brand Owner",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "balu@whiteteak.com": {
            "password": "Whiteteak*2020",
            "entity_name": "White Teak (Importer)",
            "plant": "",
            "entity_type": "Importer",
            "team_name": "Team Pi",
            "person_name": "Prathamesh"
        },
        "quality.guwahati@skanem.com": {
            "password": "Guwahati@2025",
            "entity_name": "Skanem India Pvt Ltd",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar"
        },
        "purchae.baddi@skanem.com": {
            "password": "Baddi@2025",
            "entity_name": "Skanem India Pvt Ltd",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar"
        },
        "vinit.yadav@skanem.com": {
            "password": "Epr@12345",
            "entity_name": "Skanem India Pvt Ltd",
            "plant": "",
            "entity_type": "Producer",
            "team_name": "Team Pi",
            "person_name": "Shubham Kumbhar"
        }
    }


    def generate_otp():
        today = date.today()  # ✅ This defines 'today'
        timestamp = datetime.now().strftime('%H%M%S')
        otp_value = (today.day + today.month) * 25
        timestamp_sum = sum(int(digit) for digit in timestamp)  # Sum of timestamp digits
        otp = f"{otp_value}{timestamp_sum}"  # Combine base OTP with summed timestamp
        return otp


    def send_email(title, email, otp, entity_name, entity_type, team_name, person_name,recipient_email):
        sender_email = "eprsyncaagarg@gmail.com"
        # receiver_emails = [
        #     "kamlesh.zore@aagarg.co.in",
        #     #"hussain.parpia@aagarg.co.in",
        #     #"sajan.savaliya@aagarg.co.in"
        # ]  # List of recipients
        password = "phrmtxwvkmmsqpbv"
        smtp_server = "smtp.gmail.com"
        smtp_port = 465

        device_name = platform.node()
        
        message = EmailMessage()
        message["From"] = sender_email
        message["To"] = recipient_email 
        # message["To"] = ", ".join(receiver_emails)  # Join multiple emails
        message["Subject"] = f"Login Attempt Notification – {entity_name}"
        
        # HTML Email Body
        body = f'''
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ width: 80%%; margin: auto; border: 1px solid #ddd; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; font-size: 18px; }}
                .content {{ padding: 20px; font-size: 16px; }}
                .otp {{ font-size: 20px; font-weight: bold; color: #d9534f; }}
                .footer {{ margin-top: 20px; font-size: 14px; color: #555; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">Login Attempt Notification</div>
                <div class="content">
                    <p>Dear Team,</p>
                    <p>A login attempt has been made on the CPCB EPR Portal with the following details:</p>
                    <ul>
                        <li><strong>Email:</strong> {email}</li>
                        <li><strong>Entity Name:</strong> {entity_name}</li>
                        <li><strong>Entity Type:</strong> {entity_type}</li>
                        <li><strong>Team Name:</strong> {team_name}</li>
                        <li><strong>Client Allocated to:</strong> {person_name}</li>
                        <li><strong>Windows Login User:</strong> {windows_username}</li>
                        <li><strong>One-Time Password (OTP):</strong> <span class="otp">{otp}</span></li>
                        <li><strong>Login Person Device Name:</strong> {device_name}</li>
                    </ul>
                    <p>If you recognize this attempt, please proceed with the OTP for authentication. If this attempt was not initiated by you or Team, kindly report it to the IT support team immediately.</p>
                    <p>For any concerns or assistance, feel free to contact us Tech.Support@aagarg.co.in </p>
                </div>
                <div class="footer">
                    <p>Best regards,<br>Tech Support<br>A A Garg & Co</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        message.set_content("This is a login attempt notification. Please view this email in an HTML-supported email client.")
        message.add_alternative(body, subtype='html')
        
        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent successfully to {recipient_email}")
            return True
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")
            return False
            
    # Get username from user
    username = easygui.enterbox("Enter your username:", "Login")

    if username in credentials:
        otp = generate_otp()
        entity_name = credentials[username]["entity_name"]
        entity_type = credentials[username]["entity_type"]
        team_name = credentials[username]["team_name"]  
        person_name = credentials[username]["person_name"] 
        recipient_email = credentials[username]["recipient_email"]
        
        # Now pass all required arguments
        if send_email("Login Confirmation", username, otp, entity_name, entity_type, team_name, person_name,recipient_email):
            easygui.msgbox("A confirmation email with OTP has been sent. Please check your email to proceed.", "Email Sent")
            entered_otp = easygui.enterbox("Enter the OTP sent to your email:", "OTP Verification")
            
            if entered_otp == otp:
                password = credentials[username]["password"]
                action = ActionChains(driver)
                action.click(on_element=driver.find_element(By.XPATH, '//*[@id="user_name"]')).perform()
                action.click(on_element=driver.find_element(By.XPATH, '//*[@id="password_pass"]')).perform()
                driver.find_element(By.XPATH, '//*[@id="user_name"]').send_keys(username)
                driver.find_element(By.XPATH, '//*[@id="password_pass"]').send_keys(password)
            else:
                easygui.msgbox("Invalid OTP. Please try again.", "Error")
        else:
            easygui.msgbox("Failed to send confirmation email. Try again later.", "Error")
    else:
        easygui.msgbox("Username not found!", "Error")

    print(driver.get_cookies())
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
##    login_token = driver.get_cookies()[0]["value"]
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)
##    print(login_token)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'login-token={login_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    
    errors = []
    
    def entity_type(entity, state, category, material_type):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/get_pibo_dropdown_data"
        
        payload = json.dumps({
            "type": [
                "entity_type_for_sales",
                "states_list",
                "plastic_category",
                "plastic_material_type"
            ],
            "company_id": 15247,
            "section": "procurement"
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", {})
            entity_value = next((i["value"] for i in datas.get("entity_type_for_sales", []) if entity.lower() == i["label"].lower()), None)
            state_value = next((i["value"] for i in datas.get("states_list", []) if state.lower() == i["label"].lower()), None)
            category_value = next((i["value"] for i in datas.get("plastic_category", []) if category.lower() == i["label"].lower()), None)
            material_type_value = next((i["value"] for i in datas.get("plastic_material_type", []) if material_type.lower() == i["label"].lower()), None)

            return entity_value, state_value, category_value, material_type_value
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    def pdf_path(pdf_path, pdf_filename):

        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pwp/upload_image"
        headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Cookie': f'login-token={login_token}',
                    }
        payload = {'section': 'upload_filepath'}
        files=[
        ('file',(f"{pdf_filename}.pdf",open(f'{pdf_path}','rb'),'application/pdf'))
        ]
        response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)
        path = response.json()["data"]["path"]
        return path

    def entity_register_id(entity_value, name):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_entity_name"

        payload = json.dumps({
        "entity_type": entity_value
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", [])
            registered_id = next((i["value"] for i in datas if name.lower().strip() == i["label"].lower().strip()), None)
            return registered_id
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    root.destroy()

    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename': str, 'Bank account no': str})

    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    df['bank account no'] = df['bank account no'].str.strip()
    df = df.fillna(0)
    df = df.replace('', 0).infer_objects(copy=False)
    df['date of invoice'] = df['date of invoice'].astype(str)

    if select.lower() == 'a':
        root = tk.Tk()
        file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
        root.destroy()
        df1 = pd.DataFrame(list(file2), columns=['file_path'])
        df1['file_name'] = df1['file_path'].apply(lambda x: x.split("/")[-1].split(".pdf")[0].split(".PDF")[0])

        i = -1
        time.sleep(2)
        while i < len(df) - 1:
            i += 1
            print(i)
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            a = str(df['date of invoice'][i])[:8]
            d = a[:4] + '/' + a[4:6] + '/' + a[6:]
            datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
            datetime1 = datetime0.date()
            year = datetime.date.strftime(datetime1, '%Y-%m-%d')
            quantity = df['quantity (tpa)'][i]
            gst_no = df['gst number'][i]
            gst_paid = df['gst paid'][i]
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            pdf_filename = df['pdf_filename'][i]

            try:
                pdf_file_index = df1[df1['file_name'] == df['pdf_filename'][i]].index[0]
            except:
                pdf_file_index = 0

            if pdf_file_index != 0:
                pdf_file = df1['file_path'][pdf_file_index]
                try:
                    invoice = pdf_path(pdf_file, pdf_filename)
                except:
                    invoice = ""
                if invoice:
                    result = entity_type(entity, state, category, material_type)

                    if result:
                        entity_value, state_value, category_value, material_type_value = result
                        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_material_procurement_details"

                        payload = json.dumps({
                            "registration_type": registration_type.lower(),
                            "entity_type": entity_value,
                            "registered_entity_id": None,
                            "registration_number": None,
                            "entity_state_id": state_value,
                            "entity_address": entity_address,
                            "entity_mobile": entity_mobile,
                            "plastic_type": material_type_value,
                            "plastic_category": category_value,
                            "financial_year": financial_year,
                            "year": year,
                            "quantity": quantity,
                            "recycled_plastic": int(recycled_plastic) if recycled_plastic else 0,
                            "gst_no": gst_no,
                            "gst_paid": float(gst_paid),
                            "invoice": invoice,
                            "invoice_number": None,
                            "entity_country": "India",
                            "name": name,
                            "address": "",
                            "gst_e_invoice": gst_e_invoice,
                            "user_id": 15677,
                            "company_id": 15677,
                            "other_type": other_type if other_type else "",
                        })

                        response = requests.post(url, headers=headers, data=payload, verify=False)
                        invoice_number = response.json().get("data", {}).get("invoice_number")

                        # Check if invoice number was generated
                        if not invoice_number:
                            errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })
                        else:
                            print(f"Invoice number generated: {invoice_number}")
                else:
                    errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })
    
    if select.lower() == 'b':
        df['epr invoice number'] = "na"
        i = -1
        time.sleep(2)
        while i < len(df) - 1:
            i += 1
            print(i)
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            quantity = str(df['quantity (tpa)'][i])
            gst_no = df['gst number'][i]
            gst_paid = str(df['gst paid'][i])
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            account_no = df['bank account no'][i]
            ifsc = df['ifsc code'][i]
            cat_1 = df['cat-1 container capacity'][i]
            if cat_1:
                if cat_1.lower() == "Containers > 0.9L and < 4.9 L".lower():
                    container_type = 1
                elif cat_1.lower() == "Containers > 4.9 L".lower():
                    container_type = 2
                elif cat_1.lower() == "Containers < 0.9 L".lower():
                    container_type = 0
                else:
                    container_type = 5
            else:
                container_type = 5

            result = entity_type(entity, state, category, material_type)

            if result:
                entity_value, state_value, category_value, material_type_value = result

            url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_sale_receipts"
            if registration_type.lower() == "unregistered":
                payload = json.dumps({
                    "type": registration_type.lower(),
                    "entity_type": entity_value,
                    "registered_entity_id": None,
                    "name": name,
                    "address": entity_address,
                    "entity_state_id": state_value,
                    "mobile": int(entity_mobile),
                    "financial_year": financial_year,
                    "gst_number": gst_no,
                    "account_no": account_no,
                    "ifsc": ifsc,
                    "gst_paid": gst_paid,
                    "quantity": quantity,
                    "gst_e_invoice": gst_e_invoice,
                    "plastic_category": category_value,
                    "recycled_plastic": recycled_plastic,
                    "container_type": container_type,
                    "plastic_type": material_type_value,
                    "epr_registration_number": None,
                    "invoice": "",
                    "company_id": 11579,
                    "not_registered": False,
                    "other_type": other_type if other_type else "",
                })
                response = requests.post(url, headers=headers, data=payload, verify=False)
                invoice_number = response.json().get("data", {}).get("invoice_number")

                if not invoice_number:
                    errors.append({
                        "gst_e_invoice": gst_e_invoice,
                        "status": "Your data is not uploaded."
                    })
                else:
                    print(f"Invoice number generated: {invoice_number}")
                
            else:
                registered_entity_id = entity_register_id(entity_value, name)
                if registered_entity_id:
                    payload = json.dumps({
                        "type": registration_type.lower(),
                        "financial_year": financial_year,
                        "account_no": account_no,
                        "ifsc": ifsc,
                        "gst_paid": gst_paid,
                        "quantity": quantity,
                        "gst_e_invoice": gst_e_invoice,
                        "plastic_category": category_value,
                        "recycled_plastic": recycled_plastic,
                        "entity_type": entity_value,
                        "registered_entity_id": registered_entity_id,
                        "container_type": container_type,
                        "plastic_type": material_type_value,
                        "state": state_value,
                        "entity_state_id": state_value,
                        "address": "xyz",
                        "mobile": entity_mobile,
                        "gst_number": "27AAACY3846K1ZX",
                        "epr_registration_number": None,
                        "invoice": "",
                        "company_id": 11579,
                        "not_registered": False,
                        "other_type": other_type if other_type else ""
                    })
                    response = requests.post(url, headers=headers, data=payload, verify=False)
                    invoice_number = response.json().get("data", {}).get("invoice_number")

                    if not invoice_number:
                        errors.append({
                            "gst_e_invoice": gst_e_invoice,
                            "status": "Your data is not uploaded."
                        })
                    else:
                        print(f"Invoice number generated: {invoice_number}")

    # Write errors to a CSV file
    if errors:
        error_df = pd.DataFrame(errors)
        error_file_path = "error_log.csv"
        error_df.to_csv(error_file_path, index=False)
        print(f"Errors logged to {error_file_path}")


# def producer():
    # global roww
    # global invoi
    # invoi=[]
    # global df
    # global mail
    # global errors
    # global invoicee
    # select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
    # root = tk.Tk()
    # file = fd.askopenfilename(parent=root, title='Choose a record file')
    # root.destroy()
    # if(select.lower()=='a'):
    #     root = tk.Tk()
    # #         file = fd.askopenfilename(parent=root, title='Choose a record file')
    #     file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
    #     root.destroy()
    #     df1 = pd.DataFrame(list(file2), columns =['file_path'])
    #     df1['file_name']=0
    #     for i in range(len(df1)):
    #         file2 = df1.loc[i, 'file_path'].split("/")
    #         file_name = file2[-1].split(".pdf")[0].split(".PDF")[0]
    #         df1.loc[i, 'file_name'] = file_name
    # # pd.set_option('future.no_silent_downcasting', True)

    # df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename': str, 'Bank account no': str})

    # df = df.astype(str)
    # df.columns = [x.lower() for x in df.columns]
    # df['bank account no'] = df['bank account no'].str.strip()
    # df = df.fillna(0)

    # # Explicitly call infer_objects to avoid the FutureWarning
    # df = df.replace('', 0).infer_objects(copy=False)

    # count = 0
    # try:
    #     df.upload_status
    # except AttributeError:
    #     df['upload_status'] = "no"
    # if(select.lower()=='b'):
    #     df['epr invoice number'] = "na"
    #     invoice=[]
    #     i=-1
    #     driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
    #     time.sleep(2)
    #     while i < len(df)-1:
    # #         while(i==0):
    #         driver.implicitly_wait(20)
    #         i=i+1
    #         print(i)
    #         #Add button
    #         try:
    #             time.sleep(1)
    #             click = driver.find_element(by=By.XPATH, value='//input[@autocomplete="off"][@type="text"]')
    #             custom_wait_clickable_and_click(click)
    #             add = WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH,'//button[contains(text(),"Add New")]')))
    #             custom_wait_clickable_and_click(add)
    #             time.sleep(1)

    #             #registration type nn
    #             try:
    #                 driver.find_element(by=By.XPATH, value='//*[@name="registration_type"]//input').send_keys(df['registration type'][i])
    #                 cl = WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                 custom_wait_clickable_and_click(cl)
    # #                     time.sleep(0.5)
    #             except:
    #                 errors.append('registeration error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             if(df['registration type'][i].lower()=='registered'):
    #                 #Type
    #                 cl = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//input[@value="entity"]')))
    #                 custom_wait_clickable_and_click(cl)


    #                 #financial year
    #                 try:
    #                     fy=14
    #                     time.sleep(0.5)
    #                     driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]//input').send_keys(df['financial year'][i])
    #                     cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                     custom_wait_clickable_and_click(cl)
    #                     fy=len(driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]/div[@class="ng-select-container ng-has-value"]').text)
    # #                     time.sleep(0.5)
    #                 except:
    #                     errors.append('financial year error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #GST nn
    # #                 try:
    # #                     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['gst number'][i])
    # #                 except:
    # #                     errors.append('GST error')
    # #                     invoicee.append(str(df['invoice number'][i]))
    # #                     pass

    #                 #bank account no 
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="account_no"]').send_keys(df['bank account no'][i])
    #                 except:
    #                     errors.append('bank account no error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #ifsc code 
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="ifsc"]').send_keys(df['ifsc code'][i])
    #                 except:
    #                     errors.append('ifsc code error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #gst paid
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="gst_paid"]').send_keys(df['gst paid'][i])
    #                 except:
    #                     errors.append('gst paid error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #Total Quantity (Tons)
    #                 try:
    #                     qty = round(float(df['quantity (tpa)'][i]), 3)
    #                     driver.find_element(by=By.XPATH, value='//input[@name="quantity"]').send_keys(qty)
    #                 except:
    #                     errors.append('Total Quantity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #invoice number
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="gst_invoice"]').send_keys(df['invoice number'][i])
    #                 except:
    #                     errors.append('invoice number error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #category of plastic
    #                 try:
    #                     if(df['category of plastic'][i].lower()=='cat iv'):
    #                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                 #% of recycled plastic packaging
    #                         try:
    #                             driver.find_element(by=By.XPATH, value='//input[@name="recycled_plastic"]').send_keys(str(df['recycled plastic %'][i]))
    #                         except:
    #                             errors.append('% of recycled plastic packaging error')
    #                             invoicee.append(str(df['invoice number'][i]))
    #                             pass    
    #                 except:
    #                     errors.append('category of plastic error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #entity type
    #                 try:
    #                     if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
    #                         driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                         #cat-1 container capacity nn
    #                         driver.find_element(by=By.XPATH, value='//*[@name="cat_1_sub_cat"]//input').send_keys(df['cat-1 container capacity'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1)
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)

    #                 except:
    #                     errors.append('entity type error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass


    #                 #plastic material type
    #                 try:
    #                     if(df['plastic material type'][i].lower()=='others'):
    #                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
    #                         #other plastic material type nn
    #                         driver.find_element(by=By.XPATH, value='//input[@name="other_type"]').send_keys(df['other plastic material type'][i])                        
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(0.5)
    #                 except:
    #                     errors.append('plastic material type error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #Name of the Entity Unregistered
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//*[@name="registered_entity_id"]//input').send_keys(str(df['name of entity'][i]).strip())
    #                     cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                     custom_wait_clickable_and_click(cl)
    #                 except:
    #                     errors.append('Name of the Entity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass


    #                 #address nn
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="address"]').clear()
    #                     driver.find_element(by=By.XPATH, value='//input[@name="address"]').send_keys('xyz')
    #                 except:
    #                     errors.append('Name of the Entity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass


    #                 #GST nn
    #                 try:
    #                     # if(df['entity type'][i].lower()=='brand owner'):
    #                     #     if(df['category of plastic'][i].lower()=='cat i' and df['plastic material type'][i].lower()=='others'):
    #                     driver.find_element(by=By.XPATH, value='//input[@name="gst_no"]').clear()
    #                     driver.find_element(by=By.XPATH, value='//input[@name="gst_no"]').send_keys('27AAACY3846K1ZX')
    #                     #     elif(df['category of plastic'][i].lower()!='cat i' and df['plastic material type'][i].lower()!='others'):
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').clear()
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys('27AAACY3846K1ZX')
    #                     #     elif((df['category of plastic'][i].lower()=='cat i' and df['plastic material type'][i].lower()!='others') or (df['category of plastic'][i].lower()!='cat i' and df['plastic material type'][i].lower()=='others')):
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').clear()
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys('27AAACY3846K1ZX')
    #                     # elif(df['entity type'][i].lower()!='brand owner'):
    #                     #     if(df['category of plastic'][i].lower()=='cat i' and df['plastic material type'][i].lower()=='others'):
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').clear()
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[12]/div/input').send_keys('27AAACY3846K1ZX')
    #                     #     elif(df['category of plastic'][i].lower()!='cat i' and df['plastic material type'][i].lower()!='others'):
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').clear()
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[10]/div/input').send_keys('27AAACY3846K1ZX')
    #                     #     elif((df['category of plastic'][i].lower()=='cat i' and df['plastic material type'][i].lower()!='others') or (df['category of plastic'][i].lower()!='cat i' and df['plastic material type'][i].lower()=='others')):
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').clear()
    #                     #         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys('27AAACY3846K1ZX')

    #                 except:                                    
    #                     pass





    # ########################################################################################################################
    #             else:
    #                 #Name of the Entity Unregistered nn
    #                 try:
    #                     if(df['registration type'][i].lower()=='unregistered'):
    #                         driver.find_element(by=By.XPATH, value='//input[@name="registered_entity_id_2"]').send_keys(df['name of entity'][i])
    #                     else:
    #                         pass
    #                 except:
    #                     errors.append('Name of the Entity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #address nn
    #                 try:
    #                     if(df['registration type'][i].lower()=='unregistered'):
    #                         driver.find_element(by=By.XPATH, value='//input[@name="address"]').send_keys(df['address'][i])
    #                     else:
    #                         pass
    #                 except:
    #                     errors.append('Name of the Entity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #state nn
    #                 try:
    #                     if(df['registration type'][i].lower()=='unregistered'):
    #                         time.sleep(0.5)
    #                         driver.find_element(by=By.XPATH, value='//*[@name="state_select"]//input').send_keys(df['state'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(2)
    #                     else:
    #                         pass
    #                 except:
    #                     errors.append('state error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #mobile number nn 
    #                 try:
    #                     if(df['registration type'][i].lower()=='unregistered'):
    #                         driver.find_element(by=By.XPATH, value='//input[@name="mobile_number"]').send_keys(str(df['mobile number'][i])[:10])
    #                     else:
    #                         pass
    #                 except:
    #                     errors.append('mobile number error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #financial year nn
    #                 try:
    #                     fy=14
    #                     time.sleep(0.5)
    #                     driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]//input').send_keys(df['financial year'][i])
    #                     cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                     custom_wait_clickable_and_click(cl)
    #                     fy=len(driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]/div[@class="ng-select-container ng-has-value"]').text)
    # #                     time.sleep(0.5)
    #                 except:
    #                     errors.append('financial year error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #GST nn
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="gst_no"]').send_keys(df['gst number'][i])
    #                 except:
    #                     errors.append('GST error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #bank account no nn 
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="account_no"]').send_keys(df['bank account no'][i])
    #                 except:
    #                     errors.append('bank account no error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #ifsc code nn 
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="ifsc"]').send_keys(df['ifsc code'][i])
    #                 except:
    #                     errors.append('ifsc code error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #gst paid nn
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="gst_paid"]').send_keys(df['gst paid'][i])
    #                 except:
    #                     errors.append('gst paid error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #Total Quantity (Tons) nn
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="quantity"]').send_keys(df['quantity (tpa)'][i])
    #                 except:
    #                     errors.append('Total Quantity error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #invoice number nn
    #                 try:
    #                     driver.find_element(by=By.XPATH, value='//input[@name="gst_invoice"]').send_keys(df['invoice number'][i])
    #                 except:
    #                     errors.append('invoice number error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #category of plastic nn
    #                 try:
    #                     if(df['category of plastic'][i].lower()=='cat iv'):
    #                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                 #% of recycled plastic packaging nn
    #                         try:
    #                             driver.find_element(by=By.XPATH, value='//input[@name="recycled_plastic"]').send_keys(str(df['recycled plastic %'][i]))
    #                         except:
    #                             errors.append('% of recycled plastic packaging error')
    #                             invoicee.append(str(df['invoice number'][i]))
    #                             pass    
    #                 except:
    #                     errors.append('category of plastic error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass

    #                 #entity type nn
    #                 try:
    #                     if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
    #                         driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                         #cat-1 container capacity nn
    #                         driver.find_element(by=By.XPATH, value='//*[@name="cat_1_sub_cat"]//input').send_keys(df['cat-1 container capacity'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1)
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)

    #                 except:
    #                     errors.append('entity type error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass


    #                 #plastic material type nn
    #                 try:
    #                     if(df['plastic material type'][i].lower()=='others'):
    #                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div')))
    #                         custom_wait_clickable_and_click(cl)
    #                         time.sleep(0.5)
    #                         #other plastic material type nn
    #                         driver.find_element(by=By.XPATH, value='//input[@name="other_type"]').send_keys(df['other plastic material type'][i])
    #                     else:
    #                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
    #                         cl=WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                         custom_wait_clickable_and_click(cl)
    # #                         time.sleep(0.5)
    #                 except:
    #                     errors.append('plastic material type error')
    #                     invoicee.append(str(df['invoice number'][i]))
    #                     pass





    # #             break
    #             #Submit nn
    # #             time.sleep(6)
    #             try:
    #                 if(fy<14):
    # #                         import pyperclip
    #                     #genrate epr invoice number
    #                     cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Invoice Number")]')))
    #                     custom_wait_clickable_and_click(cl)

    #                     #confirm button
    #                     cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Confirm"]')))
    #                     custom_wait_clickable_and_click(cl)

    #                     #copy epr-e invoice number
    #                     try:
    #                         cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Copy to clipboard"]')))
    #                         custom_wait_clickable_and_click(cl)
    #                         driver.find_element(by=By.XPATH, value='//input[@id="invoiceNumberCopy"]').text
    #                         inv = pyperclip.paste()
    #                         df['upload_status'][i] = "yes"
    #                         df['epr invoice number'][i] = inv
    #                         invoi.append(inv)
    #                     except:
    #                         invoi.append('none')

    #                     #close window
    # ##                        cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button')))
    # ##                        custom_wait_clickable_and_click(cl)
    #                     driver.refresh()


    #             except:
    # #                 try:
    #                 errors.append('Confirm error')
    #                 invoicee.append(str(df['invoice number'][i]))
    # #                     roww.append(i+2)
    #                 try:
    #                     close = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//h4/following::button[@aria-label="Close"][1]')))
    #                     custom_wait_clickable_and_click(close)
    #                 except:
    #                     time.sleep(1)
    #         except:
    #             invoi.append('none')
    #             driver.refresh()
    #             add = WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Add New")]')))
    #             custom_wait_clickable_and_click(add)
    #             driver.refresh()
    #             driver.implicitly_wait(15)
    # ##                driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
    #             time.sleep(3)
    # ##                i=i-1
    # ##        df['epr invoice number'] =0
    # ##        df['epr invoice number'] = invoi
    # ##        df.to_excel('new.xlsx') #creating new excel with the use of main excel





    # #----------------------------------------------------------------------------------------------------------------------    
    # #----------------------------------------------------------------------------------------------------------------------    
    # #----------------------------------------------------------------------------------------------------------------------     
    # elif(select=='a'):
    #     driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
    #     time.sleep(5)
    #     df['date of invoice']=df['date of invoice'].astype(str)
    #     i=-1
    #     time.sleep(2)
    #     while i < len(df)-1:
    #         driver.implicitly_wait(15)
    #         i=i+1
    #         print(i)
    #         #Add button nn
    #         try:
    #             time.sleep(1)
    #             click = driver.find_element(by=By.XPATH, value='//input[@autocomplete="off"][@type="text"]')
    #             custom_wait_clickable_and_click(click)
    #             driver.implicitly_wait(15)
    #             add = WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Add New")]')))

    #             custom_wait_clickable_and_click(add)
    # ##                time.sleep(0.5)
    #             driver.find_element(by=By.XPATH, value='//*[@name="registration_type"]//input').send_keys(df['registration type'][i])
    #             r_select = WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #             custom_wait_clickable_and_click(r_select)
    # #             except:
    # #                 errors.append('add button error')
    # #                 pass

    #             #entity type nn
    #             try:
    #                 driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
    #                 time.sleep(0.5)
    #                 et=WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                 custom_wait_clickable_and_click(et)
    # #                     time.sleep(1.5)
    #             except:
    #                 errors.append('entity type error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #Name of the Entity unregistred
    #             try:
    #                 driver.find_element(by=By.XPATH, value='//input[@name="registered_entity_id_2"]').send_keys(df['name of entity'][i])
    #                 #driver.find_element(by=By.XPATH, value='').click()
    #             except:
    #                 errors.append('Name of the Entity error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #state nn
    #             try:
    #                 time.sleep(0.5)
    #                 driver.find_element(by=By.XPATH, value='//*[@name="stateSelect"]//input').send_keys(df['state'][i])
    #                 cl=WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                 custom_wait_clickable_and_click(cl)
    # #                     time.sleep(2)
    #             except:
    #                 errors.append('state error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #address nn
    #             try:
    #                 driver.find_element(by=By.XPATH, value='//input[@name="address"]').send_keys(df['address'][i])
    #             except:
    #                 errors.append('Name of the Entity error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #mobile number nn
    #             try:
    #                 driver.find_element(by=By.XPATH, value='//input[@name="mobile_number"]').send_keys(str(df['mobile number'][i])[:10])
    #             except:
    #                 errors.append('mobile number error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #category of plastic nn
    #             try:
    #                 if(df['category of plastic'][i].lower()=='cat iv'):
    #                     driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
    #                     cl=WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                     custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #                 else:
    #                     driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
    #                     cl=WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                     custom_wait_clickable_and_click(cl)
    # #                         time.sleep(1.5)
    #             #% of recycled plastic packaging nn
    #                     try:
    #                         driver.find_element(by=By.XPATH, value='//input[@name="recycled_plastic"]').send_keys(str(df['recycled plastic %'][i]))
    #                     except:
    #                         errors.append('% of recycled plastic packaging error')
    #                         invoicee.append(str(df['invoice number'][i]))
    #                         pass    
    #             except:
    #                 errors.append('category of plastic error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #financial year nn
    #             try:
    #                 fy=14
    #                 driver.find_element(by=By.XPATH, value='//ng-select[@name="financial_year"]/div/span[1]').click()
    #                 driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]//input').send_keys(df['financial year'][i])
    #                 cl=WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
    #                 custom_wait_clickable_and_click(cl)
    #                 fy=len(driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]/div[@class="ng-select-container ng-has-value"]').text)
    # #                     time.sleep(0.5)
    #             except:
    #                 errors.append('financial year error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #DATE nn
    #             try:
    #                 a = str(df['date of invoice'][i])[:8]
    #                 d = a[:4]+'/'+a[4:6]+'/'+a[6:]
    #                 datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
    #                 datetime1 = datetime0.date()
    #                 datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
    #                 driver.find_element(by=By.XPATH, value='//input[@name="year"]').send_keys(datetime2)
    #             except:
    #                 errors.append('GST error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #Total Plastic Quantity nn
    #             try:
    #                 driver.find_element(by=By.XPATH, value='//input[@name="quantity"]').send_keys(df['quantity (tpa)'][i])
    #             except:
    #                 errors.append('GST error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #GST nn
    #             try:
    #                 driver.find_element(by=By.XPATH, value='//input[@name="gst_no"]').send_keys(df['gst number'][i])
    #             except:
    #                 errors.append('GST error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #gst paid nn
    #             try:
    #                 driver.find_element(by=By.XPATH, value='//input[@name="gst_paid"]').send_keys(str(df['gst paid'][i]))
    #             except:
    #                 errors.append('gst paid error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #invoice number nn
    #             try:
    #                 driver.find_element(by=By.XPATH, value='//input[@name="gst_e_invoice"]').send_keys(df['invoice number'][i])
    #             except:
    #                 errors.append('invoice number error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #Upload Invoice / GST E-Invoice nn
    #             try:
    #                 upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
    #                 pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
    #                 pdf_file = df1['file_path'][pdf_file_index]
    #                 upload_file.send_keys(pdf_file)
    #                 time.sleep(1)

    #             except:
    #                 errors.append('Invoice upload error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass

    #             #plastic material type nn
    #             try:
    #                 if(df['plastic material type'][i].lower()=='others'):
    #                     driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
    #                     cl=WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div')))
    #                     custom_wait_clickable_and_click(cl)
    # #                         time.sleep(0.5)
    #                     #other plastic material type nn
    #                     driver.find_element(by=By.XPATH, value='//input[@name="other_type"]').send_keys(df['other plastic material type'][i])
    #                 else:
    #                     driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
    #                     cl=WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div')))
    #                     custom_wait_clickable_and_click(cl)
    # #                         time.sleep(0.5)
    #             except:
    #                 errors.append('plastic material type error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 pass
    # #                 break
    #             #Submit
    #             try:
    #                 if(fy<14):
    #                     cl=WebDriverWait(driver, 3).until(
    #     EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Submit")]')))
    #                     custom_wait_clickable_and_click(cl)
    #                     try:
    #                         driver.implicitly_wait(1)
    #                         close = driver.find_element(by=By.XPATH, value='//button[@id="closeMaterialProcurementPopup"]/span').click()
    #                         errors.append('Submit error')
    #                         invoicee.append(str(df['invoice number'][i]))
    # #                             roww.append(i+2)
    #                     except:
    #                         df['upload_status'][i] = "yes" 
    #                         pass
    #                     time.sleep(0.5)
    #                 else:
    #                     df['upload_status'][i] = "no"
    #                     raise error
    #             except:
    #                 df['upload_status'][i] = "no"
    #                 errors.append('Submit error')
    #                 invoicee.append(str(df['invoice number'][i]))
    #                 close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="closeMaterialProcurementPopup"]/span')))
    #                 custom_wait_clickable_and_click(close)
    #                 time.sleep(1)
    #                 pass
    #         except:
    #             df['upload_status'][i] = "no"
    #             driver.refresh()
    #             add = WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Add New")]')))
    #             custom_wait_clickable_and_click(add)
    #             driver.refresh()
    #             driver.implicitly_wait(15)
    # ##                driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
    #             time.sleep(2)
    # ##                i=i-1
    #             pass


            



def pdf_upload():
    global errors
    global invoicee
    global roww

    now = datetime.datetime.now()
    directory = str(now.strftime("final_pdf" + "%d%m%Y_%H%M%S"))
    parent_dir = Path.cwd()
    path = os.path.join(parent_dir, directory)

    os.mkdir(path)
    parent_dir = path.replace('\\', '/')

    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a newly created record file')
    files = fd.askopenfilenames(parent=root, title='Choose merged pdf files')
    root.destroy()

    df = pd.DataFrame(list(files), columns=['file_path'])
    df1 = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename': str})
    df1.columns = (x.lower() for x in df1.columns)

    df['file_name'] = [os.path.basename(f).split(".pdf")[0].split(".PDF")[0] for f in df['file_path']]

    errors = []

    for i in range(len(df1)):
        try:
            print(f"Processing row {i+1}/{len(df1)}")
            # Generate PDF based on the record file data
            pdf_gen(df1['epr invoice number'][i], df1['registration type'][i], df1['entity type'][i],
                    df1['name of entity'][i], df1['plastic material type'][i], df1['other plastic material type'][i],
                    df1['category of plastic'][i], df1['financial year'][i], 
                    round(df1['quantity (tpa)'][i], 3), df1['gst paid'][i])

            # Attempt to merge with the corresponding file
            mergedObject = PdfMerger()
            mergedObject.append(PdfReader("table.pdf", 'rb'))
            pdf_file_index = df[df['file_name'] == df1['pdf_filename'][i]].index

            if pdf_file_index.empty:
                raise FileNotFoundError(f"No matching file found for {df1['pdf_filename'][i]}")

            mergedObject.append(PdfReader(df['file_path'][pdf_file_index[0]], 'rb'))
            filename = f"{parent_dir}/{df1['pdf_filename'][i]}.pdf"
            mergedObject.write(filename)

        except Exception as e:
            errors.append({
                'pdf_filename': df1['pdf_filename'][i],
                'error_message': str(e)
            })
            print(f"Error: {e}")

    # Log errors to an Excel file
    if errors:
        error_df = pd.DataFrame(errors)
        error_file = f"{parent_dir}/error_log.xlsx"
        error_df.to_excel(error_file, index=False)
        print(f"Errors encountered. Please check the error log: {error_file}")
    else:
        print("All files processed successfully.")

    print(f"ALL FILES GENERATED SUCCESSFULLY, PLEASE CHECK YOUR FOLDER: {parent_dir}")

def pdf_upload2():
    root = tk.Tk()
    root.withdraw()

    # Open file dialog to select base file
    file_path = fd.askopenfilename(parent=root, title='Choose base file')

    # Open file dialog to select multiple PDF files
    pdf_paths = fd.askopenfilenames(parent=root, title='Choose PDF files')  # List of selected PDF file paths

    # Close the Tkinter root window after file selection
    root.destroy()

    # Process the selected files
    df = pd.read_excel(file_path)
##    login_token = driver.get_cookies()[0]["value"]
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)

    date_from_value = driver.find_element(By.ID, 'date_from').get_attribute('value')
    date_to_value = driver.find_element(By.ID, 'date_to').get_attribute('value')

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'login-token={login_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    def find_pdf_by_filename(pdf_paths, pdf_filename):
        for pdf_path in pdf_paths:
            if os.path.basename(pdf_path) == f"{pdf_filename}.pdf":
                return pdf_path
        return None

    def upload_pdf_path(pdf_path, pdf_filename, sales_inc_id, registration_type):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pwp/upload_image"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Cookie': f'login-token={login_token}',
        }
        payload = {'section': 'upload_filepath'}
        files = [
            ('file', (f"{pdf_filename}.pdf", open(f'{pdf_path}', 'rb'), 'application/pdf'))
        ]
        try:
            response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
        except:
            time.sleep(20)
            response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
        print(response.text)
        path = response.json()["data"]["path"]

        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/uploaded_invoice_receipts"

        payload = json.dumps({
            "type": registration_type.lower(),
            "path": f"{path}",
            "sales_inc_id": sales_inc_id
        })
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        except:
            time.sleep(20)
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        print(response)
        status = response.json()["status"]
        print(status, pdf_filename, sales_inc_id)

    def scrape_dashboard_data(pdf_paths):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_materials_sold"
        
        payload = json.dumps({
            "page": 1, 
            "records": 10000, 
            "filters": {}, 
            "page_count": 50, 
            "page_no": 1, 
            "no_of_records": 50, 
            "search_text": "", 
            "from_date": f"{date_from_value}", 
            "to_date": f"{date_to_value}", 
            "sortData": ""
        })
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        except:
            time.sleep(20)
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        rows = response.json()["data"]["tableData"]["bodyContent"]

        entry_count = 0  # Counter for successfully uploaded entries
        
        for row in rows:
            registration_type = row["registration_type"]
            sales_inc_id = row["sales_inc_id"]
            b166 = int(row["invoice_no"])
            b177 = row["gst_e_invoice"]
            b188 = row["status"]

            if b188 == "pending":
                matching_row = df[df['epr invoice number'] == b166]

                if not matching_row.empty:  # Check if matching_row has data
                    pdf_filename = matching_row.iloc[0]['pdf_filename']

                    pdf_path = find_pdf_by_filename(pdf_paths, pdf_filename)
                    if pdf_path:
                        print(f"PDF found: {pdf_path}")
                        upload_pdf_path(pdf_path, pdf_filename, sales_inc_id, registration_type)
                        entry_count += 1  # Increment the counter after a successful upload
                else:
                    print(f"No matching record found for invoice number {b166}")

        print(f"Total entries processed: {entry_count}")  # Print the total count at the end

    scrape_dashboard_data(pdf_paths)

##def pdf_upload2():
####    global driver
##    driver.implicitly_wait(3)
##    global errors
##    global invoicee
##    errors = []
##    invoicee = []
##    #Finding epr invoice number using scrapping
##    ssa=easygui.enterbox("OPEN THE PAGE ON PORTAL WHERE YOU WANT TO UPLOAD PDF AND THEN PRESS OK")
##    job=driver.find_element(by=By.ID, value='ScrollableSimpleTableBody')
##    soup=BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')
##    a=soup.find_all("span",class_="ng-star-inserted")
##    if(len(a)==0):
##        a=soup.find_all("td",class_="row-item")
##    z=[]
##    for i in a:
##    #     print(i.text.replace("\n","").strip())
##        z.append(i.text.replace("\n","").strip())
##
##    EPR=[]
##
##    i=0
##    while i<len(z):
##        EPR.append(z[i+14])
##        i=i+19
##
##    df3 = pd.DataFrame({
##                   'epr_no': EPR,
##                   })
##    print(df3)
##
##    #Upload Invoice / GST E-Invoice
##    root = tk.Tk()
##    file = fd.askopenfilename(parent=root, title='Choose a record file')
##    file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
##    root.destroy()
##    df1 = pd.DataFrame(list(file2), columns =['file_path'])
##    df1['file_name']=0
##    for i in range(len(df1)):
##        file2 = df1.loc[i, 'file_path'].split("/")
##        file_name = file2[-1].split(".pdf")[0].split(".PDF")[0]
##        df1.loc[i, 'file_name'] = file_name
##
##    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename': str})
##    for i in range(0, 50):
##        try:
##            try:# Filter the DataFrame to find the matching row
##                matching_rows = df[df['epr invoice number'] == int(df3['epr_no'][i])]
##            except:
##                matching_rows = df[df['epr invoice number'] == (df3['epr_no'][i])]
##            # Check if there are any matching rows
##            if matching_rows.empty:
##                raise ValueError(f"No matching invoice found for epr_no: {df3['epr_no'][i]}")
##            
##            # Get the index for uploading
##            IndexForUpload = matching_rows.index[0]
##            
##            # Proceed with the rest of the logic
##            click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//table/tbody/tr[{i+1}]/td[17]/span')))
##            custom_wait_clickable_and_click(click)
##            upload_file = driver.find_element(by=By.XPATH, value='//*[@id="salesInvoiceUpload"]')
##            pdfindex = df1[df1['file_name'] == str(df['pdf_filename'][IndexForUpload])].index[0]
##            pdf_file = df1['file_path'][pdfindex]
##            upload_file.send_keys(pdf_file)
##            time.sleep(2)
##            upload = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[3]/div/div/div[3]/button[1]')))
##            custom_wait_clickable_and_click(upload)
##            time.sleep(1)
##        except Exception as e:
##            errors.append(f"Invoice upload error for EPR no: {df3['epr_no'][i]} - {str(e)}")
##            invoicee.append(str(df3['epr_no'][i]))
##            print(i, "><>", str(e))
##            try:
##                close = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/app-pibo-operations/div[3]/div/div/div[3]/button[2]').click()
##            except:
##                pass
##
def brand_owner():
##def producer():
##    login_token = driver.get_cookies()[0]["value"]
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)
##    print(login_token)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'login-token={login_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    
    errors = []
    
    def entity_type(entity, state, category, material_type):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/get_pibo_dropdown_data"
        
        payload = json.dumps({
            "type": [
                "entity_type_for_sales",
                "states_list",
                "plastic_category",
                "plastic_material_type"
            ],
            "company_id": 15247,
            "section": "procurement"
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", {})
            entity_value = next((i["value"] for i in datas.get("entity_type_for_sales", []) if entity.lower() == i["label"].lower()), None)
            state_value = next((i["value"] for i in datas.get("states_list", []) if state.lower() == i["label"].lower()), None)
            category_value = next((i["value"] for i in datas.get("plastic_category", []) if category.lower() == i["label"].lower()), None)
            material_type_value = next((i["value"] for i in datas.get("plastic_material_type", []) if material_type.lower() == i["label"].lower()), None)

            return entity_value, state_value, category_value, material_type_value
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    def pdf_path(pdf_path, pdf_filename):

        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pwp/upload_image"
        headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Cookie': f'login-token={login_token}',
                    }
        payload = {'section': 'upload_filepath'}
        files=[
        ('file',(f"{pdf_filename}.pdf",open(f'{pdf_path}','rb'),'application/pdf'))
        ]
        response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)
        path = response.json()["data"]["path"]
        return path

    def entity_register_id(entity_value, name):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_entity_name"

        payload = json.dumps({
        "entity_type": entity_value
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", [])
            registered_id = next((i["value"] for i in datas if name.lower().strip() == i["label"].lower().strip()), None)
            return registered_id
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    root.destroy()

    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename': str, 'Bank account no': str})

    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    df['bank account no'] = df['bank account no'].str.strip()
    df = df.fillna(0)
    df = df.replace('', 0).infer_objects(copy=False)
    df['date of invoice'] = df['date of invoice'].astype(str)

    # if select.lower() == 'a':
    root = tk.Tk()
    file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
    root.destroy()
    df1 = pd.DataFrame(list(file2), columns=['file_path'])
    df1['file_name'] = df1['file_path'].apply(lambda x: x.split("/")[-1].split(".pdf")[0].split(".PDF")[0])

    i = -1
    time.sleep(2)
    while i < len(df) - 1:
        i += 1
        print(i)
        registration_type = df['registration type'][i]
        entity = df['entity type'][i]
        name = df['name of entity'][i]
        state = df['state'][i]
        entity_address = df['address'][i]
        entity_mobile = str(df['mobile number'][i])[:10]
        category = df['category of plastic'][i]
        recycled_plastic = str(df['recycled plastic %'][i])
        financial_year = df['financial year'][i]
        a = str(df['date of invoice'][i])[:8]
        d = a[:4] + '/' + a[4:6] + '/' + a[6:]
        datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
        datetime1 = datetime0.date()
        year = datetime.date.strftime(datetime1, '%Y-%m-%d')
        quantity = df['quantity (tpa)'][i]
        gst_no = df['gst number'][i]
        gst_paid = df['gst paid'][i]
        gst_e_invoice = df['invoice number'][i]
        material_type = df['plastic material type'][i]
        other_type = df['other plastic material type'][i]
        pdf_filename = df['pdf_filename'][i]

        try:
            pdf_file_index = df1[df1['file_name'] == df['pdf_filename'][i]].index[0]
        except:
            pdf_file_index = 0

        if pdf_file_index != 0:
            pdf_file = df1['file_path'][pdf_file_index]
            try:
                invoice = pdf_path(pdf_file, pdf_filename)
            except:
                invoice = ""
            if invoice:
                result = entity_type(entity, state, category, material_type)

                if result:
                    entity_value, state_value, category_value, material_type_value = result
                    url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_material_procurement_details"

                    payload = json.dumps({
                        "registration_type": registration_type.lower(),
                        "entity_type": entity_value,
                        "registered_entity_id": None,
                        "registration_number": None,
                        "entity_state_id": state_value,
                        "entity_address": entity_address,
                        "entity_mobile": entity_mobile,
                        "plastic_type": material_type_value,
                        "plastic_category": category_value,
                        "financial_year": financial_year,
                        "year": year,
                        "quantity": quantity,
                        "recycled_plastic": int(recycled_plastic) if recycled_plastic else 0,
                        "gst_no": gst_no,
                        "gst_paid": float(gst_paid),
                        "invoice": invoice,
                        "invoice_number": None,
                        "entity_country": "India",
                        "name": name,
                        "address": "",
                        "gst_e_invoice": gst_e_invoice,
                        "user_id": 15677,
                        "company_id": 15677,
                        "other_type": other_type if other_type else "",
                    })

                    response = requests.post(url, headers=headers, data=payload, verify=False)
                    invoice_number = response.json().get("data", {}).get("invoice_number")

                    # Check if invoice number was generated
                    if not invoice_number:
                        errors.append({
                            "gst_e_invoice": gst_e_invoice,
                            "status": "Your data is not uploaded."
                        })
                    else:
                        print(f"Invoice number generated: {invoice_number}")
            else:
                errors.append({
                            "gst_e_invoice": gst_e_invoice,
                            "status": "Your data is not uploaded."
                        })


    if errors:
        error_df = pd.DataFrame(errors)
        error_file_path = "error_log.csv"
        error_df.to_csv(error_file_path, index=False)
        print(f"Errors logged to {error_file_path}")


# def brand_owner():
#     global errors
#     global invoicee
#     global roww
#     global roww
#     driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
#     root = tk.Tk()
#     file = fd.askopenfilename(parent=root, title='Choose a record file')
#     file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
#     root.destroy()
#     df1 = pd.DataFrame(list(file2), columns =['file_path'])
#     df1['file_name']=0
#     for i in range(len(df1)):
#         file2 = df1['file_path'][i].split("/")
#         file_name = file2[-1].split(".pdf")[0]
#         df1['file_name'][i]=file_name
#     df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str})

# #     now = datetime.datetime.now()
# #     val = (str(mail), "brand_owner",'',str(len(df)),str(now.strftime("%d/%m/%Y %H-%M-%S")))
# #     mycursor.execute(sql, val)
# #     mydb.commit()
    
#     df = df.astype(str)
#     df.columns = [x.lower() for x in df.columns]
#     df['date of invoice']=df['date of invoice'].astype(str)
#     #     df['date of invoice'] = df['date of invoice'].apply(lambda x: x.replace("-", "/"))
#     driver.implicitly_wait(15)
#     i=-1
#     df = df.fillna(0)
#     df = df.replace('', 0)
#     try:
#         df.upload_status
#     except:
#         df['upload_status'] = "no" 
#     while i < len(df)-1:
#         driver.implicitly_wait(15)
#         i=i+1
#         print(i)
#         #Add button
#         try:
#             time.sleep(1)
#             click = driver.find_element(by=By.XPATH, value='//input[@autocomplete="off"][@type="text"]')
#             custom_wait_clickable_and_click(click)
#             driver.implicitly_wait(15)
#             add = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Add New")]')))
#             custom_wait_clickable_and_click(add)
#             time.sleep(0.5)
#             r_click = driver.find_element(by=By.XPATH, value='//*[@name="registration_type"]//input').send_keys('unregistered')
#             r_select = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#             custom_wait_clickable_and_click(r_select)

#     #         except:
#     #             errors.append('add button error')
#     #             break



#             #Name of the Entity unregistred
#             try:
#                 driver.find_element(by=By.XPATH, value='//input[@name="registered_entity_id_2"]').send_keys(df['name of entity'][i])
#                 #driver.find_element(by=By.XPATH, value='').click()
#             except:
#                 errors.append('Name of the Entity error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #state
#             try:
#                 time.sleep(0.5)
#                 driver.find_element(by=By.XPATH, value='//*[@name="stateSelect"]//input').send_keys(df['state'][i])
#                 cl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                 custom_wait_clickable_and_click(cl)
# #                 time.sleep(2)
#             except:
#                 errors.append('state error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #address
#             try:
#                 driver.find_element(by=By.XPATH, value='//input[@name="address"]').send_keys(df['address'][i])
#             except:
#                 errors.append('Name of the Entity error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #mobile number
#             try:
#                 driver.find_element(by=By.XPATH, value='//input[@name="mobile_number"]').send_keys(str(df['mobile number'][i])[:10])
#             except:
#                 errors.append('mobile number error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass



#             #financial year
#             try:
#                 fy=21
#                 driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]//input').send_keys(df['financial year'][i])
#                 cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                 custom_wait_clickable_and_click(cl)
#                 fy=len(driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]/div[@class="ng-select-container ng-has-value"]').text)
# #                 time.sleep(0.5)
#             except:
#                 errors.append('financial year error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #DATE
#             try:
#                 a = str(df['date of invoice'][i])[:8]
#                 d = a[:4]+'/'+a[4:6]+'/'+a[6:]
#                 datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
#                 datetime1 = datetime0.date()
#                 datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
#                 driver.find_element(by=By.XPATH, value='//input[@name="year"]').send_keys(datetime2)
#             except:
#                 errors.append('GST error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #Total Plastic Quantity
#             try:
#                 driver.find_element(by=By.XPATH, value='//input[@name="quantity"]').send_keys(df['quantity (tpa)'][i])
#             except:
#                 errors.append('GST error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #GST
#             try:
#                 driver.find_element(by=By.XPATH, value='//input[@name="gst_no"]').send_keys(df['gst number'][i])
#             except:
#                 errors.append('GST error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #gst paid
#             try:
#                 driver.find_element(by=By.XPATH, value='//input[@name="gst_paid"]').send_keys(str(df['gst paid'][i]))
#             except:
#                 errors.append('gst paid error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #invoice number
#             try:
#                 driver.find_element(by=By.XPATH, value='//input[@name="gst_e_invoice"]').send_keys(df['invoice number'][i])
#             except:
#                 errors.append('invoice number error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #Upload Invoice / GST E-Invoice
#             try:
#                 upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
#                 pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
#                 pdf_file = df1['file_path'][pdf_file_index]
#                 upload_file.send_keys(pdf_file)
#                 time.sleep(1)

#             except:
#                 errors.append('Invoice upload error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #category of plastic
#             try:
#                 driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
#                 cl=driver.find_element(by=By.XPATH, value='//ng-dropdown-panel/div/div[2]/div[1]')
#                 custom_wait_clickable_and_click(cl)

#             except:
#                 errors.append('category of plastic error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             #entity type
#             try:
#                 if(df['category of plastic'][i].lower()=='cat i'):
#                     driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1.5)
#                     #cat-1 container capacity
#                     driver.find_element(by=By.XPATH, value='//*[@name="cat_1_sub_cat"]//input').send_keys(df['cat-1 container capacity'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1)
#                 else:
#                     driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1.5)

#             except:
#                 errors.append('entity type error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass
            
            
#             #financial year
#             try:
#                 if(df['category of plastic'][i].lower()!='cat i'):
#                     fy=21
#                     time.sleep(0.5)
#                     cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//ng-select[@name="financial_year"]/div/span[1]')))
#                     custom_wait_clickable_and_click(cl)
#                     driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]//input').send_keys(df['financial year'][i])
#                     cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
#                     fy=len(driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]/div[@class="ng-select-container ng-has-value"]').text)
#     #                 time.sleep(0.5)
#                 else:
#                     fy=21
#                     time.sleep(0.5)
#                     cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//ng-select[@name="financial_year"]/div/span[1]')))
#                     custom_wait_clickable_and_click(cl)
#                     driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]//input').send_keys(df['financial year'][i])
#                     cl=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
#                     fy=len(driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]/div[@class="ng-select-container ng-has-value"]').text)
#     #                 time.sleep(0.5)
#             except:
#                 errors.append('financial year error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass
            
            

#             #plastic material type
#             try:
#                 time.sleep(1)
#                 if(df['plastic material type'][i].lower()=='others'):
#                     driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(0.5)
#                     #other plastic material type
#                     driver.find_element(by=By.XPATH, value='//input[@name="other_type"]').send_keys(df['other plastic material type'][i])

#                 else:
#                     driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(0.5)
#             except:
#                 errors.append('plastic material type error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 pass

#             try:
#                 if(df['plastic material type'][i].lower()=='others' and df['category of plastic'][i].lower()=='cat i'):
#                     driver.find_element(by=By.XPATH, value='//input[@name="year"]').send_keys(datetime2)
#                     driver.find_element(by=By.XPATH, value='//input[@name="recycled_plastic"]').send_keys(str(df['recycled plastic %'][i]))
#                 elif(df['plastic material type'][i].lower()=='others' and df['category of plastic'][i].lower()!='cat i'):
#                     driver.find_element(by=By.XPATH, value='//input[@name="year"]').send_keys(datetime2)
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="recycled_plastic"]').send_keys(str(df['recycled plastic %'][i]))
#                     except:
#                         pass
#                 elif(df['category of plastic'][i].lower()=='cat i' and df['plastic material type'][i].lower()!='others'):
#                     driver.find_element(by=By.XPATH, value='//input[@name="year"]').send_keys(datetime2)
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="recycled_plastic"]').send_keys(str(df['recycled plastic %'][i]))
#                     except:
#                         pass
#                 else:
#                     driver.find_element(by=By.XPATH, value='//input[@name="year"]').send_keys(datetime2)
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="recycled_plastic"]').send_keys(str(df['recycled plastic %'][i]))
#                     except:
#                         pass
#             except:
#                 pass
 
#             #Submit
#             try:
#                 if(fy<21):
#                     cl=WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Submit")]')))
#                     custom_wait_clickable_and_click(cl)
#                     time.sleep(3)
#                     try:
#                         driver.implicitly_wait(1)
#                         driver.find_element(by=By.XPATH, value='/html/body/app-root/app-epr/kl-toastr/toaster-container/div/div/div/div[2]/div').click()
#                         driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[1]/button/span').click()
#                         df['upload_status'][i] = "no" 
#                         errors.append('Submit error')
#                         invoicee.append(str(df['invoice number'][i]))
#     #                     roww.append(i+2)
#                     except:
#                         df['upload_status'][i] = "yes" 
#                         pass
#                     time.sleep(0.5)
#                 else:
#                     df['upload_status'][i] = "no"
#                     raise error
#             except:
#                 df['upload_status'][i] = "no"
#                 errors.append('Submit error')
#                 invoicee.append(str(df['invoice number'][i]))
#                 close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button/span')))
#                 custom_wait_clickable_and_click(close)
#         except:
#             df['upload_status'][i] = "no"
#             driver.refresh()
#             add = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-epr/app-pibo-operations/div[1]/div[2]/div/div/div/div/div[2]/button')))
#             custom_wait_clickable_and_click(add)
#             driver.refresh()
#             driver.implicitly_wait(15)
# ##            driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
#             time.sleep(2)
# ##            i=i-1
#             pass
            

def importer():
##    login_token = driver.get_cookies()[0]["value"]
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)
##    print(login_token)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'login-token={login_token}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    
    errors = []
    
    def entity_type(entity, state, category, material_type):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/get_pibo_dropdown_data"
        
        payload = json.dumps({
            "type": [
                "entity_type_for_sales",
                "states_list",
                "plastic_category",
                "plastic_material_type"
            ],
            "company_id": 15247,
            "section": "procurement"
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", {})
            entity_value = next((i["value"] for i in datas.get("entity_type_for_sales", []) if entity.lower() == i["label"].lower()), None)
            state_value = next((i["value"] for i in datas.get("states_list", []) if state.lower() == i["label"].lower()), None)
            category_value = next((i["value"] for i in datas.get("plastic_category", []) if category.lower() == i["label"].lower()), None)
            material_type_value = next((i["value"] for i in datas.get("plastic_material_type", []) if material_type.lower() == i["label"].lower()), None)

            return entity_value, state_value, category_value, material_type_value
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    def pdf_path(pdf_path, pdf_filename):

        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pwp/upload_image"
        headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'Cookie': f'login-token={login_token}',
                    }
        payload = {'section': 'upload_filepath'}
        files=[
        ('file',(f"{pdf_filename}.pdf",open(f'{pdf_path}','rb'),'application/pdf'))
        ]
        response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)
        path = response.json()["data"]["path"]
        return path

    def entity_register_id(entity_value, name):
        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_entity_name"

        payload = json.dumps({
        "entity_type": entity_value
        })

        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        try:
            datas = response.json().get("data", [])
            registered_id = next((i["value"] for i in datas if name.lower().strip() == i["label"].lower().strip()), None)
            return registered_id
        
        except KeyError as e:
            print(f"Error parsing data: {e}")
            return None

    select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs")
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose a record file')
    root.destroy()

    df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename': str, 'Bank account no': str})

    df = df.astype(str)
    df.columns = [x.lower() for x in df.columns]
    df['bank account no'] = df['bank account no'].str.strip()
    df = df.fillna(0)
    df = df.replace('', 0).infer_objects(copy=False)
    df['date of invoice'] = df['date of invoice'].astype(str)

    if select.lower() == 'a':
        root = tk.Tk()
        file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
        root.destroy()
        df1 = pd.DataFrame(list(file2), columns=['file_path'])
        df1['file_name'] = df1['file_path'].apply(lambda x: x.split("/")[-1].split(".pdf")[0].split(".PDF")[0])

        i = -1
        time.sleep(2)
        while i < len(df) - 1:
            i += 1
            print(i)
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            a = str(df['date of invoice'][i])[:8]
            d = a[:4] + '/' + a[4:6] + '/' + a[6:]
            datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
            datetime1 = datetime0.date()
            year = datetime.date.strftime(datetime1, '%Y-%m-%d')
            quantity = df['quantity (tpa)'][i]
            gst_no = df['gst number'][i]
            gst_paid = df['gst paid'][i]
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            pdf_filename = df['pdf_filename'][i]

            try:
                pdf_file_index = df1[df1['file_name'] == df['pdf_filename'][i]].index[0]
            except:
                pdf_file_index = 0

            if pdf_file_index != 0:
                pdf_file = df1['file_path'][pdf_file_index]
                try:
                    invoice = pdf_path(pdf_file, pdf_filename)
                except:
                    invoice = ""
                if invoice:

                    result = entity_type(entity, state, category, material_type)

                    if result:
                        entity_value, state_value, category_value, material_type_value = result
                        url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_material_procurement_details"

                        payload = json.dumps({
                            "registration_type": registration_type.lower(),
                            "entity_type": entity_value,
                            "registered_entity_id": None,
                            "registration_number": None,
                            "entity_state_id": state_value,
                            "entity_address": entity_address,
                            "entity_mobile": entity_mobile,
                            "plastic_type": material_type_value,
                            "plastic_category": category_value,
                            "financial_year": financial_year,
                            "year": year,
                            "quantity": quantity,
                            "recycled_plastic": int(recycled_plastic) if recycled_plastic else 0,
                            "gst_no": gst_no,
                            "gst_paid": float(gst_paid),
                            "invoice": invoice,
                            "invoice_number": None,
                            "entity_country": "India",
                            "name": name,
                            "address": "",
                            "gst_e_invoice": gst_e_invoice,
                            "user_id": 15677,
                            "company_id": 15677,
                            "other_type": other_type if other_type else "",
                        })

                        response = requests.post(url, headers=headers, data=payload, verify=False)
                        invoice_number = response.json().get("data", {}).get("invoice_number")

                        # Check if invoice number was generated
                        if not invoice_number:
                            errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })
                        else:
                            print(f"Invoice number generated: {invoice_number}")
                
                else:
                    errors.append({
                                "gst_e_invoice": gst_e_invoice,
                                "status": "Your data is not uploaded."
                            })

    
    if select.lower() == 'b':
        df['epr invoice number'] = "na"
        i = -1
        time.sleep(2)
        while i < len(df) - 1:
            i += 1
            print(i)
            registration_type = df['registration type'][i]
            entity = df['entity type'][i]
            name = df['name of entity'][i]
            state = df['state'][i]
            entity_address = df['address'][i]
            entity_mobile = str(df['mobile number'][i])[:10]
            category = df['category of plastic'][i]
            recycled_plastic = str(df['recycled plastic %'][i])
            financial_year = df['financial year'][i]
            quantity = str(df['quantity (tpa)'][i])
            gst_no = df['gst number'][i]
            gst_paid = str(df['gst paid'][i])
            gst_e_invoice = df['invoice number'][i]
            material_type = df['plastic material type'][i]
            other_type = df['other plastic material type'][i]
            account_no = df['bank account no'][i]
            ifsc = df['ifsc code'][i]
            cat_1 = df['cat-1 container capacity'][i]
            if cat_1:
                if cat_1.lower() == "Containers > 0.9L and < 4.9 L".lower():
                    container_type = 1
                elif cat_1.lower() == "Containers > 4.9 L".lower():
                    container_type = 2
                elif cat_1.lower() == "Containers < 0.9 L".lower():
                    container_type = 0
                else:
                    container_type = 5
            else:
                container_type = 5

            result = entity_type(entity, state, category, material_type)

            if result:
                entity_value, state_value, category_value, material_type_value = result

            url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/save_sale_receipts"
            if registration_type.lower() == "unregistered":
                payload = json.dumps({
                    "type": registration_type.lower(),
                    "entity_type": entity_value,
                    "registered_entity_id": None,
                    "name": name,
                    "address": entity_address,
                    "entity_state_id": state_value,
                    "mobile": int(entity_mobile),
                    "financial_year": financial_year,
                    "gst_number": gst_no,
                    "account_no": account_no,
                    "ifsc": ifsc,
                    "gst_paid": gst_paid,
                    "quantity": quantity,
                    "gst_e_invoice": gst_e_invoice,
                    "plastic_category": category_value,
                    "recycled_plastic": recycled_plastic,
                    "container_type": container_type,
                    "plastic_type": material_type_value,
                    "epr_registration_number": None,
                    "invoice": "",
                    "company_id": 11579,
                    "not_registered": False,
                    "other_type": other_type if other_type else "",
                })
                response = requests.post(url, headers=headers, data=payload, verify=False)
                invoice_number = response.json().get("data", {}).get("invoice_number")

                if not invoice_number:
                    errors.append({
                        "gst_e_invoice": gst_e_invoice,
                        "status": "Your data is not uploaded."
                    })
                else:
                    print(f"Invoice number generated: {invoice_number}")
                
            else:
                registered_entity_id = entity_register_id(entity_value, name)
                if registered_entity_id:
                    payload = json.dumps({
                        "type": registration_type.lower(),
                        "financial_year": financial_year,
                        "account_no": account_no,
                        "ifsc": ifsc,
                        "gst_paid": gst_paid,
                        "quantity": quantity,
                        "gst_e_invoice": gst_e_invoice,
                        "plastic_category": category_value,
                        "recycled_plastic": recycled_plastic,
                        "entity_type": entity_value,
                        "registered_entity_id": registered_entity_id,
                        "container_type": container_type,
                        "plastic_type": material_type_value,
                        "state": state_value,
                        "entity_state_id": state_value,
                        "address": "xyz",
                        "mobile": entity_mobile,
                        "gst_number": "27AAACY3846K1ZX",
                        "epr_registration_number": None,
                        "invoice": "",
                        "company_id": 11579,
                        "not_registered": False,
                        "other_type": other_type if other_type else ""
                    })
                    response = requests.post(url, headers=headers, data=payload, verify=False)
                    invoice_number = response.json().get("data", {}).get("invoice_number")

                    if not invoice_number:
                        errors.append({
                            "gst_e_invoice": gst_e_invoice,
                            "status": "Your data is not uploaded."
                        })
                    else:
                        print(f"Invoice number generated: {invoice_number}")

    # Write errors to a CSV file
    if errors:
        error_df = pd.DataFrame(errors)
        error_file_path = "error_log.csv"
        error_df.to_csv(error_file_path, index=False)
        print(f"Errors logged to {error_file_path}")
        

# def importer():
#     global roww
#     global invoi
#     invoi=[]
#     global df
#     global mail
#     global errors
#     global invoicee
#     select = easygui.enterbox("you want to proceed with?\n a) Plastic Raw Material/Packaging Procured from Non-registered Entity\n b)Plastic Raw material sale to PIBOs\n enter a or b")
#     root = tk.Tk()
#     file = fd.askopenfilename(parent=root, title='Choose a record file')
#     root.destroy()
#     if(select.lower()=='a'):
#         root = tk.Tk()
# #         file = fd.askopenfilename(parent=root, title='Choose a record file')
#         file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
#         root.destroy()
#         df1 = pd.DataFrame(list(file2), columns =['file_path'])
#         df1['file_name']=0
#         for i in range(len(df1)):
#             file2 = df1['file_path'][i].split("/")
#             file_name = file2[-1].split(".pdf")[0]
#             df1['file_name'][i]=file_name
#     df = pd.read_excel(file, keep_default_na=False, converters={'pdf_filename':str,'Bank account no':str,'Quantity (TPA)':float})

# #     now = datetime.datetime.now()
# #     val = (str(mail), "producer",str(select),str(len(df)),str(now.strftime("%d/%m/%Y %H-%M-%S")))
# #     mycursor.execute(sql, val)
# #     mydb.commit()

#     df = df.astype(str)
#     df.columns = [x.lower() for x in df.columns]
#     df['bank account no'] = df['bank account no'].str.strip()
#     count=0
#     df = df.fillna(0)
#     df = df.replace('', 0)
#     try:
#         df.upload_status
#     except:
#         df['upload_status'] = "no" 
#     if(select.lower()=='b'):
#         df['epr invoice number'] = "na"
#         invoice=[]
#         i=-1
#         driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
#         time.sleep(2)
#         while i < len(df)-1:
# #         while(i==0):
#             driver.implicitly_wait(20)
#             i=i+1
#             print(i)
#             #Add button
#             try:
#                 time.sleep(1)
#                 click = driver.find_element(by=By.XPATH, value='//input[@autocomplete="off"][@type="text"]')
#                 custom_wait_clickable_and_click(click)
#                 add = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH,'//button[contains(text(),"Add New")]')))
#                 custom_wait_clickable_and_click(add)
#                 time.sleep(1)

#                 #registration type nn
#                 try:
#                     driver.find_element(by=By.XPATH, value='//*[@name="registration_type"]//input').send_keys(df['registration type'][i])
#                     cl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(0.5)
#                 except:
#                     errors.append('registeration error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 if(df['registration type'][i].lower()=='registered'):
#                     #Type
#                     cl = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//input[@value="entity"]')))
#                     custom_wait_clickable_and_click(cl)


#                     #financial year
#                     try:
#                         fy=14
#                         time.sleep(0.5)
#                         driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]//input').send_keys(df['financial year'][i])
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                         fy=len(driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]/div[@class="ng-select-container ng-has-value"]').text)
#     #                     time.sleep(0.5)
#                     except:
#                         errors.append('financial year error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     # #GST nn
#                     # try:
#                     #     driver.find_element(by=By.XPATH, value='/html/body/ngb-modal-window/div/div/div[2]/app-pibo-material-procurement-form-sales/form/div[1]/div[11]/div/input').send_keys(df['gst number'][i])
#                     # except:
#                     #     errors.append('GST error')
#                     #     invoicee.append(str(df['invoice number'][i]))
#                     #     pass

#                     #bank account no 
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="account_no"]').send_keys(df['bank account no'][i])
#                     except:
#                         errors.append('bank account no error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #ifsc code 
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="ifsc"]').send_keys(df['ifsc code'][i])
#                     except:
#                         errors.append('ifsc code error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     # gst paid
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="gst_paid"]').send_keys(df['gst paid'][i])
#                     except:
#                         errors.append('gst paid error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #Total Quantity (Tons)
#                     try:
#                         qty = round(float(df['quantity (tpa)'][i]), 3)
#                         driver.find_element(by=By.XPATH, value='//input[@name="quantity"]').send_keys(qty)
#                     except:
#                         errors.append('Total Quantity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #invoice number
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="gst_invoice"]').send_keys(df['invoice number'][i])
#                     except:
#                         errors.append('invoice number error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #category of plastic
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
#                         cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
# #                         time.sleep(1.5)
#                     except:
#                         errors.append('category of plastic error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #entity type
#                     try:
#                         if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
#                             driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                             #cat-1 container capacity nn
#                             driver.find_element(by=By.XPATH, value='//*[@name="cat_1_sub_cat"]//input').send_keys(df['cat-1 container capacity'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1)
#                         else:
#                             driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)

#                     except:
#                         errors.append('entity type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass
            

#                     #plastic material type
#                     try:
#                         if(df['plastic material type'][i].lower()=='others'):
#                             driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#                             time.sleep(0.5)
#                             #other plastic material type nn
#                             driver.find_element(by=By.XPATH, value='//input[@name="other_type"]').send_keys(df['other plastic material type'][i])
#                         else:
#                             driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(0.5)
#                     except:
#                         errors.append('plastic material type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass
            
#                     #Name of the Entity Unregistered
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@name="registered_entity_id"]//input').send_keys(str(df['name of entity'][i]).strip())
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #address nn
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="address"]').clear()
#                         driver.find_element(by=By.XPATH, value='//input[@name="address"]').send_keys('xyz')
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #GST nn
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="gst_no"]').clear()
#                         driver.find_element(by=By.XPATH, value='//input[@name="gst_no"]').send_keys('27AAACY3846K1ZX')
#                     except:                                    
#                         pass

#                     # time.sleep(1)
                
                
# ########################################################################################################################

#                 else:
#                     #Name of the Entity Unregistered nn
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             driver.find_element(by=By.XPATH, value='//input[@name="registered_entity_id_2"]').send_keys(df['name of entity'][i])
#                         else:
#                             pass
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #address nn
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             driver.find_element(by=By.XPATH, value='//input[@name="address"]').send_keys(df['address'][i])
#                         else:
#                             pass
#                     except:
#                         errors.append('Name of the Entity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #state nn
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             time.sleep(0.5)
#                             driver.find_element(by=By.XPATH, value='//*[@name="state_select"]//input').send_keys(df['state'][i])
#                             cl=WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(2)
#                         else:
#                             pass
#                     except:
#                         errors.append('state error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #mobile number nn 
#                     try:
#                         if(df['registration type'][i].lower()=='unregistered'):
#                             driver.find_element(by=By.XPATH, value='//input[@name="mobile_number"]').send_keys(str(df['mobile number'][i])[:10])
#                         else:
#                             pass
#                     except:
#                         errors.append('mobile number error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #financial year nn
#                     try:
#                         fy=14
#                         time.sleep(0.5)
#                         driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]//input').send_keys(df['financial year'][i])
#                         cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
#                         fy=len(driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]/div[@class="ng-select-container ng-has-value"]').text)
#     #                     time.sleep(0.5)
#                     except:
#                         errors.append('financial year error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #GST nn
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="gst_no"]').send_keys(df['gst number'][i])
#                     except:
#                         errors.append('GST error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #bank account no nn 
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="account_no"]').send_keys(df['bank account no'][i])
#                     except:
#                         errors.append('bank account no error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #ifsc code nn 
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="ifsc"]').send_keys(df['ifsc code'][i])
#                     except:
#                         errors.append('ifsc code error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #gst paid nn
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="gst_paid"]').send_keys(df['gst paid'][i])
#                     except:
#                         errors.append('gst paid error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #Total Quantity (Tons) nn
#                     try:
#                         qty = round(float(df['quantity (tpa)'][i]), 3)
#                         driver.find_element(by=By.XPATH, value='//input[@name="quantity"]').send_keys(qty)
#                         print(qty)
#                     except:
#                         errors.append('Total Quantity error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #invoice number nn
#                     try:
#                         driver.find_element(by=By.XPATH, value='//input[@name="gst_invoice"]').send_keys(df['invoice number'][i])
#                     except:
#                         errors.append('invoice number error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #category of plastic nn
#                     try:
#                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
#                         cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                         custom_wait_clickable_and_click(cl)
# #                         time.sleep(1.5)
#                     except:
#                         errors.append('category of plastic error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass

#                     #entity type nn
#                     try:
#                         if(df['entity type'][i].lower()=='brand owner' and df['category of plastic'][i].lower()=='cat i'):
#                             driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)
#                             #cat-1 container capacity nn
#                             driver.find_element(by=By.XPATH, value='//*[@name="cat_1_sub_cat"]//input').send_keys(df['cat-1 container capacity'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1)
#                         else:
#                             driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(1.5)

#                     except:
#                         errors.append('entity type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass


#                     #plastic material type nn
#                     try:
#                         if(df['plastic material type'][i].lower()=='others'):
#                             driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div')))
#                             custom_wait_clickable_and_click(cl)
#                             time.sleep(0.5)
#                             #other plastic material type nn
#                             driver.find_element(by=By.XPATH, value='//input[@name="other_type"]').send_keys(df['other plastic material type'][i])
#                         else:
#                             driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
#                             cl=WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                             custom_wait_clickable_and_click(cl)
#     #                         time.sleep(0.5)
#                     except:
#                         errors.append('plastic material type error')
#                         invoicee.append(str(df['invoice number'][i]))
#                         pass
            
# #                 break
#                 #Submit nn
#                 try:
#                     if(fy<14):
# #                         import pyperclip
#                         #genrate epr invoice number
#                         cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Invoice Number")]')))
#                         custom_wait_clickable_and_click(cl)

#                         #confirm button
#                         cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Confirm"]')))
#                         custom_wait_clickable_and_click(cl)

#                         #copy epr-e invoice number
#                         try:
#                             cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Copy to clipboard"]')))
#                             custom_wait_clickable_and_click(cl)
#                             driver.find_element(by=By.XPATH, value='//input[@id="invoiceNumberCopy"]').text
#                             inv = pyperclip.paste()
#                             df['upload_status'][i] = "yes"
#                             df['epr invoice number'][i] = inv
#                             invoi.append(inv)
#                         except:
#                             invoi.append('none')

#                         #close window
#     ##                        cl=WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/div[1]/button')))
#     ##                        custom_wait_clickable_and_click(cl)
#                         driver.refresh()


                    
#                 except:
# #                 try:
#                     errors.append('Confirm error')
#                     invoicee.append(str(df['invoice number'][i]))
# #                     roww.append(i+2)
#                     try:
#                         close = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//h4/following::button[@aria-label="Close"][1]')))
#                         custom_wait_clickable_and_click(close)
#                     except:
# ##                        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
#                         time.sleep(1)
#             except:
#                 invoi.append('none')
#                 driver.refresh()
#                 add = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Add New")]')))
#                 custom_wait_clickable_and_click(add)
#                 driver.refresh()
#                 driver.implicitly_wait(15)
# ##                driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/sales')
#                 time.sleep(3)
# ##                i=i-1





#     #----------------------------------------------------------------------------------------------------------------------    
#     #----------------------------------------------------------------------------------------------------------------------    
#     #----------------------------------------------------------------------------------------------------------------------     
#     elif(select=='a'):
#         # file2 = fd.askopenfilenames(parent=root, title='Choose a pdf files')
#         driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-operations/material')
#         time.sleep(5)
#         df['date of invoice']=df['date of invoice'].astype(str)
#         i=-1
#         while i < len(df)-1:
#             driver.implicitly_wait(15)
#             i=i+1
#             print(i)
#             #Add button nn
#             try:
#                 time.sleep(1)
#                 click = driver.find_element(by=By.XPATH, value='//input[@autocomplete="off"][@type="text"]')
#                 custom_wait_clickable_and_click(click)
#                 driver.implicitly_wait(15)
#                 add = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Add New")]')))
                                        
#                 custom_wait_clickable_and_click(add)
# ##                time.sleep(0.5)
#                 driver.find_element(by=By.XPATH, value='//*[@name="registration_type"]//input').send_keys(df['registration type'][i])
#                 r_select = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                 custom_wait_clickable_and_click(r_select)
#     #             except:
#     #                 errors.append('add button error')
#     #                 pass

#                 #entity type nn
#                 try:
#                     driver.find_element(by=By.XPATH, value='//*[@name="entity_type"]//input').send_keys(df['entity type'][i])
#                     time.sleep(0.5)
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(1.5)
#                 except:
#                     errors.append('entity type error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #Name of the Entity unregistred
#                 try:
#                     driver.find_element(by=By.XPATH, value='//input[@name="registered_entity_id_2"]').send_keys(df['name of entity'][i])
#                     #driver.find_element(by=By.XPATH, value='').click()
#                 except:
#                     errors.append('Name of the Entity error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #country nn
#                 try:
#                     time.sleep(0.5)
#                     driver.find_element(by=By.XPATH, value='//*[text()="Select Country"]/following-sibling::div/input').send_keys(df['state'][i])
#                     cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                     time.sleep(2)
#                 except:
#                     errors.append('state error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #address nn
#                 try:
#                     driver.find_element(by=By.XPATH, value='//input[@name="address"]').send_keys(df['address'][i])
#                 except:
#                     errors.append('Name of the Entity error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #mobile number nn
#                 try:
#                     driver.find_element(by=By.XPATH, value='//input[@name="mobile_number"]').send_keys(str(df['mobile number'][i])[:10])
#                 except:
#                     errors.append('mobile number error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #category of plastic nn
#                 try:
#                     driver.find_element(by=By.XPATH, value='//*[@name="plastic_category"]//input').send_keys(df['category of plastic'][i])
#                     cl=WebDriverWait(driver, 10).until(
# EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]')))
#                     custom_wait_clickable_and_click(cl)
# #                         time.sleep(1.5)
#                 except:
#                     errors.append('category of plastic error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #financial year nn
#                 try:
#                     fy=14
#                     time.sleep(0.5)
                    
#                     # Click on the financial year dropdown to open it
#                     dropdown = driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]//input')
#                     dropdown.click()
                    
#                     # Send the financial year value
#                     dropdown.send_keys(df['financial year'][i])
                    
#                     # Wait until the dropdown options are clickable and then click on the first matching option
#                     cl = WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div[1]'))
#                     )
#                     cl.click()
                    
#                     # Validate that the financial year has been selected
#                     fy = len(driver.find_element(by=By.XPATH, value='//*[@name="financial_year"]/div[@class="ng-select-container ng-has-value"]').text)
                    
#                     # Additional sleep to ensure the selection is processed (if needed)
#                     time.sleep(0.5)
                    
#                     # Exception handling
#                 except Exception as e:
#                     errors.append('financial year error: ' + str(e))
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass


#                 #DATE nn
#                 try:
#                     a = str(df['date of invoice'][i])[:8]
#                     d = a[:4]+'/'+a[4:6]+'/'+a[6:]
#                     datetime0 = datetime.datetime.strptime(d, '%Y/%m/%d')
#                     datetime1 = datetime0.date()
#                     datetime2 = datetime.date.strftime(datetime1, "%d-%m-%Y")
#                     driver.find_element(by=By.XPATH, value='//input[@name="year"]').send_keys(datetime2)
#                 except:
#                     errors.append('GST error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #Total Plastic Quantity nn
#                 try:
#                     driver.find_element(by=By.XPATH, value='//input[@name="quantity"]').send_keys(df['quantity (tpa)'][i])
#                 except:
#                     errors.append('GST error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

# #                 #GST nn
# #                 try:
# #                     driver.find_element(by=By.XPATH, value='//input[@name="gst_no"]').send_keys(df['gst number'][i])
# #                 except:
# #                     errors.append('GST error')
# #                     invoicee.append(str(df['invoice number'][i]))
# #                     pass

# #                 #gst paid nn
# #                 try:
# #                     driver.find_element(by=By.XPATH, value='//input[@name="gst_paid"]').send_keys(str(df['gst paid'][i]))
# #                 except:
# #                     errors.append('gst paid error')
# #                     invoicee.append(str(df['invoice number'][i]))
# #                     pass

#                 #invoice number nn
#                 try:
#                     driver.find_element(by=By.XPATH, value='//input[@name="gst_e_invoice"]').send_keys(df['invoice number'][i])
#                 except:
#                     errors.append('invoice number error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #Upload Invoice / GST E-Invoice nn
#                 try:
#                     upload_file = driver.find_element(by=By.XPATH, value='//*[@id="invoiceID"]')
#                     pdf_file_index = df1[df1['file_name']==df['pdf_filename'][i]].index[0]
#                     pdf_file = df1['file_path'][pdf_file_index]
#                     upload_file.send_keys(pdf_file)
#                     time.sleep(1)

#                 except:
#                     errors.append('Invoice upload error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass

#                 #plastic material type nn
#                 try:
#                     if(df['plastic material type'][i].lower()=='others'):
#                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
#                         cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div')))
#                         custom_wait_clickable_and_click(cl)
# #                         time.sleep(0.5)
#                         #other plastic material type nn
#                         driver.find_element(by=By.XPATH, value='//input[@name="other_type"]').send_keys(df['other plastic material type'][i])
#                     else:
#                         driver.find_element(by=By.XPATH, value='//*[@name="plastic_type"]//input').send_keys(df['plastic material type'][i])
#                         cl=WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//ng-dropdown-panel/div/div[2]/div')))
#                         custom_wait_clickable_and_click(cl)
# #                         time.sleep(0.5)
#                 except:
#                     errors.append('plastic material type error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     pass
# #                 break
#                 #Submit
#                 try:
#                     if(fy<14):
#                         cl=WebDriverWait(driver, 3).until(
#         EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Submit")]')))
#                         custom_wait_clickable_and_click(cl)
#                         try:
#                             driver.implicitly_wait(1)
#                             close = driver.find_element(by=By.XPATH, value='//button[@id="closeMaterialProcurementPopup"]/span').click()
#                             errors.append('Submit error')
#                             invoicee.append(str(df['invoice number'][i]))
# #                             roww.append(i+2)
#                         except:
#                             df['upload_status'][i] = "yes" 
#                             pass
#                         time.sleep(0.5)
#                     else:
#                         df['upload_status'][i] = "no"
#                         raise error
#                 except:
#                     df['upload_status'][i] = "no"
#                     errors.append('Submit error')
#                     invoicee.append(str(df['invoice number'][i]))
#                     close = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="closeMaterialProcurementPopup"]/span')))
#                     custom_wait_clickable_and_click(close)
#                     time.sleep(1)
#                     pass
#             except:
#                 df['upload_status'][i] = "no"
#                 driver.refresh()
#                 add = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Add New")]')))
#                 custom_wait_clickable_and_click(add)
#                 driver.refresh()
#                 driver.implicitly_wait(15)
#                 time.sleep(2)
# ##                i=i-1
#                 pass
            
            
            


####################################################################################################################################################################################


##def get_details(driver):
##    job=driver.find_elements(by=By.XPATH, value='//table[@id="simple-table-with-pagination"]/tbody/tr/td[16]/span[@title]')
##    invoice_no=[]
##    for ii in job:
##        details = ii.get_attribute("title").strip()
##        if details:
##            invoice_no.append(details)
##    df3 = pd.DataFrame({
##                   'invoice_no': invoice_no,
##                   })
##    return df3
##
##def delete_items():
####    ssa =easygui.enterbox('What do you want to scrape? Select one option -\na) Delete Sales Entry\nb) Delete Puchase Entry)
##    root = tk.Tk()
##    file = fd.askopenfilename(parent=root, title='Choose Records deletion File')
##    root.destroy()
##    df = pd.read_excel(file, converters={'Invoice Number':str})
##    for j in range(len(df)):
##        driver.refresh()
##        click = driver.find_element(by=By.XPATH, value='//input[@autocomplete="off"][@type="text"]')
##        custom_wait_clickable_and_click(click)
##        click.send_keys(df['Invoice Number'][j])
##        driver.find_element(by=By.XPATH, value='//button[text()="Search"]').click()
##        time.sleep(3)
##        df3 = get_details(driver)
##        i = 0
##        while i < len(df3):
##            if df['Invoice Number'][j] == df3['invoice_no'][i]:
##                binn = driver.find_element(by=By.XPATH, value='//table/tbody/tr[1]/td[19]/span')
##                custom_wait_clickable_and_click(binn)
##                yes = driver.find_element(by=By.XPATH, value='//button[text()="YES"]')
##                time.sleep(1)
##                custom_wait_clickable_and_click(yes)
##                time.sleep(1)
##            i += 1
##     

def delete_items():
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)
    
    ssa =easygui.enterbox('What do you want to scrape? Select one option -\na) Delete Sales Entry\nb) Delete Puchase Entry')
    root = tk.Tk()
    file = fd.askopenfilename(parent=root, title='Choose Records deletion File')
    root.destroy()
    date_from_value = driver.find_element(By.ID, 'date_from').get_attribute('value')
    date_to_value = driver.find_element(By.ID, 'date_to').get_attribute('value')
    if ssa.lower() == 'a':
        df = pd.read_excel(file, converters={'EPR invoice No': str})
        invoice_column = 'EPR invoice No'

        for j in range(len(df)):
            search_text = df[invoice_column][j]
            url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_materials_sold"
       
            payload = json.dumps({
            "page": 1,
            "records": 50,
            "filters": {},
            "page_count": 50,
            "page_no": 1,
            "no_of_records": 50,
            "search_text": f"{search_text}",
            "from_date": f"{date_from_value}",
            "to_date": f"{date_to_value}",
            "sortData": ""
            })
            print(search_text)
            headers = {
            'Accept': 'application/json, text/plain, */*',
            'Cookie': f'login-token={login_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            }
       
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            print(response)
            rows = response.json()["data"]["tableData"]["bodyContent"]      
       
            if len(rows) > 0:
                try:
                    com_id = rows[0]["invoice"].split("/")[3]
                except:
                    com_id = 0
                sales_inc_id = rows[0]["sales_inc_id"]
                invoice = rows[0]["invoice_no"]
                registration_type = rows[0]["registration_type"]
                if registration_type == "Registered":
                    registered = True
                else:
                    registered = False
                if str(search_text) == str(invoice):
                    url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/delete_sales_reciept"
                    payload = json.dumps({
                    "company_id": com_id,
                    "registered": registered,
                    "sales_inc_id": sales_inc_id
                    })
                    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
                    status = response.json()["status"]
                    print(status)
    else:
        df = pd.read_excel(file, converters={'Invoice Number': str})
        invoice_column = 'Invoice Number'
        for j in range(len(df)):
            search_text = df[invoice_column][j]
            url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_material_procurement_details"
        
            payload = json.dumps({
            "page": 1,
            "records": 50,
            "filters": {},
            "page_count": 50,
            "page_no": 1,
            "no_of_records": 50,
            "search_text": f"{search_text}",
            "from_date": f"{date_from_value}",
            "to_date": f"{date_to_value}",
            "sortData": ""
            })
            headers = {
            'Accept': 'application/json, text/plain, */*',
            'Cookie': f'login-token={login_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            }
        
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            print(response)
            rows = response.json()["data"]["tableData"]["bodyContent"]      
        
            for row in rows:
                try:
                    com_id = row["invoice"].split("/")[3]
                except:
                    com_id = 0
                mat_proc_id = row["mt_proc_id"]
                invoice = row["gst_e_invoice"]
                if str(search_text) == str(invoice):
                    url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/delete_material_reciept"
                    payload = json.dumps({
                    "gst_e_invoice": str(invoice),
                    "company_id": com_id,
                    "registered": False,
                    "mat_proc_id": mat_proc_id
                    })
                    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
                    status = response.json()["status"]
                    print(status)


####################################################################################################################################################################################

def scrape():
    cookies_data = driver.execute_cdp_cmd("Network.getAllCookies", {})
    for cookie in cookies_data["cookies"]:
        if cookie["name"] == "login-token":
            login_token = cookie["value"]
            break
    print(login_token)

    # Prompt user for input
    ssa = easygui.enterbox('What do you want to scrape? Select one option -\na) Sales Data Entry\nb) Purchase Data Entry\nc) Credit Transactions')

    # Sales Data Entry
    if ssa.lower() == 'a':
        date_from_value = driver.find_element(By.ID, 'date_from').get_attribute('value')
        date_to_value = driver.find_element(By.ID, 'date_to').get_attribute('value')
        
        # Initialize lists for Data Entry scraping
        a11, a12, a13, a14, a15, a16, a17, a18, a19 = [], [], [], [], [], [], [], [], []
        a111, a122, a133, a144, a155, a166, a177, a188 = [], [], [], [], [], [], [], []

        def scrape_dashboard_data():
            url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_materials_sold"
            payload = json.dumps({
                "page": 1,
                "records": 100000,
                "filters": {},
                "page_count": 50,
                "page_no": 1,
                "no_of_records": 100000,
                "search_text": "",
                "from_date": f"{date_from_value}",
                "to_date": f"{date_to_value}",
                "sortData": ""
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'login-token={login_token}',
                'Origin': 'https://eprplastic.cpcb.gov.in',
                'Permissions-Policy': 'self',
                'User-Agent': 'Mozilla/5.0'
            }
            try:
                response = requests.request("POST",url, headers=headers, data=payload, files=None, verify=False)
            except:
                time.sleep(20)
                response = requests.request("POST",url, headers=headers, data=payload, files=None, verify=False)
            rows = response.json()["data"]["tableData"]["bodyContent"]
            
            for row in rows:
                # Extract data from API response, handling missing fields
                a11.append(row.get("registration_type", "N/A"))
                a12.append(row.get("entity_type", "N/A"))
                a13.append(row.get("entity_name", "N/A"))
                a14.append(row.get("entity_state", "N/A"))
                a15.append(row.get("entity_address", "N/A"))
                a16.append(row.get("entity_mobile", "N/A"))
                a17.append(row.get("plastic_type", "N/A"))
                a18.append(row.get("plastic_category", "N/A"))
                a19.append(row.get("year", "N/A"))
                a111.append(row.get("last_updated_at", "N/A"))
                a122.append(row.get("quantity", "N/A"))
                a133.append(row.get("recycled", "N/A"))
                a144.append(row.get("gst", "N/A"))
                a155.append(row.get("gst_paid", "N/A"))
                a166.append(row.get("invoice_no", "N/A"))
                a177.append(row.get("gst_e_invoice", "N/A"))
                a188.append(row.get("status", "N/A"))

        scrape_dashboard_data()

        now = datetime.datetime.now()
        df = pd.DataFrame({
            'Registration Type': a11,
            'Entity Type': a12,
            'Name of the Entity': a13,
            'State': a14,
            'Address': a15,
            'Mobile Number': a16,
            'Plastic Material Type': a17,
            'Category of Plastic': a18,
            'Financial Year': a19,
            'Date': a111,
            'Total Plastic Qty (Tons)': a122,
            'Recycled Plastic %': a133,
            'GST': a144,
            'GST Paid': a155,
            'EPR invoice No': a166,
            'GST E-Invoice No': a177,
            'Upload Status': a188
        })

        df.to_excel('Sales_Scrapped_Data_' + now.strftime("%d%m%Y_%H%M%S") + '.xlsx')
        print("Your file is generated by name - " + 'Scrapped_Data_' + now.strftime("%d%m%Y_%H%M%S") + '.xlsx')

    # Purchase Data Entry
    elif ssa.lower() == 'b':
        date_from_value = driver.find_element(By.ID, 'date_from').get_attribute('value')
        date_to_value = driver.find_element(By.ID, 'date_to').get_attribute('value')
        
        a11, a12, a13, a14, a15, a16, a17, a18, a19 = [], [], [], [], [], [], [], [], []
        a111, a122, a133, a144, a155, a166, a177 = [], [], [], [], [], [], []
        
        def scrape_material_data():
            url = "https://eprplastic.cpcb.gov.in/epr/api/v1.0/pibo/list_material_procurement_details"
            payload = json.dumps({
                "page": 1,
                "records": 100000,
                "filters": {},
                "page_count": 50,
                "page_no": 1,
                "no_of_records": 100000,
                "search_text": "",
                "from_date": f"{date_from_value}",
                "to_date": f"{date_to_value}",
                "sortData": ""
            })
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'login-token={login_token}',
                'Origin': 'https://eprplastic.cpcb.gov.in',
                'Permissions-Policy': 'self',
                'User-Agent': 'Mozilla/5.0'
            }
            try:
                response = requests.request("POST",url, headers=headers, data=payload, files=None, verify=False)
            except:
                time.sleep(20)
                response = requests.request("POST",url, headers=headers, data=payload, files=None, verify=False)
            # response = requests.post(url, headers=headers, data=payload, verify=False)
            rows = response.json()["data"]["tableData"]["bodyContent"]
            
            for row in rows:
                a11.append(row.get("registration_type", "N/A"))
                a12.append(row.get("entity_type", "N/A"))
                a13.append(row.get("entity_name", "N/A"))
                a14.append(row.get("entity_state", "N/A"))
                a15.append(row.get("entity_address", "N/A"))
                a16.append(row.get("entity_mobile", "N/A"))
                a17.append(row.get("plastic_type", "N/A"))
                a18.append(row.get("plastic_category", "N/A"))
                a19.append(row.get("year", "N/A"))
                a111.append(row.get("last_updated_at", "N/A"))
                a122.append(row.get("quantity", "N/A"))
                a133.append(row.get("recycled", "N/A"))
                a144.append(row.get("gst", "N/A"))
                a155.append(row.get("gst_paid", "N/A"))
                a166.append(row.get("invoice_no", "N/A"))
                a177.append(row.get("gst_e_invoice", "N/A"))

        scrape_material_data()
        
        now = datetime.datetime.now()
        df = pd.DataFrame({
            'Registration Type': a11,
            'Entity Type': a12,
            'Name of the Entity': a13,
            'State': a14,
            'Address': a15,
            'Mobile Number': a16,
            'Plastic Material Type': a17,
            'Category of Plastic': a18,
            'Financial Year': a19,
            'Date': a111,
            'Total Plastic Qty (Tons)': a122,
            'Recycled Plastic %': a133,
            'GST': a144,
            'GST Paid': a155,
            'EPR invoice No': a166,
            'GST E-Invoice No': a177,
        })

        df.to_excel('Material_Procurement_Scrapped_Data_' + now.strftime("%d%m%Y_%H%M%S") + '.xlsx')
        print("Your file is generated by name - " + 'Scrapped_Data_' + now.strftime("%d%m%Y_%H%M%S") + '.xlsx')

    # Credit Transactions
    elif ssa.lower() == 'c':
        driver.get('https://eprplastic.cpcb.gov.in/#/epr/pibo-wallet')
        time.sleep(5)
        driver.implicitly_wait(15)
        
        # Initialize lists for Credit Transactions scraping
        a2, b, c, d, e, f, g, h, i2, j, k, l, m, n, o, p = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

        def scrape_wallet_data():
            url = "https://eprplastic.cpcb.gov.in/epr/m3/api/v1.0/pwp/list_credit_transactions"
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'login-token={login_token}',
                'User-Agent': 'Mozilla/5.0'
            }

            payload = json.dumps({})
            try:
                response = requests.request("POST",url, headers=headers, data=payload, files=None, verify=False)
            except:
                time.sleep(20)
                response = requests.request("POST",url, headers=headers, data=payload, files=None, verify=False)
            # response = requests.post(url, headers=headers, data=payload, verify=False)
            details = response.json()["data"]["tableData"]["bodyContent"]

            for index, d_data in enumerate(details):
                index += 1
                com_id = d_data["id"]
                date = d_data.get("date", "")
                credit = d_data.get("transferTo", "")

                # Fetch additional certificate details
                url = "https://eprplastic.cpcb.gov.in/epr/m3/api/v1.0/pwp/list_transfered_certificates"
                payload = json.dumps({"id": com_id})
                try:
                    response = requests.request("POST",url, headers=headers, data=payload, files=None, verify=False)
                except:
                    time.sleep(20)
                    response = requests.request("POST",url, headers=headers, data=payload, files=None, verify=False)
                rows = response.json()["data"]["tableData"]["bodyContent"]

                for row in rows:
                    a2.append(index)
                    b.append(date)
                    c.append(credit)
                    d.append(row.get("cert_id", "N/A"))
                    e.append(row.get("value", "N/A"))
                    f.append(row.get("owner", "N/A"))
                    g.append(row.get("category", "N/A"))
                    h.append(row.get("processing_type", "N/A"))
                    i2.append(row.get("transaction_id", "N/A"))
                    j.append(row.get("before_potential", "N/A"))
                    k.append(row.get("after_potential", "N/A"))
                    l.append(row.get("before_used_potential", "N/A"))
                    m.append(row.get("after_used_potential", "N/A"))
                    n.append(row.get("cumulative_potential", "N/A"))
                    o.append(row.get("generation_time", "N/A"))
                    p.append(row.get("validity", "N/A"))

        scrape_wallet_data()

        now = datetime.datetime.now()
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
            'Validity': p
        })

        df.to_excel('Wallet_Scrapper_data_' + now.strftime("%d%m%Y_%H%M%S") + '.xlsx')
        print("Your file is generated by name - " + 'Scrapped_CT_' + now.strftime("%d%m%Y_%H%M%S") + '.xlsx')
    
def Format():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
        "Registration Type": ['registered', 'unregistered'," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Entity Type": ['pwp', 'producer', 'brand owner', 'importer', 'manufacturer', 'other'," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Name of Entity": ["Name1", "Name2"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "State": ['andaman and nicobar islands', 'andhra pradesh', 'arunachal pradesh', 'assam', 'bihar', 'chandigarh', 'chhattisgarh', 'dadra and nagar haveli and daman and diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal pradesh', 'jammu and kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'pondicherry', 'punjab', 'rajasthan', 'sikkim', 'tamil nadu', 'telangana', 'tripura', 'uttar pradesh', 'uttarakhand', 'west bengal'],
        "Address": ["Address1", "Address2"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Mobile Number": ["1234567890", "0987654321"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Plastic Material Type": ['hdpe', 'pet', 'pp', 'ps', 'ldpe', 'lldpe', 'mlp', 'others', 'pla', 'pbat'," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Category of Plastic": ['cat i', 'cat ii', 'cat iii', 'cat iv'," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Financial Year": ["2023-24", "2024-25"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Date of invoice": ["yyyymmdd", "yyyymmdd"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Quantity (TPA)": ["20", "40"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Recycled Plastic %": ["50", "60"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "GST Number": ["GST123", "GST456"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "GST Paid": ["20", "40"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Invoice Number": ["INV123", "INV456"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "pdf_filename": ["file1.pdf", "file2.pdf"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Other Plastic Material Type": ["OtherType1", "OtherType2"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Cat-1 Container Capacity": ['containers > 0.9l and < 4.9 l', 'containers > 4.9 l', 'containers < 0.9 l'," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Country": ["Country1", "Country2"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "Bank account no": ["ACC123", "ACC456"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
        "IFSC code": ["IFSC123", "IFSC456"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
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
##        "Date of invoice": ["2023-01-01", "2023-06-01"],
        "Quantity (TPA)": [10, 20],
        "Recycled Plastic %": [50, 60],
        "GST Number": ["GST123", "GST456"],
        "GST Paid": [1000, 2000],
        "Invoice Number": ["INV123", "INV456"],
        "pdf_filename": ["file1.pdf", "file2.pdf"],
        "Other Plastic Material Type": ["OtherType1", "OtherType2"],
        "Cat-1 Container Capacity": [100, 200],
##        "Country": ["Country1", "Country2"],
##        "Bank account no": ["ACC123", "ACC456"],
##        "IFSC code": ["IFSC123", "IFSC456"],
        "epr invoice number":["EInv1","EINV2"]
    }

    df = pd.DataFrame(data)
    excel_filename = 'Info_Format.xlsx'
    df.to_excel(excel_filename, index=False)
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")


def Format3():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
##        "GST Paid": [1000, 2000],
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

def Format4():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
        "invoice_pdf": ["INV123", "INV456"],
        "statement_pdf": ["STAT123", "STAT456"],
    }

    df = pd.DataFrame(data)
    excel_filename = 'Merge_Format.xlsx'
    df.to_excel(excel_filename, index=False)
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")

def Format5():
    # Dummy data to create DataFrame. Replace this with your actual data fetching logic
    data = {
##        "GST Paid": [1000, 2000],
##        "Invoice Number": ["INV123", "INV456"],
##        "pdf_filename": ["file1.pdf", "file2.pdf"],
##        "Other Plastic Material Type": ["OtherType1", "OtherType2"],
##        "Cat-1 Container Capacity": [100, 200],
##        "Country": ["Country1", "Country2"],
##        "Bank account no": ["ACC123", "ACC456"],
##        "IFSC code": ["IFSC123", "IFSC456"],
        "epr invoice no":["EInv1","EINV2"]
    }

    df = pd.DataFrame(data)
    excel_filename = 'Delete_Format.xlsx'
    df.to_excel(excel_filename, index=False)
    messagebox.showinfo("Success", f"Excel file '{excel_filename}' has been created successfully.")

def take_screenshot():
    total_height = driver.execute_script("return document.body.scrollHeight")
    window_height = driver.execute_script("return window.innerHeight")

    num_sections = (total_height + window_height - 1) // window_height
    screenshots = []

    for section in range(num_sections):
        scroll_position = section * window_height
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(2)  # Wait for the page to load before taking screenshot
        
        screenshot_path = f"screenshot_{section}.png"
        driver.save_screenshot(screenshot_path)
        screenshots.append(screenshot_path)

    images = [Image.open(s) for s in screenshots]

    last_section_height = (total_height % window_height) - 50 if total_height % window_height != 0 else window_height
    print(total_height, last_section_height, window_height, images[-1].width)
    
    if last_section_height < window_height:
        images[-1] = images[-1].crop((0, window_height - last_section_height, images[-1].width, window_height))

    total_combined_height = sum(img.height for img in images)
    combined_image = Image.new('RGB', (images[0].width, total_combined_height))

    current_height = 0
    for img in images:
        combined_image.paste(img, (0, current_height))
        current_height += img.height

    final_path = "screenshot.png"
    combined_image.save(final_path)
    
    # Cleanup temporary screenshots
    for s in screenshots:
        if os.path.exists(s):
            os.remove(s)
    
    print("Screenshot saved successfully!")

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
root.title("EPR SYNC EDGE")
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
Excel_menu.add_command(label="Delete Format Purchase", command=Format3)
Excel_menu.add_command(label="Merge Format", command=Format4)
Excel_menu.add_command(label="Delete Format Sales", command=Format5)


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
btn_screenshot = Button(root, text='Take Screenshot', command=take_screenshot, bg='#0A0D15', fg='#FFFFFF', font=('Verdana', 12), width=btn_width, height=btn_height, wraplength=120)
btn_screenshot.place(x=100, y=445)

copyright_label = Label(root, text="© AA Garg & Co. All Rights Reserved.", 
                        bg="#FFFFFF", fg="black", font=("Verdana", 8, "italic"))
copyright_label.place(x=250, y=480)
##copyright_label.pack(side="top", pady=5)

root.mainloop()
