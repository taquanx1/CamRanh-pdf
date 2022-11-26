# -*- coding: UTF-8 -*-# -*- coding: UTF-8 -*-
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_file
import os
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#upload
@app.route('/', methods=['GET', 'POST'])
def main():
    print('start')
    if request.method == 'POST':
        file = request.files['filename']
        file.save(os.path.join('file/pdf', file.filename))
        status = json.dumps({"pdfPath": file.filename})
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

    command = 'python utils/pdf-jpg.py -path %s -combine True' % pdfPath
    print(command)
    os.system(command)
    # python utils/pdf-jpg.py -path test/Aladdin_EN.pdf -combine True

    if request.method == 'POST':
        buttValue = request.form.get("btn")
        print(buttValue, combineJpgPath)
        if buttValue == 'download':
            return send_file(combineJpgPath_download, as_attachment=True)
        #download
        #if new upload
        # to upload
        pass




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