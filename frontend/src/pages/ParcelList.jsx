import { useEffect, useState } from "react";
import api from "../services";
import ParcelMap from "../components/ParcelMap";

export default function ParcelList() {
  const [geojson, setGeojson] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/parcels/geojson")
      .then(res => setGeojson(res.data))
      .catch(err => {
        console.error(err);
        setError("Failed to load parcels");
      });
  }, []);

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Swiss Parcels</h1>

      {error && <div className="text-red-600">{error}</div>}

      {geojson ? (
        <ParcelMap geojson={geojson} height="600px" />
      ) : (
        <div>Loading map…</div>
      )}
    </div>
  );
}
