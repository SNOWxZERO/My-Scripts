import PyPDF2
import os
totalpages=0
path = os.getcwd()
for filename in os.listdir(path):
   if filename == os.path.basename(__file__) or filename[-3:]!='pdf' :
       continue
   with open(os.path.join(path, filename), 'rb') as f:
       readpdf = PyPDF2.PdfFileReader(f)
       NumOfPages = readpdf.numPages
       print(f'{filename} : {NumOfPages}')
       totalpages += NumOfPages
print('Total Pdf Pages = ',end='')
print(totalpages)
