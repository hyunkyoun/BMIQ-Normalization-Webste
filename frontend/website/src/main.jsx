import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

import Authors from './Authors.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    {/* <Authors /> */}
  </StrictMode>,
)
