import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import 'antd/dist/antd.css';
import { MsalProvider } from '@azure/msal-react';
import msalInstance, { initializeMsal } from './components/security/auth/AuthConfig';
import AuthProvider from './components/security/auth/AuthContext';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

const AppWrapper: React.FC = () => {
  const [isInitialized, setIsInitialized] = useState(false);
  const [initError, setInitError] = useState<Error | null>(null);

  useEffect(() => {
    const init = async () => {
      try {
        await initializeMsal();
        setIsInitialized(true);
      } catch (error: unknown) {
        console.error('MSAL Initialization Error:', error);
        if (error instanceof Error) {
          setInitError(error);
        } else {
          setInitError(new Error('Unknown initialization error'));
        }
      }
    };

    init();
  }, []);

  if (initError) {
    return <div style={{ padding: '20px', textAlign: 'center' }}>
      <h2>Initialization Error</h2>
      <p>{initError.message}</p>
    </div>;
  }

  if (!isInitialized) {
    return <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh'
    }}>Loading...</div>;
  }

  return (
    <AuthProvider>
      <MsalProvider instance={msalInstance}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </MsalProvider>
    </AuthProvider>
  );
};

root.render(
  // <React.StrictMode>
  <AppWrapper />
  // </React.StrictMode>
);
