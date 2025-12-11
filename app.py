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

def try_generate(prompt):
    model_list = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-pro"]
    last_error = ""

    for model_name in model_list:
        try:
            model = genai.GenerativeModel(model_name=model_name, generation_config=generation_config)
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            continue
    
    return "Error en todos los modelos: " + last_error

@app.route('/')
def home():
    return "Drixz AI Proxy Online - Auto Model Switcher Active"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get('message', '')
        response_text = try_generate(user_msg)
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": "System Error: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
