from flask import Flask, request, jsonify
from flask_cors import CORS
import os 
from script_connection import compute_results

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './R Scripts/data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx'}

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "API Connected"}   
)

def validateFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/upload", methods=['POST'])
def upload_files():
    if 'betaFile' not in request.files or 'probeFile' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    betaFile = request.files['betaFile']
    probeFile = request.files['probeFile']

    if not (validateFile(betaFile.filename) and validateFile(probeFile.filename)):
        return jsonify({"message": "Invalid file type"}), 400
    
    try:
        betaFile.save(os.path.join(UPLOAD_FOLDER, betaFile.filename))
        probeFile.save(os.path.join(UPLOAD_FOLDER, probeFile.filename))

        beta_data_path = os.path.join(UPLOAD_FOLDER, betaFile.filename)
        probe_data_path = os.path.join(UPLOAD_FOLDER, probeFile.filename)

        compute_results(probe_data_path, beta_data_path)
        
        return jsonify({"message": "Files uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}, 500)

if __name__ == '__main__':
    app.run(debug=True)