"use client";

import React, { useState, useEffect } from 'react';
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
  const [lastPdfDate, setLastPdfDate] = useState<string>(''); // Estado para la fecha del último PDF

  const apiUrl = 'http://localhost:8080/llama';
  const dateApiUrl = 'http://localhost:5002/last-date'; // URL del endpoint para la fecha del último PDF

  // Función para obtener la última fecha del PDF
  const fetchLastPdfDate = async () => {
    try {
      const response = await axios.get(dateApiUrl);
      const lastDateUpdate = response.data.last_date;
      // Formatear la fecha en formato 'YYYY-MM-DD'
      const formattedDate = `${lastDateUpdate.toString().slice(0, 4)}-${lastDateUpdate.toString().slice(4, 6)}-${lastDateUpdate.toString().slice(6)}`;
      setLastPdfDate(formattedDate);
    } catch (error) {
      console.error('Error al obtener la fecha del último PDF:', error);
    }
  };

  useEffect(() => {
    fetchLastPdfDate(); // Llamar a la función cuando el componente se monte
  }, []);

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
      <div className="last-pdf-date">
          <p>Último PDF subido: {lastPdfDate}</p>
        </div>
      <FetchButton url="http://127.0.0.1:5002/update-pdf" />
    </div>
  );
};

export default Chat;
