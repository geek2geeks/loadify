# This file is located at /views/upload_views.py

import os
import subprocess
from flask import request, jsonify, send_from_directory
from flask_login import login_required
from werkzeug.utils import secure_filename

def init_app(upload_blueprint, app):
    # Function to check if the uploaded file has an allowed extension
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'jpg', 'png', 'pdf', 'docx', 'ppt'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # Route for file upload
    @upload_blueprint.route('/upload', methods=['POST'])
    @login_required  # User must be logged in to access this route
    def upload_file():
        # Get the file from the request
        file = request.files['file']
        # If the file exists and has an allowed extension
        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # If the file is a docx or ppt, convert it to pdf
            if filename.rsplit('.', 1)[1].lower() in ['docx', 'ppt']:
                pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'
                pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
                subprocess.run(['unoconv', '-f', 'pdf', '-o', pdf_path, file_path])
                filename = pdf_filename  # Update filename to the PDF version
            # Return the filename as a JSON response
            return jsonify({'filename': filename})

    # Route to serve uploaded files
    @upload_blueprint.route('/uploads/<filename>')
    @login_required  # User must be logged in to access this route
    def uploaded_file(filename):
        # Send the file from the upload folder
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
