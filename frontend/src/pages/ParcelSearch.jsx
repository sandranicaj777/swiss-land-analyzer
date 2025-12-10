import { useState } from "react";
import api from "../services.js"


export default function ParcelSearch() {
  const [canton, setCanton] = useState("");
  const [buildable, setBuildable] = useState("");
  const [results, setResults] = useState([]);

  function search() {
    api.get("/parcels/search", {
      params: {
        canton: canton || undefined,
        buildable: buildable === "" ? undefined : buildable === "true"
      }
    }).then(res => setResults(res.data));
  }

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Search Parcels</h1>

      <div className="space-y-3">
        <input className="border p-2 w-full"
               placeholder="Canton"
               value={canton}
               onChange={e => setCanton(e.target.value)} />

        <select className="border p-2 w-full"
                onChange={e => setBuildable(e.target.value)}>
          <option value="">Any</option>
          <option value="true">Buildable</option>
          <option value="false">Not Buildable</option>
        </select>

        <button className="bg-red-600 text-white px-4 py-2 rounded"
                onClick={search}>
          Search
        </button>
      </div>

      <ul className="mt-4 space-y-2">
        {results.map(r => (
          <li key={r.id} className="border rounded p-2">
            {r.id} • {r.canton} • {r.area_m2} m²
          </li>
        ))}
      </ul>
    </div>
  );
}
