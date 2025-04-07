import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { Input, Button } from "@/components/ui/button";

export default function SunlitTerraces() {
  const [location, setLocation] = useState("");
  const [venues, setVenues] = useState([]);

  const fetchVenues = async () => {
    const response = await fetch(
      `http://localhost:8000/venues?location=${location}&radius=1000&min_rating=4.0`
    );
    const data = await response.json();
    setVenues(data.results || []);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Find Sunlit Terraces</h1>
      <div className="flex gap-2 mb-4">
        <Input
          type="text"
          placeholder="Enter location (lat,lng)"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <Button onClick={fetchVenues}>Search</Button>
      </div>
      <MapContainer center={[51.5074, -0.1278]} zoom={13} className="h-96 w-full">
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {venues.map((venue, index) => (
          <Marker key={index} position={[venue.geometry.location.lat, venue.geometry.location.lng]}>
            <Popup>
              <strong>{venue.name}</strong>
              <p>Rating: {venue.rating}</p>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
