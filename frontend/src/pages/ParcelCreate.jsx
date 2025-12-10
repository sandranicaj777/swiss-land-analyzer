import { useState } from "react";
import api from "../services.js"
import { useNavigate } from "react-router-dom";

export default function ParcelCreate() {
  const [form, setForm] = useState({
    id: "",
    canton: "",
    area_m2: "",
    zoning: "",
    is_buildable: false
  });

  const navigate = useNavigate();

  function update(field, value) {
    setForm(prev => ({ ...prev, [field]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();

    api.post("/parcels", form)
      .then(() => navigate("/parcels"))
      .catch(err => console.error(err));
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-lg">
      <h1 className="text-2xl font-bold">Create Parcel</h1>

      <input className="border p-2 w-full"
             placeholder="Parcel ID"
             onChange={e => update("id", e.target.value)} />

      <input className="border p-2 w-full"
             placeholder="Canton"
             onChange={e => update("canton", e.target.value)} />

      <input className="border p-2 w-full"
             placeholder="Area m²"
             type="number"
             onChange={e => update("area_m2", Number(e.target.value))} />

      <input className="border p-2 w-full"
             placeholder="Zoning"
             onChange={e => update("zoning", e.target.value)} />

      <label className="flex items-center gap-2">
        <input type="checkbox"
               onChange={e => update("is_buildable", e.target.checked)} />
        Is Buildable
      </label>

      <button className="bg-red-600 text-white px-4 py-2 rounded">
        Create
      </button>
    </form>
  );
}
