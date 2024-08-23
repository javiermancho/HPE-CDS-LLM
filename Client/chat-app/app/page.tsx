// app/page.tsx
import Head from 'next/head';
import Chat from '../components/Chat';

import './globals.css';



export default function Home() {
  return (
    <div className="container">
      <Head>
        <title>Consulta al BOE</title>
        <meta name="description" content="Chat application used to consult BOE" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1 className = "title">Consulta al Boe</h1>
        <Chat />
      </main>
    </div>
  );
}
