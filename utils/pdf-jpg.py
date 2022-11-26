from datetime import datetime
start = datetime.now()

import argparse
import os.path
from pdf2image import convert_from_path, pdfinfo_from_path
'''
Solution for [Errno 2] No such file or directory: 'pdfinfo'

For MacOS: brew install poppler
For Ubuntu: sudo apt-get install -y poppler-utils
'''

parser = argparse.ArgumentParser(description='Tile the first num-pages horizontally into a JPEG image.')
parser.add_argument("-path", type=str, default='paper.pdf', help='The pdf to convert.')
parser.add_argument("-combine", type=str, default=15, help='Determined how long to wait before quiting')
args = parser.parse_args()

#Setting
pdfPath = args.path
pdfName = pdfPath.split('/')[-1].replace('.pdf', '')
jpgPath = 'file/jpg/' + pdfName
dpi = 200
combine = args.combine
thread_count = 1

'''
python pdf-jpg.py -path test/Aladdin_EN.pdf -combine True
'''





if not os.path.exists(jpgPath):
    os.makedirs(jpgPath)
if not os.path.exists('static/pdfPreview/' + pdfName):
    os.makedirs('static/pdfPreview/' + pdfName)

i = 1
outFile_list = []
info = pdfinfo_from_path(pdfPath, userpw=None, poppler_path=None)
maxPages = info["Pages"]
for page in range(1, maxPages+1, 3) :
    cur_chunkPage = convert_from_path(pdfPath, dpi=200, first_page=page, last_page = min(page+10-1,maxPages))
    for p in cur_chunkPage:
        outPath = jpgPath + '/%s.jpg'%str(i)
        p.save(outPath, 'JPEG')
        p.save('static/pdfPreview/' + pdfName + '/%s.jpg'%str(i), 'JPEG')
        i += 1
        outFile_list.append(outPath)

if combine == 'True':
    from PIL import Image

    images = [Image.open(x) for x in outFile_list]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(heights)
    max_height = max(widths)
    new_im = Image.new('RGB', (max_height, total_width))

    y_offset = 0
    for im in images:
      new_im.paste(im, (0, y_offset))
      y_offset += im.size[1]

    new_im.save(jpgPath + '/combine.jpg')
    new_im.save('static/pdfPreview/' + pdfName + '/combine.jpg')

print(datetime.now() - start)
