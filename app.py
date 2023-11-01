from flask import Flask, request, redirect, url_for, render_template_string
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # specify your upload folder

@app.route('/')
def home():
    return "Hello, Loadify!"

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'pdf', 'docx', 'ppt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload'))
    return render_template_string(open("templates/upload.html").read())

if __name__ == '__main__':
    app.run(debug=True)