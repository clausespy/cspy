import os
import re
from flask import Flask, request, jsonify, redirect, url_for, render_template

# --- 1. Basic App Setup ---
app = Flask(__name__)

# Define the path for uploaded files. 
# We'll create a folder named 'uploads' in the same directory as this script.
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# --- 2. Filename Sanitization Function ---
def sanitize_filename(filename):
  """
  Takes a filename and returns a web-safe version of it.
  - Replaces spaces with underscores.
  - Removes all characters that are not letters, numbers, dots, underscores, or hyphens.
  """
  # Replace one or more whitespace characters with a single underscore
  filename = re.sub(r'\s+', '_', filename)
  # Remove all characters that aren't alphanumeric, a dot, an underscore, or a hyphen
  safe_filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
  return safe_filename


# --- 3. Frontend Display Route ---
# This route will just display a simple HTML form to test the upload.
@app.route('/')
def index():
    # This function will look for an 'index.html' file in a 'templates' folder.
    # For now, we'll return a simple string to keep it self-contained.
    return '''
    <!doctype html>
    <title>ClauseSpy Uploader</title>
    <h1>Upload a Contract to Analyze</h1>
    <form method=post action="/upload" enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# --- 4. File Upload Route ---
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Get the original filename from the upload
        original_filename = file.filename
        
        # Create a safe, sanitized version of the filename
        safe_filename = sanitize_filename(original_filename)
        
        # Create the full path to save the file
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        
        # Save the file to the 'uploads' folder
        file.save(save_path)
        
        # For now, return a success message with the new filename.
        # In the next steps, this is where you would trigger the analysis.
        return jsonify({
            "message": "File uploaded successfully.",
            "original_filename": original_filename,
            "saved_as_filename": safe_filename,
            "file_size_bytes": os.path.getsize(save_path)
        }), 200

    return jsonify({"error": "An unknown error occurred during file upload"}), 500


# --- 5. API Endpoint for Analysis (for the next step) ---
@app.route('/api/analyze', methods=['POST'])
def analyze_contract():
    data = request.get_json()
    contract_content = data.get('content')

    if not contract_content:
        return jsonify({"error": "No content provided for analysis"}), 400

    # --- AI PROCESSING LOGIC WILL GO HERE ---
    # This is a placeholder for your AI model's logic.
    print(f"Analyzing content: {contract_content[:100]}...") # Print first 100 chars to log
    
    analysis_result = {
        "opportunities_found": 2,
        "details": [
            "Placeholder: Ambiguous payment terms detected.",
            "Placeholder: Unfavorable liability clause found."
        ]
    }
    # --- End of placeholder ---

    return jsonify(analysis_result)

# --- Main execution block (for local testing) ---
if __name__ == '__main__':
    # The host='0.0.0.0' makes it accessible on your local network
    # The port=10000 matches what Render expects.
    app.run(host='0.0.0.0', port=10000, debug=True)

