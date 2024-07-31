// app/page.tsx
import Head from 'next/head';
import Chat from '../components/Chat';
import './globals.css';

export default function Home() {
  return (
    <div className="container">
      <Head>
        <title>Chat App</title>
        <meta name="description" content="Chat application built with Next.js" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1>Chat App</h1>
        <Chat />
      </main>
    </div>
  );
}
