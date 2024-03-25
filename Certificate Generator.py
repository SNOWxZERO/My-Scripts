import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display

names_file_male = r'F:\Muhammad\HardWork\تطوع\فاتحون\أبجديات الثقافة\النهائي.xlsx'
certificate_image_general = r'F:\Muhammad\HardWork\تطوع\فاتحون\أبجديات الثقافة\شهادة.jpg'

data = pd.read_excel(names_file_male)

for index, row in data.iterrows():
    
    
    current_name = row['الاسم']
    print(f"\rProcessing: {current_name}", end='')

    rawname = str(current_name)
    if len(rawname) > 32:
        rawname = rawname[0:32].rsplit(' ', 1)[0]

    reshaped_p = arabic_reshaper.reshape(rawname)
    name = get_display(reshaped_p)
    reshaped_p = arabic_reshaper.reshape(row['التقدير'])
    taqdeer = get_display(reshaped_p)
    im = Image.open(certificate_image_general)

    imgname = current_name + ".jpg"
    letter = current_name[0]
    if letter in ['إ', 'أ', 'آ', 'ء']:
        letter = 'ا'

    d = ImageDraw.Draw(im)
    name_color = (0, 91, 111)
    taqdeer_color = (220, 136, 12)
    font = ImageFont.truetype("C:\Windows\Fonts\Bahij TheSansArabic-ExtraBold.ttf", 80)
    _, _, w, h = d.textbbox((0, 0), name, font=font)
    d.text(((2025 - w) / 2, (1360 - h) / 2), name, font=font, fill=name_color)

    font = ImageFont.truetype("C:\Windows\Fonts\Bahij TheSansArabic-ExtraBold.ttf", 50)
    image_width, image_height = im.size
    _, _, w, h = d.textbbox((0, 0), taqdeer, font=font, align='right')
    d.text((975 - w, 853), taqdeer, font=font, fill=taqdeer_color)

    path = f"F:\Muhammad\HardWork\تطوع\فاتحون\أبجديات الثقافة\شهادات\{letter}"
    if not os.path.exists(path):
        os.makedirs(path)

    savepath = os.path.join(path, imgname)
    im.save(savepath)