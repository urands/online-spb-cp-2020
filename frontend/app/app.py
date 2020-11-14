from shared import app
from flask import  render_template, send_from_directory, request
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def files():
    mypath = app.config['UPLOAD_FOLDER']
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    return render_template('files.html', files = onlyfiles)

@app.route('/file/<int:idx>')
def file(idx):
    return render_template('file.html', idx = idx)




@app.route('/fonts/<path:path>')
def send_js(path):
    return send_from_directory('static/fonts', path)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            #return redirect(request.url)
            return {'msg': 'fail'}
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {'msg': 'fail filename'}
            #flash('No selected file')
            #return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'msg': 'done', 'url': '/files'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)