import React, { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios';
import FileUploadButton from './FileUploadButton';
import Error404Page from './Error404Page';

function App() {

  const [isComplete, setIsComplete] = useState(false);
  const [isConnected, setIsConnected] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = (betaData, probeData) => {
    console.log("Beta File: ", betaData);
    console.log("Probe File: ", probeData);

    const formData = new FormData();
    formData.append("betaFile", betaData);
    formData.append("probeFile", probeData);

    axios.post("http://127.0.0.1:5000/api/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
    })
      .then((response) => {
        console.log("Upload successful: ", response.data);
        alert("Files uploaded successfully.");
        setIsComplete(true);
      })
      .catch((error) => {
        console.error("Upload failed: ", error);
        alert("Failed to upload files.");
      });
  }

  const handleDownload = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/download', { 
        responseType: 'blob' 
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'results.zip');
      
      // Append to document, click, and clean up
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  // future updates
  // check if server is connected. display 404 page if not
  // be able to remove probes from excel file
  // update log when processing files

  return (
    <div className="container">
      <h1 className="head">BMIQ Normalization Tool</h1>
      <FileUploadButton onUpload={handleFileUpload} />
      {isComplete && (
        <button onClick={handleDownload} className="downloadButton">
          Download Results
        </button>
      )}
    </div>
  );
}

export default App
