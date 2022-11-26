# -*- coding: UTF-8 -*-# -*- coding: UTF-8 -*-
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_file
import os
import json
from io import BytesIO
import zipfile

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#upload
@app.route('/', methods=['GET', 'POST'])
def main():
    print('start')
    if request.method == 'POST':
        file = request.files['filename']
        save_filename = file.filename.replace(' ', '-')
        file.save(os.path.join('file/pdf', save_filename))
        status = json.dumps({"pdfPath": save_filename})
        session['messages'] = status
        return redirect(url_for('preview', messages=status))
    return render_template('upload.html')

@app.route('/preview', methods=['GET', 'POST'])
def preview():
    print('click2')
    status = session['messages']
    status = json.loads(status)

    pdfPath = 'file/pdf/' + status['pdfPath']
    print('pdfPath', pdfPath)
    jpgPath = '/'.join(pdfPath.split('/')[:-1]) + pdfPath.split('/')[-1].replace('.pdf', '')
    print('jpgPath', jpgPath)

    pdfName = pdfPath.split('/')[-1].replace('.pdf', '')
    jpgPath = 'file/jpg/' + pdfName
    combineJpgPath = '../../static/pdfPreview/' + pdfName + '/combine.jpg'
    combineJpgPath_download = 'static/pdfPreview/' + pdfName + '/combine.jpg'

    command = 'python3 utils/pdf-jpg.py -path %s -combine True' % pdfPath
    print(command)
    os.system(command)
    # python utils/pdf-jpg.py -path test/Aladdin_EN.pdf -combine True

    if request.method == 'POST':
        buttValue = request.form.get("btn")
        print(buttValue, combineJpgPath)
        if buttValue == 'downloadMerge':
            return send_file(combineJpgPath_download, as_attachment=True)
        if buttValue == 'downloadSplit':
            '''
            stream = BytesIO()
            with ZipFile(stream, 'w') as zf:
                download_filelist = []
                for filename in os.listdir(jpgPath):
                    if filename.split('.')[-1] == 'jpg' and 'combine' not in filename:
                        #print(jpgPath + '/%s'%filename)
                        download_filelist.append(jpgPath + '/%s'%filename)
                        zf.write(jpgPath + '/%s'%filename, os.path.basename(jpgPath + '/%s'%filename))
                stream.seek(0)
            '''

            # Zip file Initialization
            zipfolder = zipfile.ZipFile('%s.zip'%pdfName, 'w', compression=zipfile.ZIP_STORED)  # Compression type

            # zip all the files which are inside in the folder
            for root, dirs, files in os.walk(jpgPath):
                for filename in files:
                    if filename.split('.')[-1] == 'jpg' and 'combine' not in filename:
                        zipfolder.write(jpgPath + '/%s'%filename)
            zipfolder.close()

            return send_file('%s.zip'%pdfName,
                             mimetype='zip',
                             as_attachment=True,
                             download_name='%s.zip'%pdfName)





    return render_template('preview.html', **locals())


'''
        print('in')
        if 'input_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['input_file']
        print('in2', file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            print('in3')
            file.save(os.path.join('file/pdf', file.filename))
            PREVIEW_IMAGE_PATH = file.filename
        return redirect(url_for('preview'))
'''