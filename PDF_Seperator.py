from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("العشر_الأخير_من_تفسير_أيسر_التفاسير_للشيخ_ابو_بكر_الجزائري.pdf", "rb"))
Sowar_list = {'الملك': [112, 124],
              'النبأ': [219, 226],
              'النازعات': [226, 234],
              'عبس': [235, 241],
              'التكوير': [242, 247],
              'الانشقاق': [261, 266],
              'البروج': [266, 271],
              'الطارق': [271, 274],
              'الأعلى': [274, 278],
              'الغاشية': [278, 282],
              'الفجر': [283, 290]}
for sora in Sowar_list:
    output = PdfFileWriter()
    for page in range(Sowar_list[sora][0]-1, Sowar_list[sora][1]):
        output.addPage(inputpdf.getPage(page))
    with open(f' سورة {sora}.pdf', "wb") as outputStream:
        output.write(outputStream)
