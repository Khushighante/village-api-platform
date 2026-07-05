import React from 'react'
import ReactDOM from 'react-dom/client'

const App = () => {
  return React.createElement('h1', null, 'Hello World! Dashboard is Alive!');
};

const rootEl = document.getElementById('root');
if (rootEl) {
  ReactDOM.createRoot(rootEl).render(React.createElement(App));
}
