import React from 'react';

const ProgressLabel = ({ progress }) => {
  return (
    <div className="progress-container">
      <p>{progress.status}</p>
      {progress.progress >= 0 && progress.progress <= 100 && (
        <progress value={progress.progress} max="100"></progress>
      )}
      {progress.progress === 100 && <p>Computation Complete!</p>}
      {progress.progress === -1 && <p style={{ color: 'red' }}>Error: {progress.status}</p>}
    </div>
  );
};

export default ProgressLabel;
