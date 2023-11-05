#views\upload.py

import os
import subprocess
from flask import request, jsonify, send_from_directory
from flask_login import login_required
from werkzeug.utils import secure_filename
from . import upload
from app import app

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'png', 'pdf', 'docx', 'ppt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload.route('/upload', methods=['POST'])
@login_required
def upload_file():
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
        # Return the filename as a JSON response
        return jsonify({'filename': filename})

@upload.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
