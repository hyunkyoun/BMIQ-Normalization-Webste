import React from 'react'
import './Authors.css'

function Authors() {
  return (
    <div className='author-container'>
        <h1 className='heading'>Authors</h1>
        <p>The BMIQ Normalization Tool was developed by</p>
        <ul>
            <li className='author-link'><a href="https://www.linkedin.com/in/elliott-seo/">Elliott Seo</a></li>
            <li className='author-link'><a href="https://www.linkedin.com/in/hyunkyoun-kim/">Hyunkyoun Kim</a></li>
        </ul>
    </div>
  )
}

export default Authors