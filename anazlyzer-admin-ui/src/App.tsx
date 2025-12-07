import './App.css';
import './index.css';
import AppRoutes from './AppRoutes';
import { useAuth } from './components/security/auth/AuthContext';

function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return <AppRoutes />;
}

export default App;
