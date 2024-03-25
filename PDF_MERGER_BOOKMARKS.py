from PyPDF2 import PdfFileMerger, PdfFileReader
import os

path = os.getcwd()
merger = PdfFileMerger()
totalpages = 0
for filename in os.listdir(path):
    if filename == os.path.basename(__file__) or filename[-3:] != 'pdf':
        continue
    pdffile = PdfFileReader(open(filename, 'rb'), strict=False)
    merger.append(pdffile, bookmark=filename)
    NumOfPages = pdffile.numPages
    print(f'{filename} : {NumOfPages}')
    totalpages += NumOfPages
merger.write("Merged.pdf")
print('-----------------------------')
print('Merging is DONE!')
print('----------------')
print(f'Total Pdf Pages = {totalpages}', end='')
