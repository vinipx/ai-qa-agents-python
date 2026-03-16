import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)} style={{ 
      background: '#000', 
      padding: '160px 0', 
      borderBottom: '1px solid #18181b',
      position: 'relative',
      overflow: 'hidden'
    }}>
      <div style={{
        position: 'absolute',
        top: 0,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '100%',
        height: '100%',
        background: 'radial-gradient(circle at 50% 50%, rgba(255,255,255,0.03) 0%, transparent 70%)',
        pointerEvents: 'none'
      }} />
      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
           <div style={{ 
             padding: '12px', 
             background: '#09090b', 
             borderRadius: '12px', 
             marginBottom: '32px', 
             border: '1px solid #27272a',
             boxShadow: '0 0 20px rgba(255,255,255,0.05)'
           }}>
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>
           </div>
           <Heading as="h1" className="hero__title" style={{ 
             letterSpacing: '0.15em', 
             fontWeight: 900, 
             color: '#fff',
             fontSize: '3.5rem',
             margin: 0,
             fontFamily: 'var(--qore-font-title)',
             textIndent: '0.15em' // Balance the letter spacing
           }}>
            {siteConfig.title}
          </Heading>
          <p className="hero__subtitle" style={{ 
            color: '#71717a', 
            letterSpacing: '0.2em', 
            textTransform: 'uppercase', 
            fontSize: '0.75rem', 
            marginTop: '24px',
            fontWeight: 600
          }}>
            {siteConfig.tagline}
          </p>
          <div className={styles.buttons} style={{ marginTop: '64px' }}>
            <Link
              className="button button--secondary button--lg"
              style={{ 
                background: '#fff', 
                color: '#000', 
                border: 'none', 
                borderRadius: '4px', 
                fontWeight: 800, 
                letterSpacing: '0.2em', 
                fontSize: '0.7rem',
                padding: '12px 40px',
                transition: 'all 0.2s ease'
              }}
              to="/docs/intro">
              INITIALIZE_DOCS
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} | Protocol`}
      description="Agentic Quality Engineering Orchestrator">
      <HomepageHeader />
      <main style={{ background: '#000', padding: '100px 0' }}>
         <div className="container">
            <div className="row">
               <div className="col col--4">
                  <div style={{ 
                    padding: '40px', 
                    border: '1px solid #18181b', 
                    borderRadius: '16px', 
                    background: '#09090b',
                    height: '100%',
                    transition: 'border-color 0.3s ease'
                  }}>
                     <h3 style={{ color: '#fff', letterSpacing: '0.2em', fontSize: '0.8rem', fontWeight: 800, marginBottom: '20px' }}>01_AUTONOMOUS</h3>
                     <p style={{ color: '#52525b', fontSize: '0.85rem', lineHeight: '1.6', margin: 0 }}>End-to-end QE orchestration with specialized agents for manual QA, automation, and documentation. Zero manual overhead.</p>
                  </div>
               </div>
               <div className="col col--4">
                  <div style={{ 
                    padding: '40px', 
                    border: '1px solid #18181b', 
                    borderRadius: '16px', 
                    background: '#09090b',
                    height: '100%'
                  }}>
                     <h3 style={{ color: '#fff', letterSpacing: '0.2em', fontSize: '0.8rem', fontWeight: 800, marginBottom: '20px' }}>02_TRACEABLE</h3>
                     <p style={{ color: '#52525b', fontSize: '0.85rem', lineHeight: '1.6', margin: 0 }}>Real-time event streaming and graph visualization for complete observability of the agentic thinking process.</p>
                  </div>
               </div>
               <div className="col col--4">
                  <div style={{ 
                    padding: '40px', 
                    border: '1px solid #18181b', 
                    borderRadius: '16px', 
                    background: '#09090b',
                    height: '100%'
                  }}>
                     <h3 style={{ color: '#fff', letterSpacing: '0.2em', fontSize: '0.8rem', fontWeight: 800, marginBottom: '20px' }}>03_PERSISTENT</h3>
                     <p style={{ color: '#52525b', fontSize: '0.85rem', lineHeight: '1.6', margin: 0 }}>High-performance SQLite checkpointers ensure system state integrity across sessions and human interruptions.</p>
                  </div>
               </div>
            </div>
         </div>
      </main>
    </Layout>
  );
}
