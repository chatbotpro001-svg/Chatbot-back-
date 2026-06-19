from flask import Flask, request, jsonify
from flask_cors import CORS
import requests  # Agar future me kisi external API ko hit karna ho

app = Flask(__name__)

# CORS enable kiya hai taaki aapka HTML bina kisi restriction ke is URL ko hit kar sake
CORS(app)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        # Frontend se aaya hua JSON data extract karein
        data = request.json
        user_message = data.get('message', '').strip()

        # Agar user ka message khali hai
        if not user_message:
            return jsonify({"reply": "Kuch toh likho yaar! Message khali hai."}), 400

        # --- YAHAN AAP APNA CUSTOM LOGIC YA EXTERNAL API CALL DAL SAKTE HAIN ---
        # Abhi ke liye ek basic bot replies logic setup hai:
        
        message_lower = user_message.lower()
        
        if "book" in message_lower or "suggest" in message_lower:
            bot_reply = "Sure! How about 'Atomic Habits' by James Clear? It's a great book on building good habits."
        elif "hello" in message_lower or "hi" in message_lower:
            bot_reply = "Hello! 👋 How can I help you today?"
        elif "thanks" in message_lower or "thank you" in message_lower:
            bot_reply = "You're welcome! 😊 Let me know if you need anything else."
        else:
            # Default response agar upar me se kuch match nahi hua
            bot_reply = f"Mene aapka message suna: '{user_message}'. Main abhi seekh raha hoon!"

        # Response ko JSON format me wapas frontend ko bhejein
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"reply": "Oops! Backend server me koi dikkat aa gayi."}), 500

if __name__ == '__main__':
    # Server ko port 5000 par run karne ke liye
    app.run(host='127.0.0.1', port=5000, debug=True)
