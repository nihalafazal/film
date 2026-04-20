import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Create a chatbot model instance
# Switched to gemini-flash-lite-latest to provide a fresh quota bucket
model = genai.GenerativeModel('gemini-flash-lite-latest',
    system_instruction="You are an expert film critic and movie enthusiast bot. "
                       "You help users discover movies, discuss film theory, and provide recommendations. "
                       "Keep your answers concise and engaging, with a cinematic tone."
)

chats = {}

@app.route('/')
def home():
    """Render the main landing page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
        
    try:
        # Initialize chat session if it doesn't exist
        if session_id not in chats:
            chats[session_id] = model.start_chat()
            
        chat_session = chats[session_id]
        
        # Send message to model
        response = chat_session.send_message(user_message)
        
        return jsonify({
            "response": response.text,
            "status": "success"
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in chat: {e}", flush=True)
        return jsonify({
            "error": f"Error: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
