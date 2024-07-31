// pages/api/chat.ts
import type { NextApiRequest, NextApiResponse } from 'next';

type Data = {
  reply: string;
};

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  if (req.method === 'POST') {
    const { message } = req.body;

    const reply = `Respuesta a: ${message}`;
    res.status(200).json({ reply });
  } else {
    res.status(405).end(); // Método no permitido
  }
}
