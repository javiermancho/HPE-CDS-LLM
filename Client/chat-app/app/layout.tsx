export const metadata = {
  title: 'HPE Javier Mancho',
  description: 'LLM to consult BOE',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
