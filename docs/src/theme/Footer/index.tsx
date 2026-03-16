import React from 'react';
import { useThemeConfig } from '@docusaurus/theme-common';

function Footer(): JSX.Element | null {
  const { footer } = useThemeConfig();
  if (!footer) {
    return null;
  }

  return (
    <footer style={{ 
      background: '#000', 
      borderTop: '1px solid #18181b', 
      padding: '80px 40px',
      color: '#fff',
      fontFamily: 'Inter, sans-serif'
    }}>
      <div className="container">
        <div className="row" style={{ marginBottom: '60px' }}>
          <div className="col col--6">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
               <div style={{ background: '#111', padding: '6px', borderRadius: '4px', border: '1px solid #27272a' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>
               </div>
               <span style={{ letterSpacing: '0.15em', fontWeight: 900, fontSize: '0.9rem', fontFamily: 'var(--qore-font-title)' }}>QORE // PROTOCOL</span>
            </div>
            <p style={{ color: '#52525b', fontSize: '0.8rem', maxWidth: '300px', lineHeight: '1.6' }}>
              Advanced Agentic Quality Engineering Orchestration for Enterprise SDLC.
            </p>
          </div>
          
          <div className="col col--2">
            <h4 style={{ fontSize: '0.7rem', color: '#71717a', letterSpacing: '0.1em', marginBottom: '20px' }}>INDEX</h4>
            <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.75rem', color: '#a1a1aa' }}>
              <li style={{ marginBottom: '8px' }}><a href="/docs/intro" style={{ color: 'inherit', textDecoration: 'none' }}>INTRODUCTION</a></li>
              <li style={{ marginBottom: '8px' }}><a href="/docs/intro" style={{ color: 'inherit', textDecoration: 'none' }}>ARCHITECTURE</a></li>
            </ul>
          </div>

          <div className="col col--2">
            <h4 style={{ fontSize: '0.7rem', color: '#71717a', letterSpacing: '0.1em', marginBottom: '20px' }}>SYSTEM</h4>
            <ul style={{ listStyle: 'none', padding: 0, fontSize: '0.75rem', color: '#a1a1aa' }}>
              <li style={{ marginBottom: '8px' }}><a href="https://github.com/vinipx/ai-qa-agents-python" style={{ color: 'inherit', textDecoration: 'none' }}>REPOSITORY</a></li>
              <li style={{ marginBottom: '8px' }}>CORE_V1.1.2</li>
            </ul>
          </div>

          <div className="col col--2">
            <h4 style={{ fontSize: '0.7rem', color: '#71717a', letterSpacing: '0.1em', marginBottom: '20px' }}>STATUS</h4>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.7rem', color: '#22c55e' }}>
               <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#22c55e', boxShadow: '0 0 10px #22c55e' }}></div>
               <span>OPERATIONAL</span>
            </div>
          </div>
        </div>

        <div style={{ 
          borderTop: '1px solid #111', 
          paddingTop: '40px', 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          fontSize: '0.65rem',
          color: '#3f3f46',
          letterSpacing: '0.1em'
        }}>
          <div>© 2026 QORE TECHNOLOGY. ALL RIGHTS RESERVED.</div>
          <div style={{ display: 'flex', gap: '24px' }}>
             <span>SECURE_ENCRYPTION_ACTIVE</span>
             <span>TERMS_OF_SERVICE</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default React.memo(Footer);
