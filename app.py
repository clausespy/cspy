

# app.py - The Backend Engine

from flask import Flask, request, jsonify
from flask_cors import CORS
import time

# Create the Flask application
app = Flask(__name__)
# Enable CORS to allow the frontend to communicate with the backend
CORS(app)

def analyze_contract_text(contract_text, user_query):
    """
    This is the core analysis engine. In a real application, this function
    would make calls to an AI model like GPT-4. Here, we simulate that analysis.
    """
    # Simulate AI processing time
    time.sleep(2) 

    # --- 1. Plain English Summary (Simulated AI Output) ---
    summary = "This is a 5-year contract that can be terminated by either party with 90 days' written notice for any reason. If terminated, the client is responsible for paying all fees incurred up to the date of termination."

    # --- 2. Risk & Loophole Detection (Simulated AI Output) ---
    risks = []
    if "for any reason or no reason" in contract_text:
        risks.append({
            "level": "High",
            "title": "Termination for Convenience",
            "explanation": "Either side can end this contract at any time without cause, creating uncertainty for you."
        })
    if "responsible for all fees incurred" in contract_text:
        risks.append({
            "level": "Medium",
            "title": "Liability for All Fees",
            "explanation": "You are on the hook for all fees up until the moment of cancellation, which could be a large sum."
        })

    # --- 3. Advantage Finder Search (Simulated AI Output) ---
    advantages = []
    if "terminate" in user_query.lower():
        if "ninety (90) days' written notice" in contract_text:
            advantages.append({
                "clause": "1.2",
                "finding": "You have a flexible exit strategy. The contract can be terminated for any reason with 90 days' notice."
            })

    # --- Package the results into a structured dictionary ---
    return {
        "summary": summary,
        "risks": risks,
        "advantages": advantages
    }

@app.route('/analyze', methods=['POST'])
def handle_analysis():
    """This is the API endpoint that the frontend will call."""
    if not request.json or 'contract_text' not in request.json:
        return jsonify({"error": "Missing contract text"}), 400

    contract_text = request.json['contract_text']
    user_query = request.json.get('user_query', '') # Get user query, default to empty string

    # Run the analysis engine
    analysis_results = analyze_contract_text(contract_text, user_query)

    # Return the results to the frontend as JSON
    return jsonify(analysis_results)

if __name__ == '__main__':
    # This allows you to test the app on your local machine
    app.run(debug=True, port=5000)
