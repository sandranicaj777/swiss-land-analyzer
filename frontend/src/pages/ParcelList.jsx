import { useEffect, useState } from "react";
import api from "../services.js"

export default function ParcelList() {
  const [parcels, setParcels] = useState([]);

  useEffect(() => {
    api.get("/parcels")
      .then(res => setParcels(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Parcels</h1>

      <ul className="space-y-3">
        {parcels.map(p => (
          <li key={p.id} className="border rounded p-3">
            <strong>{p.id}</strong> • {p.canton} • {p.area_m2} m²  
          </li>
        ))}
      </ul>
    </div>
  );
}
