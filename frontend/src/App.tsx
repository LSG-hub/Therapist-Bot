import { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import './styles/global.css';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';
import { SessionProvider } from './contexts/SessionContext';

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <SessionProvider>
      <div className="app-container">
        <Sidebar 
          collapsed={sidebarCollapsed}
          onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
        />
        <main className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
          <ChatInterface />
        </main>
      </div>
    </SessionProvider>
  );
}

export default App;