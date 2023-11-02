from flask import Flask, request, send_from_directory, render_template, jsonify  # Import jsonify
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # specify your upload folder

@app.route('/')
def home():
    return render_template("upload.html")  # Serve the upload.html template on the home page

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'pdf', 'docx', 'ppt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        if filename.rsplit('.', 1)[1].lower() in ['docx', 'ppt']:
            pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
            subprocess.run(['unoconv', '-f', 'pdf', '-o', pdf_path, file_path])
            filename = pdf_filename  # Update filename to the PDF version
        return jsonify({'filename': filename})  # Return the filename as a JSON response

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
