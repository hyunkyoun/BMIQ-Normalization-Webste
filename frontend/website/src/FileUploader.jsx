import React, { useState } from 'react';
import axios from 'axios';

const FileUploader = () => {
  const [output, setOutput] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileUpload = async (event) => {
    event.preventDefault();
    const betaFile = event.target.elements.betaFile.files[0];
    const probeFile = event.target.elements.probeFile.files[0];

    // Reset previous output
    setOutput([]);
    setIsProcessing(true);

    // Create FormData
    const formData = new FormData();
    formData.append('betaFile', betaFile);
    formData.append('probeFile', probeFile);

    try {
      // Use EventSource for streaming
      const eventSource = new EventSource(
        `http://127.0.0.1:5000/api/upload`,
        { method: 'POST', body: formData }
      );

      eventSource.onmessage = (event) => {
        if (event.data === '[DONE]') {
          eventSource.close();
          setIsProcessing(false);
        } else {
          setOutput(prev => [...prev, event.data]);
        }
      };

      eventSource.onerror = (error) => {
        console.error('EventSource failed:', error);
        eventSource.close();
        setIsProcessing(false);
      };

    } catch (error) {
      console.error('Upload error:', error);
      setIsProcessing(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleFileUpload}>
        <input type="file" name="betaFile" required />
        <input type="file" name="probeFile" required />
        <button type="submit">Upload and Process</button>
      </form>

      {isProcessing && (
        <div>
          <h3>Processing Output:</h3>
          {output.map((line, index) => (
            <div key={index}>{line}</div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FileUploader;