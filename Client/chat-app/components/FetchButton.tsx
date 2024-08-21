// Returns a Blue button that when pressed sends a /GET request to 127.0.0.1:5002/update-pdf

import React, { useState } from 'react';
import axios from 'axios';
import ErrorMessage from './ErrorMessage';

interface FetchButtonProps {
  url: string; // La URL a la que se enviará la solicitud GET
}

const FetchButton: React.FC<FetchButtonProps> = ({ url }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleClick = async () => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await axios.get(url);
      setData(response.data); // Guarda la respuesta en el estado
    } catch (error: any) {
      if (error.response) {
        setError(`Error ${error.response.status}: ${error.response.data}`);
      } else if (error.request) {
        setError('No se recibió respuesta del servidor.');
      } else {
        setError('Error desconocido.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
    <div className= "fetchButtonParent">
      <button className = "fetchButton" onClick={handleClick} disabled={loading}>
        {loading ? 'Cargando...' : 'Actualizar PDFs'}
      </button>
    </div>
    {error && <ErrorMessage error={error} />}
      {data && (
        <div className="data-container">
          <pre>{JSON.stringify(data, null, 2)}</pre> {/* Muestra la respuesta JSON */}
        </div>
      )}
      </div>
  );
};

export default FetchButton;

