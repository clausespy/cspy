import os
import re
from flask import Flask, request, jsonify, render_template

# --- 1. Basic App Setup ---
app = Flask(__name__)

# Define the path for uploaded files.
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# --- 2. Filename Sanitization Function ---
def sanitize_filename(filename):
  """
  Takes a filename and returns a web-safe version of it.
  """
  filename = re.sub(r'\s+', '_', filename)
  safe_filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
  return safe_filename


# --- 3. Frontend Display Route ---
# This serves your index.html file from the 'templates' folder.
@app.route('/')
def index():
    return render_template('index.html')


# --- 4. File Upload Route (for potential future use, not used by current UI) ---
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        original_filename = file.filename
        safe_filename = sanitize_filename(original_filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(save_path)
        
        return jsonify({
            "message": "File uploaded successfully.",
            "saved_as_filename": safe_filename
        }), 200

    return jsonify({"error": "An unknown error occurred"}), 500


# ==============================================================================
# --- STEP 5: AI INTEGRATION SECTION ---
# ==============================================================================

def get_ai_analysis(contract_text: str) -> dict:
    """
    ############################################################################
    ###   THIS IS THE FUNCTION YOU NEED TO EDIT.                             ###
    ###   Replace the content of this function with your actual AI logic.    ###
    ############################################################################
    
    This function takes the contract text as input and must return a dictionary
    with the keys "opportunities_found" and "details".
    """
    
    # --- YOUR AI LOGIC GOES HERE ---
    
    # Example: You might be calling the OpenAI API, a local model, or other service.
    #
    # import openai
    # openai.api_key = 'YOUR_API_KEY'
    #
    # prompt = f"Analyze the following contract and identify key opportunities or risks. Return the answer as a numbered list:\n\n{contract_text}"
    #
    # response = openai.Completion.create(
    #   engine="text-davinci-003",
    #   prompt=prompt,
    #   max_tokens=200
    # )
    #
    # ai_response_text = response.choices[0].text
    # details_list = [item.strip() for item in ai_response_text.split('\n') if item.strip()]
    
    
    # For now, here is a simple placeholder that demonstrates the required output format.
    # It counts the words in the contract to show it's processing the input.
    print(f"--- Running Real AI Analysis on contract text (length: {len(contract_text)}) ---")
    word_count = len(contract_text.split())
    
    # Your code MUST return a dictionary in this format for the frontend to work.
    analysis_results = {
        "opportunities_found": 2, # Replace with the actual number you find
        "details": [
            f"The contract contains approximately {word_count} words.", # Replace with details from your AI
            "This is a second placeholder detail from the AI model."
        ]
    }
    
    return analysis_results
    # --- END OF YOUR AI LOGIC ---


# --- 5b. API Endpoint for Analysis ---
# This endpoint receives the contract text from the frontend, calls your AI function,
# and returns the results. You should not need to edit this.
@app.route('/api/analyze', methods=['POST'])
def analyze_contract():
    data = request.get_json()
    if not data or 'content' not in 
        return jsonify({"error": "Invalid request: No content provided"}), 400

    contract_content = data['content']

    try:
        # Call the function containing your AI logic
        results = get_ai_analysis(contract_content)
        return jsonify(results)

    except Exception as e:
        # This will catch any errors that happen during your AI processing
        print(f"[AI ANALYSIS ERROR]: {e}")
        return jsonify({"error": "An error occurred during AI analysis."}), 500


# --- Main execution block (for local testing and Render deployment) ---
if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible outside the container.
    # port=10000 matches Render's default.
    # debug=False is recommended for production, but True is fine for testing.
    app.run(host='0.0.0.0', port=10000, debug=True)

