import React, { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios';

function App() {

  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/data')
        .then(response => {
          setData(response.data);
          console.log("fetch successful");
        })
        .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h1>React + Flask</h1>
      {data ? <p>{data.message}</p> : <p>Loading...</p>}
    </div>
  )
}

export default App
