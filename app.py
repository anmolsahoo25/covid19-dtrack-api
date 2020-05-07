import os
import sys
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from b2blaze import B2
import tempfile

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
b2 = B2()
bucket = b2.buckets.get('vinod-project1')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            tmpdir = tempfile.TemporaryDirectory()
            tmpfile = os.path.join(tmpdir.name,'tmpfile')
            file.save(tmpfile)
            bucket.files.upload(contents=open(tmpfile, 'rb'), file_name = filename)
            return '''
                <!doctype html>
                    <h1> Done! </h1>
                </html>
            '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
