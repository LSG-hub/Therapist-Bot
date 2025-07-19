import 'bootstrap/dist/css/bootstrap.min.css';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <div className="App d-flex flex-column" style={{ height: '100vh' }}>
      <ChatInterface />
    </div>
  );
}

export default App
