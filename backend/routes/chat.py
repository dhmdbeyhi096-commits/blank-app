from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)

def create_chat_blueprint(ai_handler):
    """Create and return chat blueprint"""
    chat_bp = Blueprint('chat', __name__)
    
    @chat_bp.route('/chat', methods=['POST'])
    def chat():
        """Handle chat messages"""
        try:
            data = request.get_json()
            
            if not data or 'message' not in data:
                return jsonify({'error': 'الرسالة مفقودة'}), 400
            
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return jsonify({'error': 'الرسالة لا يمكن أن تكون فارغة'}), 400
            
            # Check Ollama connection
            if not ai_handler.check_connection():
                return jsonify({
                    'error': 'لا يمكن الاتصال بـ Ollama. تأكد من تشغيله.',
                    'instructions': 'شغل Ollama أولاً: ollama serve'
                }), 503
            
            # Get AI response
            response = ai_handler.get_response(user_message)
            
            if response.get('success'):
                return jsonify(response), 200
            else:
                return jsonify(response), 500
        
        except Exception as e:
            logger.error(f"Error in chat endpoint: {e}")
            return jsonify({'error': f'خطأ على الخادم: {str(e)}'}), 500
    
    @chat_bp.route('/clear', methods=['POST'])
    def clear():
        """Clear chat history"""
        try:
            result = ai_handler.clear_history()
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error clearing history: {e}")
            return jsonify({'error': f'خطأ: {str(e)}'}), 500
    
    @chat_bp.route('/models', methods=['GET'])
    def models():
        """Get available models"""
        try:
            result = ai_handler.get_models()
            return jsonify(result), 200 if result.get('success') else 500
        except Exception as e:
            logger.error(f"Error getting models: {e}")
            return jsonify({'error': f'خطأ: {str(e)}'}), 500
    
    return chat_bp
