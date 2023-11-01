from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os
from docx2pdf import convert
from ppt2pdf import convert_ppt_to_pdf

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
            if filename.rsplit('.', 1)[1].lower() == 'docx':
                convert(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = filename.rsplit('.', 1)[0] + '.pdf'
            elif filename.rsplit('.', 1)[1].lower() == 'ppt':
                convert_ppt_to_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = filename.rsplit('.', 1)[0] + '.pdf'
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template_string(open("templates/upload.html").read())

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)