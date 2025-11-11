'''import os
from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask App and OpenAI API Key
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- AI Analysis Function ---
def get_ai_analysis(contract_text: str) -> dict:
    """Sends contract text to OpenAI for analysis."""
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
        
        return {"opportunities_found": len(details_list), "details": details_list}

    except Exception as e:
        print(f"[OpenAI API Error]: {e}")
        # Return a structured error that the frontend can display
        return {"opportunities_found": 1, "details": [f"An error occurred while contacting the AI: {e}"]}

# --- Flask Routes ---

@app.route('/')
def index():
    """Serves the main dashboard page."""
    # This requires your HTML file to be in a folder named 'templates'
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_api():
    """API endpoint to receive text and return AI analysis."""
    data = request.get_json()
    
    # Validate that the request contains the 'content' of the contract
    if not data or 'content' not in 
        return jsonify({"error": "Invalid request: No content provided"}), 400
    
    contract_content = data['content']
    
    try:
        # Get analysis from the AI function
        results = get_ai_analysis(contract_content)
        return jsonify(results)
    except Exception as e:
        print(f"[API /analyze ERROR]: {e}")
        return jsonify({"error": "An error occurred during AI analysis."}), 500

if __name__ == '__main__':
    # Use port 10000 as specified, accessible on the local network
    app.run(host='0.0.0.0', port=10000, debug=True)'''
