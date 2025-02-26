from flask import Flask, request, jsonify, session
import google.generativeai as genai
from flask_cors import CORS  # Allow frontend to communicate with backend
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests
app.secret_key = os.getenv("FLASK_SECRET_KEY", "f2c4b8d9e07b4c1a9f54d3b2a7e8c6d5")  # Required for using session

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyCr1cgsTr8KbrIzWcTv6BBF7vA1Fh0Ad7E"))
custom_model  = genai.GenerativeModel("tunedModels/aichatbot-py5ia531sfyn")  # Use a valid model
base_model = genai.GenerativeModel("gemini-pro")  # Base Gemini model

def is_out_of_scope(response):
    """
    Check if the response from the custom model is irrelevant or empty.
    You can define your own logic here based on your use case.
    """
    return not response.text.strip() or "I don't know" in response.text
@app.route("/")
def home():
    return "Chatbot API is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    # Initialize chat history
    if "history" not in session:
        session["history"] = []

    # Append user message to history
    session["history"].append({"role": "user", "parts": [{"text": user_message}]})

    try:
        # Step 1: Try generating a response with the custom-tuned model
        response = custom_model.generate_content(contents=session["history"])
        ai_response = response.text.strip()

        # Step 2: If the response is out of scope, fall back to the base model
        if is_out_of_scope(response):
            response = base_model.generate_content(contents=session["history"])
            ai_response = response.text.strip()

        # Append AI response to history
        session["history"].append({"role": "model", "parts": [{"text": ai_response}]})

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
