from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from langChainservices import extract_text_from_pdf, extractRelevantDataWithStandardUnits
from flask_cors import CORS, cross_origin

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CORS(app)  # Enable CORS globally

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    print(request)
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        text = extract_text_from_pdf(file_path)
        extracted_data = extractRelevantDataWithStandardUnits(text)

        return jsonify({"extracted_data": extracted_data})

    return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

if __name__ == '__main__':
    app.run(debug=True)
