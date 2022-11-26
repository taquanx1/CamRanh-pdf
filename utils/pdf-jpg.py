from datetime import datetime
start = datetime.now()

import argparse
import os.path
from pdf2image import convert_from_path
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
thread_count = 100

'''
python pdf-jpg.py -path test/Aladdin_EN.pdf -combine True
'''

pages = convert_from_path(
    pdf_path = pdfPath,
    dpi = dpi,
    thread_count = thread_count)

i = 1
outFile_list = []
if not os.path.exists(jpgPath):
    os.makedirs(jpgPath)
if not os.path.exists('static/pdfPreview/' + pdfName):
    os.makedirs('static/pdfPreview/' + pdfName)
for page in pages:
    outPath = jpgPath + '/%s.jpg'%str(i)
    page.save(outPath, 'JPEG')
    page.save('static/pdfPreview/' + pdfName + '/%s.jpg'%str(i), 'JPEG')
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
