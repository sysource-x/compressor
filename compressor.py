# compressor.py
from flask import Flask, render_template, request, send_file
import zipfile
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('programa.html')

@app.route('/compress', methods=['POST'])
def compress():
    files = request.files.getlist('files')
    zip_path = os.path.join(UPLOAD_FOLDER, 'compressed.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            zipf.write(file_path, filename)
            os.remove(file_path)
    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)