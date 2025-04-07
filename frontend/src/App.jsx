import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet icon issues
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png',
});

const MapCenterUpdater = ({ center }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center);
  }, [center, map]);
  return null;
};

const App = () => {
  const [location, setLocation] = useState('');
  const [radius, setRadius] = useState(1000);
  const [hour, setHour] = useState('');
  const [venues, setVenues] = useState([]);
  const [center, setCenter] = useState([51.5074, -0.1278]);
  const [hoveredId, setHoveredId] = useState(null);

  const fetchVenues = async () => {
    if (!location) return;
    try {
      const res = await fetch(
        `http://localhost:8000/venues?location=${encodeURIComponent(location)}&radius=${radius}&hour=${hour}`
      );
      const data = await res.json();
      setVenues(data.venues || []);
      if (data.location) {
        setCenter([data.location.lat, data.location.lng]);
      }
    } catch (err) {
      console.error('Error fetching venues:', err);
    }
  };

  const topVenues = venues.slice(0, 10);

  return (
    <div className="min-h-screen w-full px-4 py-10 flex flex-col items-center space-y-10">
      <div className="bg-white/90 backdrop-blur-lg shadow-2xl rounded-3xl p-10 max-w-6xl w-full text-center space-y-6">
        <h1 className="text-5xl font-extrabold text-gray-800">Sunlit Terraces</h1>
        <p className="text-2xl text-gray-600">Discover sunny cafés, bars, and restaurants near you.</p>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="📍 Location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="text-xl p-4 rounded-xl border border-gray-300 focus:outline-none focus:ring-4 focus:ring-purple-200 focus:border-purple-400 transition w-full"
          />
          <input
            type="number"
            placeholder="📏 Radius (m)"
            value={radius}
            onChange={(e) => setRadius(e.target.value)}
            className="text-xl p-4 rounded-xl border border-gray-300 focus:outline-none focus:ring-4 focus:ring-purple-200 focus:border-purple-400 transition w-full"
          />
          <input
            type="time"
            value={hour}
            onChange={(e) => setHour(e.target.value)}
            className="text-xl p-4 rounded-xl border border-gray-300 focus:outline-none focus:ring-4 focus:ring-purple-200 focus:border-purple-400 transition w-full"
          />
          <button
            onClick={fetchVenues}
            className="w-full py-4 text-xl font-semibold text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 rounded-xl shadow-md transition duration-300"
          >
            🔍 Search
          </button>
        </div>
      </div>

      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map */}
        <div className="col-span-2 h-[600px] rounded-3xl overflow-hidden shadow-2xl border border-gray-300">
          <MapContainer
            center={center}
            zoom={14}
            scrollWheelZoom={true}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
            />
            <MapCenterUpdater center={center} />
            {venues.map((venue) => (
              <Marker key={venue.id} position={[venue.lat, venue.lng]}>
                <Popup>
                  <strong>{venue.name}</strong><br />
                  {venue.address}<br />
                  ⭐ {venue.rating || 'N/A'}<br />
                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${venue.lat},${venue.lng}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 underline"
                  >
                    📍 View on Google Maps
                  </a>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        {/* Venue list */}
        <div className="bg-white/90 rounded-3xl shadow-lg p-6 space-y-4 overflow-y-auto max-h-[600px]">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Top 10 Nearby Spots</h2>
          {topVenues.length === 0 ? (
            <p className="text-gray-500">No results yet.</p>
          ) : (
            topVenues.map((venue) => (
              <div
                key={venue.id}
                onMouseEnter={() => setHoveredId(venue.id)}
                onMouseLeave={() => setHoveredId(null)}
                className={`text-left border-b border-gray-200 pb-3 cursor-pointer transition ${
                  hoveredId === venue.id ? 'bg-purple-100' : ''
                }`}
              >
                <h3 className="text-lg font-semibold text-purple-700">{venue.name}</h3>
                <p className="text-sm text-gray-600">{venue.address}</p>
                <p className="text-sm text-yellow-600">⭐ {venue.rating || 'N/A'}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
