import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
from datetime import date
# .env file se API Key load karne ke liye
load_dotenv()

app = Flask(__name__)
# CORS lagana zaroori hai taaki tumhara HTML browser isse baat kar sake
CORS(app)

# Google Gemini AI Client initialize kar rahe hain
# Ye automatically tumhare system ya .env file se GEMINI_API_KEY utha lega
client = genai.Client()

@app.route('/api/ask', methods=['POST'])
def ask_ai():
    try:
        # Frontend se aaya hua sawaal (data) nikalna
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'reply': 'Sawaal khali hai bhai!'}), 400
        
        user_prompt = data['prompt']

        # Gemini Model se jawab mangna (Sabse naya aur fast model)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
        )

        # AI ka jawab wapas frontend ko bhejna
        return jsonify({'reply': response.text})

    except Exception as e:
        print("Backend Error:", str(e))
        return jsonify({'reply': 'Sorry bhai, Python server me thoda error aa gaya hai!'}), 500

# Server ko port 3000 par chalane ke liye
if __name__ == '__main__':
    print("===============================================")
    print("🔥 Python AI Engine Port 3000 par live hai! 🔥")
    print("===============================================")
    app.run(host='0.0.0.0', port=3000, debug=True)
