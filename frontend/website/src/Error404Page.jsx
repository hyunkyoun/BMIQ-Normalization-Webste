import React from "react";
import './Error404Page.css';

const Error404Page = () => {
  return (
    <div className="error-page">
      <h1 className="head">404</h1>
      <p className="subhead">
        Oops! The page you're looking for doesn't exist. <br />
        Please check again later!
      </p>
    </div>
  );
};

export default Error404Page;