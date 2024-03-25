import pandas as pd
from arabic_reshaper import reshape
import re

def convert_arabic_to_western(arabic_number_str):
    # Use regular expression to replace Arabic-Indic digits with Western digits
    arabic_number_str = re.sub(r'\D', '', arabic_number_str)
    western_number = re.sub('[٠-٩]', lambda x: str(ord(x.group()) - ord('٠')), arabic_number_str)
    return western_number

#names_file_male = r'F:\Muhammad\HardWork\تطوع\فاتحون\أبجديات الثقافة\قبل التنظيف.xlsx'
#df = pd.read_excel(names_file_male,sheet_name='مجمع للتنظيف اليدوي')
#col=df.columns

file = r'F:\Muhammad\HardWork\تطوع\فاتحون\أبجديات الثقافة\بعد التنظيف.xlsx'
df = pd.read_excel(file,sheet_name='Sheet2')



df['الهاتف'] = df['الهاتف'].astype(str)
df['الهاتف 2'] = df['الهاتف 2'].astype(str)
df['الهاتف'] = df['الهاتف'].apply(convert_arabic_to_western)
df['الهاتف 2'] = df['الهاتف 2'].apply(convert_arabic_to_western)
df['معرف التليجرام']=df['معرف التليجرام'].astype(str)
df['معرف التليجرام 2']=df['معرف التليجرام 2'].astype(str)
df[['الاسم','الاسم 2','معرف التليجرام','معرف التليجرام 2']] = df[['الاسم','الاسم 2','معرف التليجرام','معرف التليجرام 2']].apply(lambda x: x.str.strip())



df['وجود الاسم']=df['الاسم'].isin(df['الاسم 2']).astype(int)
df['وجود الاسم 2']=df['الاسم 2'].isin(df['الاسم']).astype(int)
df['وجود الهاتف']=df['الهاتف'].isin(df['الهاتف 2']).astype(int)
df['وجود الهاتف 2']=df['الهاتف 2'].isin(df['الهاتف']).astype(int)
df['وجود التليجرام']=df['معرف التليجرام'].isin(df['معرف التليجرام 2']).astype(int)
df['وجود التليجرام 2']=df['معرف التليجرام 2'].isin(df['معرف التليجرام']).astype(int)


for index, row in df.iterrows():
    if row['وجود الاسم'] == 0 and row['وجود الهاتف'] == 0 and row['وجود التليجرام'] == 0:   
        df.loc[df['الاسم'] == row['الاسم'], 'الاسم'] = 'z' + df.loc[df['الاسم'] == row['الاسم'], 'الاسم']
    if row['وجود الاسم 2'] == 0 and row['وجود الهاتف 2'] == 0 and row['وجود التليجرام 2'] == 0:
        df.loc[df['الاسم 2'] == row['الاسم 2'], 'الاسم 2'] ='z' + df.loc[df['الاسم 2'] == row['الاسم 2'], 'الاسم 2']
        
        
df=df.sort_values(by=['الاسم'])
#df = df.duplicated(subset=['الاسم'], keep='first')    
df = df[['إجمالي النتيجة','الاسم','الهاتف','معرف التليجرام','إجمالي النتيجة 2','الاسم 2','الهاتف 2','معرف التليجرام 2']]


excel_file_path = 'F:\Muhammad\HardWork\تطوع\فاتحون\أبجديات الثقافة\بعد التنظيف النهائي.xlsx'
df.to_excel(excel_file_path, index=False)

