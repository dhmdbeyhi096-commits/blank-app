import requests
import json
from config import config
import logging

logger = logging.getLogger(__name__)

class AIHandler:
    """Handle communication with Ollama AI"""
    
    def __init__(self):
        self.ollama_host = config.OLLAMA_HOST
        self.model = config.OLLAMA_MODEL
        self.chat_history = []
    
    def check_connection(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f'{self.ollama_host}/api/tags', timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False
    
    def get_response(self, user_message):
        """Get AI response from Ollama"""
        try:
            # Add user message to history
            self.chat_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Prepare context from chat history
            context = self._prepare_context()
            
            # Make request to Ollama
            url = f'{self.ollama_host}/api/generate'
            
            payload = {
                'model': self.model,
                'prompt': context + user_message,
                'stream': False
            }
            
            response = requests.post(url, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('response', 'عذراً، لم أستطع الرد')
                
                # Add AI response to history
                self.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response
                })
                
                return {
                    'success': True,
                    'message': ai_response,
                    'model': self.model
                }
            else:
                return {
                    'success': False,
                    'error': 'فشل الحصول على الرد من Ollama'
                }
        
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'انتهت مهلة الانتظار - الرد يأخذ وقتاً طويلاً'
            }
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return {
                'success': False,
                'error': f'خطأ: {str(e)}'
            }
    
    def _prepare_context(self):
        """Prepare context from chat history"""
        context = ""
        for msg in self.chat_history[-10:]:  # Keep last 10 messages
            role = "المستخدم" if msg['role'] == 'user' else "المساعد"
            context += f"{role}: {msg['content']}\n"
        return context
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        return {'success': True, 'message': 'تم مسح السجل'}
    
    def get_models(self):
        """Get available models from Ollama"""
        try:
            response = requests.get(f'{self.ollama_host}/api/tags', timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                return {
                    'success': True,
                    'models': [m.get('name') for m in models]
                }
            else:
                return {
                    'success': False,
                    'error': 'لم يتمكن من الحصول على قائمة النماذج'
                }
        except Exception as e:
            logger.error(f"Error getting models: {e}")
            return {
                'success': False,
                'error': f'خطأ: {str(e)}'
            }
