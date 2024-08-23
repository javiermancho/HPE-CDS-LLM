import React, { useState, useEffect } from 'react';

interface ErrorMessageProps {
  error: string | null; // El mensaje de error puede ser una cadena o null
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ error }) => {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    if (error) {
      setVisible(true); // Mostrar el error cuando `error` cambie
      const timer = setTimeout(() => {
        setVisible(false); // Ocultar el error después de 10 segundos
      }, 2000);

      return () => clearTimeout(timer); // Limpiar el temporizador si el componente se desmonta o `error` cambia
    }
  }, [error]);

  return (
    visible && error ? (
      <div className={`error-message ${!visible ? 'hidden' : ''}`}>
        {error}
      </div>
    ) : null
  );
}

export default ErrorMessage;
