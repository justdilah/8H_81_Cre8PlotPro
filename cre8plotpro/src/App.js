import logo from './logo.svg';
import './App.css';
import Chatbot from 'react-chatbot-kit'
import 'react-chatbot-kit/build/main.css'

import config from "./chatbot/config";
import messageParser from "./chatbot/MessageParser";
import actionProvider from "./chatbot/ActionProvider";
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Chatbot
        config={config}
        messageParser={messageParser}
        actionProvider={actionProvider}/>
      </header>
    </div>
  );
}

export default App;
