import React, { useState } from "react";
import './FileUploadButton.css';

function FileUploadButton({ onUpload }) {

    const [betaData, setBetaData] = useState(null);
    const [probeData, setProbeData] = useState(null);
    const [error, setError] = useState(null);

    const validateFile = (file) => {
        const fileExtension = file.name.split('.').pop();
        if (fileExtension !== "xlsx") {
            setError("Only .xlsx files are allowed.");
            return false;
        }
        setError("");
        return true;
    }

    const handleBetaFile = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile && validateFile(selectedFile)) {
            setBetaData(selectedFile);
        } else {
            setBetaData(null);
        }
    }

    const handleProbeFile = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile && validateFile(selectedFile)) {
            setProbeData(selectedFile);
        } else {
            setProbeData(null);
        }
    }

    const handleUploadClick = () => {
        if (betaData && probeData) {
            onUpload(betaData, probeData);
        } else {
            alert("Please select valid .xlsx files before uploading.")
        }

    }

    return (
        <div>
            <form className='container'>
                <div>
                    <label>Beta File: </label>
                    <input type="file" className="chooseButton" onChange={handleBetaFile} />
                </div>
                <div>
                    <label>Probe File: </label>
                    <input type="file" className="chooseButton" onChange={handleProbeFile} />
                </div>
                <button type="button" className="uploadButton" onClick={handleUploadClick}>
                    Upload
                </button>
            </form>
        </div>
    );
}

export default FileUploadButton;
