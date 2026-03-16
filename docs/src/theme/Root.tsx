import React, { useEffect, useState } from 'react';
import MatrixBackground from '@site/src/components/MatrixBackground';
import Head from '@docusaurus/Head';

export default function Root({children}: {children: React.ReactNode}) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div style={{ backgroundColor: 'transparent' }}>
      <Head>
        <title>QORE | Protocol</title>
      </Head>
      {mounted && <MatrixBackground />}
      <div style={{ position: 'relative', zIndex: 1, backgroundColor: 'transparent' }}>
        {children}
      </div>
    </div>
  );
}
