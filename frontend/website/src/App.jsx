import React, { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios';
import FileUploadButton from './FileUploadButton';
import Error404Page from './Error404Page';
// import ProgressLabel from './ProgressLabel';

function App() {

  const [isComplete, setIsComplete] = useState(false);
  // const [isConnected, setIsConnected] = useState(true);
  // const [isLoading, setIsLoading] = useState(false);
  // const [progress, setProgress] = useState({ status: "Initializing...", progress: 0 });

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


  // // code for progress bar
  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     axios.get('/progress')
  //       .then((response) => {
  //         setProgress(response.data);
  //       })
  //       .catch((error) => {
  //         console.error("Failed to fetch progress:", error);
  //       });
  //   }, 1000); // Poll every second

  //   return () => clearInterval(interval);
  // }, []);

  // future updates
  // check if server is connected. display 404 page if not
  // be able to remove probes from excel file
  // update log when processing files

  return (
    <div className="container">
      <h1 className="head">BMIQ Normalization Tool</h1>
      <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
        <div>
          <div className="description-box">
            <div className="description-box-title">Description</div>
            A new model-based intra-array normalization strategy for 450k data, known as BMIQ (Beta MIxture Quantile dilation),
            aims to adjust the beta values of type 2 design probes to match the statistical distribution characteristics of type 1 probes.
            <br />
            <br />
            Teschendorff, A. E. , Marabita, F. , Lechner, M. , Bartlett, T. , Tegner, J. , & Gomez-Cabrero, D. , et al. 2013. “A beta-mixture quantile normalization method for correcting probe design bias in illumina infinium 450 k dna methylation data.” Bioinformatics, 29(2), 189-196.
          </div>
          <div className="content-box">
            <div className="content-box-title">Data Submission Form</div>
            <FileUploadButton onUpload={handleFileUpload} />
            {isComplete && (
              <button onClick={handleDownload} className="downloadButton">
                Download Results
              </button>
            )}
          </div>
        </div>
        <div className="directions-box">
          <div className="directions-box-title">Directions</div>
          <ol>
            <li>
              Upload the Beta file. It must have the list of probe sets with the corresponding beta values for each sample.
              An example is shown to the right:
              <img src="/example/img1.JPG" alt="Beta file example" />
            </li>
            <li>
              Upload the Probe file. It must have the column "targetid" with the corresponding probe information.
              The type of probe used should be stated in the probe information as the second to last number, as shown to the right:
              <img src="/example/img2.JPG" alt="Probe file example" />
            </li>
          </ol>
        </div>
      </div>
    </div>
  );
}

export default App;