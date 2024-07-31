"use client";

import React, { useState } from 'react';
import axios from 'axios';

interface Message {
  text: string;
  from: 'user' | 'api';
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const apiUrl = 'http://localhost:8080/llama'; 

  const handleSend = async () => {
    if (input.trim() === '') return;

    setLoading(true);
    setError(null);

    try {
      // Envía la solicitud POST a la API
      const response = await axios.post(apiUrl, input, {
        headers: {
          'Content-Type': 'text/plain',
        },
        timeout: 60000,
      });

      const reply = response.data as string;

      const newMessage: Message = {
        text: reply,
        from: 'api',
      };

      // Actualiza el estado con el nuevo mensaje
      setMessages([...messages, { text: input, from: 'user' }, newMessage]);
      setInput('');
    } catch (error: any) {
      if (error.response) {
        // Error con respuesta del servidor
        setError(`Error ${error.response.status}: ${error.response.data}`);
      } else if (error.request) {
        // Error en la solicitud (no se recibió respuesta)
        setError('No se recibió respuesta del servidor.');
      } else {
        // Otro error
        setError('Error desconocido.');
      }
      console.error('Error enviando el mensaje:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.from}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default Chat;
