
import os
import re
from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def sanitize_filename(filename):
    filename = re.sub(r'\s+', '_', filename)
    safe_filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    return safe_filename

@app.route('/')
def index():
    return render_template('index.html')

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
        return jsonify({"message": "File uploaded successfully.", "saved_as_filename": safe_filename}), 200
    return jsonify({"error": "An unknown error occurred"}), 500

def get_ai_analysis(contract_text: str) -> dict:
    print("--- Contacting OpenAI API for analysis... ---")
    prompt = f"""
    Analyze the following legal contract text. Identify key risks, unfavorable clauses, or opportunities for improvement.
    Return your findings as a numbered list. If you find nothing, write "No significant issues found."

    Contract Text:
    ---
    {contract_text}
    ---
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert AI legal assistant specializing in contract analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        ai_response_text = response.choices[0].message.content.strip()
        details_list = [item.strip() for item in ai_response_text.split('\n') if item.strip()]
        if not details_list or "no significant issues" in details_list[0].lower():
            return {"opportunities_found": 0, "details": ["No significant issues were found in the contract."]}
        final_result = {"opportunities_found": len(details_list), "details": details_list}
    except Exception as e:
        print(f"[OpenAI API Error]: {e}")
        return {"opportunities_found": 1, "details": [f"An error occurred while contacting the AI: {e}"]}
    return final_result

@app.route('/api/analyze', methods=['POST'])
def analyze_contract():
    data = request.get_json()
    # THE FIX IS HERE ON THE NEXT LINE:
    if not data or 'content' not in data:
        return jsonify({"error": "Invalid request: No content provided"}), 400
    contract_content = data['content']
    try:
        results = get_ai_analysis(contract_content)
        return jsonify(results)
    except Exception as e:
        print(f"[AI ANALYSIS ERROR]: {e}")
        return jsonify({"error": "An error occurred during AI analysis."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)


