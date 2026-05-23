import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import ChatWindow from './components/ChatWindow';
import InputArea from './components/InputArea';

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  const API_URL = 'http://localhost:5000/api';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: message,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setError('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: message
      });

      if (response.data.success) {
        const aiMessage = {
          id: Date.now() + 1,
          text: response.data.message,
          sender: 'ai',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        setError(response.data.error || 'حدث خطأ غير معروف');
      }
    } catch (err) {
      const errorMessage = err.response?.data?.error || 
                          'فشل الاتصال بالخادم. تأكد من تشغيل الخادم والـ Ollama.';
      setError(errorMessage);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    try {
      await axios.post(`${API_URL}/clear`);
      setMessages([]);
      setError('');
    } catch (err) {
      console.error('Error clearing chat:', err);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <div className="header">
          <div className="header-content">
            <h1>🤖 AI Gemini</h1>
            <p>تطبيق ذكاء اصطناعي محلي</p>
          </div>
          <button 
            className="clear-btn"
            onClick={handleClear}
            disabled={loading || messages.length === 0}
          >
            مسح السجل
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <ChatWindow 
          messages={messages}
          loading={loading}
          messagesEndRef={messagesEndRef}
        />

        <InputArea 
          onSendMessage={handleSendMessage}
          disabled={loading}
        />
      </div>
    </div>
  );
}

export default App;
