import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../services.js";

export default function ParcelSearch() {
  const [canton, setCanton] = useState("");
  const [buildable, setBuildable] = useState("");
  const [minArea, setMinArea] = useState("");
  const [maxArea, setMaxArea] = useState("");
  const [zoning, setZoning] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  function search() {
    setLoading(true);

    api
      .get("/parcels/search", {
        params: {
          canton: canton || undefined,
          buildable: buildable === "" ? undefined : buildable === "true",
          min_area: minArea || undefined,
          max_area: maxArea || undefined,
          zoning: zoning || undefined,
        },
      })
      .then((res) => setResults(res.data))
      .finally(() => setLoading(false));
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Search Parcels</h1>

      {/* FILTERS */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
        <input
          className="border p-2 rounded"
          placeholder="Canton (e.g. FR)"
          value={canton}
          onChange={(e) => setCanton(e.target.value)}
        />

        <select
          className="border p-2 rounded"
          value={buildable}
          onChange={(e) => setBuildable(e.target.value)}
        >
          <option value="">Any status</option>
          <option value="true">Buildable</option>
          <option value="false">Not buildable</option>
        </select>

        <input
          className="border p-2 rounded"
          type="number"
          placeholder="Min area (m²)"
          value={minArea}
          onChange={(e) => setMinArea(e.target.value)}
        />

        <input
          className="border p-2 rounded"
          type="number"
          placeholder="Max area (m²)"
          value={maxArea}
          onChange={(e) => setMaxArea(e.target.value)}
        />

        <select
          className="border p-2 rounded md:col-span-2"
          value={zoning}
          onChange={(e) => setZoning(e.target.value)}
        >
          <option value="">Any land type</option>
          <option value="forest">Forest</option>
          <option value="agriculture">Agriculture</option>
          <option value="water">Water</option>
          <option value="built">Built / buildable-ish</option>
          <option value="other">Other</option>
        </select>

        <button
          className="bg-red-600 text-white px-4 py-2 rounded md:col-span-2"
          onClick={search}
        >
          Search
        </button>
      </div>

  
    
      <ul className="space-y-3">
        {results.map((r) => (
          <li
            key={r.id}
            className="border rounded p-4 hover:bg-gray-50 transition"
          >
            <Link to={`/parcels/${r.id}`} className="block">
              <div className="font-semibold text-lg">{r.id}</div>
              <div className="text-sm text-gray-600">
                Canton: {r.canton}<br />
                Area: {Math.round(r.area_m2)} m²<br />
                Status: {r.is_buildable ? "Buildable" : "Not buildable"}
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
