from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config)

CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ollama_model': config.OLLAMA_MODEL,
        'ollama_host': config.OLLAMA_HOST
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'AI Gemini App Backend',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'chat': '/api/chat',
            'models': '/api/models'
        }
    })

if __name__ == '__main__':
    print("\n🤖 Starting AI Gemini App Backend...")
    print(f"📡 Ollama Host: {config.OLLAMA_HOST}")
    print(f"🧠 Model: {config.OLLAMA_MODEL}")
    print("\n✅ Server running on http://localhost:5000")
    print("Press CTRL+C to stop\n")
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
