from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from script_connection import compute_results
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import default_converter

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'xlsx'}

# Create necessary folders
os.makedirs(os.path.join('./R Scripts', UPLOAD_FOLDER), exist_ok=True)

# Helper function to validate file extensions
def validateFile(filename):
    print(f"Validating file: {filename}")
    is_valid = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    print(f"File validation result for {filename}: {is_valid}")
    return is_valid

@app.route('/api/data', methods=['GET'])
def get_data():
    print("API '/api/data' was called")
    return jsonify({"message": "API Connected"})

@app.route("/api/upload", methods=['POST'])
def upload_files():
    print("Received request to upload files")

    # Check if files are included in the request
    if 'betaFile' not in request.files or 'probeFile' not in request.files:
        print("Error: Missing files in the request")
        return jsonify({"message": "No file part"}), 400

    betaFile = request.files['betaFile']
    probeFile = request.files['probeFile']

    # Log uploaded filenames
    print(f"Uploaded beta file: {betaFile.filename}")
    print(f"Uploaded probe file: {probeFile.filename}")

    # Validate file extensions
    if not (validateFile(betaFile.filename) and validateFile(probeFile.filename)):
        print(f"Error: Invalid file types - betaFile: {betaFile.filename}, probeFile: {probeFile.filename}")
        return jsonify({"message": "Invalid file type"}), 400

    try:
        # Define paths to save files
        print(f"Current working directory: {os.getcwd()}")
        beta_file_path = os.path.join('./R Scripts', UPLOAD_FOLDER, betaFile.filename).replace("\\", "/")
        probe_file_path = os.path.join('./R Scripts', UPLOAD_FOLDER, probeFile.filename).replace("\\", "/")

        # Save files
        betaFile.save(beta_file_path)
        probeFile.save(probe_file_path)

        print(f"Files saved successfully at: {beta_file_path} and {probe_file_path}")

        # Pass file paths to compute_results
        print("Calling compute_results function")
        with localconverter(default_converter):
            compute_results(probe_file_path, beta_file_path)

        print("compute_results function completed successfully")
        return jsonify({"message": "Files uploaded and processed successfully"}), 200

    except Exception as e:
        print(f"Error during file upload or processing: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/download', methods=['GET'])
def download_results():
    try:
        results_path = './R Scripts/results.zip'
        print(f"Preparing to send file: {results_path}")
        return send_file(
            results_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name='results.zip'
        )
    except Exception as e:
        print(f"Error during download: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/progress', methods=['GET'])
def get_progress():
    global progress_state
    print(f"Progress state requested: {progress_state}")
    return jsonify(progress_state)

if __name__ == '__main__':
    print("Starting Flask application")
    app.run(debug=True, threaded=True)