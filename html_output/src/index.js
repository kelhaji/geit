import React from 'react';
import ReactDOM from 'react-dom/client';
import './bootstrap.min.css';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <nav className="navbar navbar-expand-lg fixed-top navbar-white">
      <img src={process.env.REACT_APP_LOGO} alt="Geit logo" className="logo"/>
    </nav>
  
    <main role="main" className="container">
      <App />
    </main>
  </React.StrictMode>
);
