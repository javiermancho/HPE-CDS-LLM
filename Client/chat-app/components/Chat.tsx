"use client";

import React, { useState } from 'react';
import axios from 'axios';
import ErrorMessage from './ErrorMessage'; // Importa el componente ErrorMessage
import FetchButton from './FetchButton';

interface Message {
  text: string;
  from: 'user' | 'api';
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [dateStart, setDateStart] = useState<string>('');
  const [dateEnd, setDateEnd] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const apiUrl = 'http://localhost:8080/llama';

  const handleSend = async () => {
    if (input.trim() === '') return;

    setLoading(true);
    setError(null);

    // Formar el objeto JSON con los datos
    const requestData = {
      'message': input,
      'dateStart': dateStart,
      'dateEnd': dateEnd,
    };

    try {
      console.log('Sending data:', requestData);
      // Envía la solicitud POST a la API
      const response = await axios.post(apiUrl, requestData, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 1500000,
      });

      const reply = response.data as string;

      const newMessage: Message = {
        text: reply,
        from: 'api',
      };

      // Actualiza el estado con el nuevo mensaje
      setMessages([...messages, { text: input, from: 'user' }, newMessage]);
      setInput('');
      setDateStart(''); // Limpiar las fechas después de enviar
      setDateEnd('');
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
    <div>
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.from}`}>
              {msg.text}
            </div>
          ))}
        </div>
        <div className="date-input-container">
          <div className="date-input-wrapper">
            <label className="date-label">Fecha inicio</label>
            <input
              type="date"
              className="date-input"
              value={dateStart}
              onChange={(e) => setDateStart(e.target.value)}
            />
          </div>
          <div className="date-input-wrapper">
            <label className="date-label">Fecha fin</label>
            <input
              type="date"
              className="date-input"
              value={dateEnd}
              onChange={(e) => setDateEnd(e.target.value)}
            />
          </div>
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
            {loading ? 'Enviando...' : 'Enviar'}
          </button>
        </div>
        
        {/* Utiliza el componente ErrorMessage para mostrar el error */}
        {error && <ErrorMessage error={error} />}
      </div>
      <FetchButton url="http://localhost:5002/update-pdf" />
    </div>
  );
};

export default Chat;
