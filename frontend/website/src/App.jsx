import React, { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios';
import FileUploadButton from './FileUploadButton';

function App() {

  // code to check if server is connected properly
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/data')
        .then(response => {
          console.log("Server connected successfully.");
        })
        .catch(error => console.error(error));
  }, []);

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
      })
      .catch((error) => {
        console.error("Upload failed: ", error);
        alert("Failed to upload files.");
      });
  }

  // be able to remove probes from excel file
  // update log when processing files

  return (
    <div className="container">
      <h1 className="head">BMIQ Normalization Tool</h1>
      <FileUploadButton onUpload={handleFileUpload} />
    </div>
  )
}

export default App
