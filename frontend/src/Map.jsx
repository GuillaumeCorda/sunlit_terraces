import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapWithVenues = () => {
  const [venues, setVenues] = useState([]);
  const [center, setCenter] = useState([48.8566, 2.3522]); // Default: Paris
  const [locationInput, setLocationInput] = useState('');
  const [radiusInput, setRadiusInput] = useState(1000);

  const fetchVenues = async () => {
    if (!locationInput) return;
    try {
      const res = await fetch(
        `http://localhost:8000/venues?location=${encodeURIComponent(
          locationInput
        )}&radius=${radiusInput}`
      );
      const data = await res.json();
      setVenues(data.venues || []);
      if (data.location) setCenter([data.location.lat, data.location.lng]);
    } catch (error) {
      console.error('Error fetching venues:', error);
    }
  };

  useEffect(() => {
    fetchVenues(); // optionally auto-load on mount
  }, []);

  return (
    <div className="w-full h-screen flex flex-col items-center gap-4 px-4 py-6">
      <div className="flex gap-2 w-full max-w-xl">
        <input
          type="text"
          placeholder="Enter location"
          value={locationInput}
          onChange={(e) => setLocationInput(e.target.value)}
          className="flex-1 p-4 text-lg rounded-xl border border-gray-300 focus:ring-2 focus:ring-purple-300"
        />
        <input
          type="number"
          placeholder="Radius (m)"
          value={radiusInput}
          onChange={(e) => setRadiusInput(e.target.value)}
          className="w-32 p-4 text-lg rounded-xl border border-gray-300 focus:ring-2 focus:ring-purple-300"
        />
        <button
          onClick={fetchVenues}
          className="bg-purple-500 hover:bg-purple-600 text-white font-semibold px-6 rounded-xl text-lg"
        >
          Search
        </button>
      </div>

      <div className="w-full max-w-5xl h-[600px] rounded-xl overflow-hidden">
        <MapContainer center={center} zoom={15} style={{ height: '100%', width: '100%' }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {venues.map((venue) => (
            <Marker key={venue.id} position={[venue.lat, venue.lng]}>
              <Popup>
                <strong>{venue.name}</strong><br />
                {venue.address}<br />
                ⭐ {venue.rating || 'N/A'}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};

export default MapWithVenues;
