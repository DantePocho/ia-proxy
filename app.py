import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1024,
}

model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

@app.route('/')
def home():
    return "Drixz AI Proxy Active"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get('message', '')
        
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_msg)
        
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "Error: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
