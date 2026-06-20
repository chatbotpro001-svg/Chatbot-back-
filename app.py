import os
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # CORS import kiya

app = Flask(__name__)
CORS(app)  # Isse kisi bhi frontend domain se request aane par error nahi aayega

# Gemini Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

@app.route('/')
def home():
    return "Kewa AI Backend is Running Successfully!"

@app.route('/ask', methods=['POST'])
def ask_bot():
    user_message = request.json.get('message', '')
    image_active = request.json.get('image_active', False)
    
    if not user_message and not image_active:
        return jsonify({'response': 'Koi input nahi mila!'}), 400

    if "YOUR_GEMINI_API_KEY" in GEMINI_API_KEY or not GEMINI_API_KEY:
        return jsonify({'response': f"Backend connect hai par Gemini API Key missing hai! Message: '{user_message}'"})

    system_instruction = "You are Kewa AI, a smart AI companion represented by a cute robot mascot. Answer beautifully, short and friendly."
    full_prompt = f"{system_instruction}\nUser: {user_message}"

    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            bot_response = data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'response': bot_response})
        else:
            return jsonify({'response': f"Gemini Error: Code {response.status_code}"}), response.status_code
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"}), 500

@app.route('/process-image', methods=['POST'])
def process_image():
    file_type = request.json.get('type', 'image')
    return jsonify({
        'status': 'success', 
        'message': f"✨ {file_type.capitalize()} successfully upload ho gayi!"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
