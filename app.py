from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os  # System se environment variable padhne ke liye

app = Flask(__name__)
CORS(app)

# 🔒 Yeh line Render ke Environment Variables se key uthayegi
# Local par chalaoge toh system ke env se, Render par chalaoge toh Render se.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({"reply": "Kuch toh likho yaar! Message khali hai."}), 400

        # Agar Render me key set karna bhool gaye toh yeh error dikhega
        if not GEMINI_API_KEY:
            return jsonify({"reply": "Error: Backend me Gemini API Key set nahi hai!"}), 500

        # Gemini API Endpoint URL
        GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [{
                "parts": [{"text": user_message}]
            }]
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            bot_reply = response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Gemini API Error: {response.text}")
            bot_reply = "Sorry bhai, Gemini API se sahi response nahi mila."

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"reply": "Oops! Backend server me koi dikkat aa gayi."}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
