from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ollama API endpoint (default is http://localhost:11434/api/generate)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Data to send to Ollama API
    data = {
        "model": "hf.co/Update0936/Law_llm:Q5_K_M",  # Or use model ID '11928495fa09'
        "prompt": user_message,
        "stream": False  # Set to False for a single response, True for streaming
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_json = response.json()

        # Extract the response text from Ollama's JSON response
        bot_response = response_json.get('response', "Error: Could not get response from model.") # Adjust key if needed
        if not bot_response:
            bot_response = response_json.get('content', "Error: Could not get response from model.") # Try 'content' as fallback

        return jsonify({"response": bot_response})

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama API: {e}")
        return jsonify({"error": "Failed to communicate with AI model."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Run Flask app on port 5000 in debug mode