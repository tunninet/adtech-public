import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [ad, setAd] = useState(null);

  // Reusable function to fetch an ad
  const fetchAd = async () => {
    try {
      // Generate random user ID between 1 and 10
      const userId = Math.floor(Math.random() * 10) + 1;
      
      const response = await axios.get(
        'https://<YOUR_API_URL>/ad',
        { params: { user_id: userId } }
      );
      
      console.log("Fetched ad data:", response.data);
      setAd(response.data);
    } catch (error) {
      console.error("Error fetching ad:", error);
    }
  };

  // Fetch an ad on initial component mount
  useEffect(() => {
    fetchAd();
    // eslint-disable-next-line
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Dynamic Ad Display</h1>

        {/* First line */}
        <p className="subtitle">
          Pulled from a simulated Kafka user event stream and a MongoDB Backend
        </p>
        {/* Second line, italic, slightly smaller */}
        <p className="subtitle" style={{ fontStyle: 'italic', fontSize: '0.9rem' }}>
          (A Full Stack Application for Simulated User Actions, retrieving related adverts, and returning them to the browser/app.)
        </p>

        {/* Usage Note */}
        <p className="usage-note">
          Usage: Refresh your browser or click the button below to see a new ad.
        </p>
        <button className="refresh-button" onClick={fetchAd}>
          Get Another Ad
        </button>

        {ad ? (
          <div className="ad-container">
            <div className="ad-details">
              <div className="ad-detail">
                <span className="label">User ID:</span>
                <span className="value">{ad.user_id}</span>
              </div>
              <div className="ad-detail">
                <span className="label">User Action:</span>
                <span className="value">{ad.event}</span>
              </div>
            </div>

            <h2 className="ad-title">{ad.ad}</h2>

            <div className="ad-image-wrapper">
              <img
                src={ad.image}
                alt={ad.ad}
                className="ad-image"
              />
            </div>
          </div>
        ) : (
          <p>Loading ad...</p>
        )}
      </header>
    </div>
  );
}

export default App;
