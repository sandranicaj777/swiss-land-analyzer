import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../services.js"


export default function ParcelDetail() {
  const { id } = useParams();
  const [parcel, setParcel] = useState(null);
  const [score, setScore] = useState(null);
  const [summary, setSummary] = useState(null);
  const [value, setValue] = useState(null);
  const [potential, setPotential] = useState(null);

  useEffect(() => {
    api.get(`/parcels/${id}`).then(res => setParcel(res.data));
    api.get(`/parcels/${id}/score`).then(res => setScore(res.data));
    api.get(`/parcels/${id}/summary`).then(res => setSummary(res.data));
    api.get(`/parcels/${id}/value-estimate`).then(res => setValue(res.data));
    api.get(`/parcels/${id}/development-potential`).then(res => setPotential(res.data));
  }, [id]);

  if (!parcel) return <div>Loading...</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">
        Parcel {parcel.id}
      </h1>

      <div className="grid grid-cols-2 gap-4">
        <div className="border p-4 rounded">
          <p><strong>Canton:</strong> {parcel.canton}</p>
          <p><strong>Area:</strong> {parcel.area_m2} m²</p>
          <p><strong>Zoning:</strong> {parcel.zoning}</p>
          <p><strong>Buildable:</strong> {parcel.is_buildable ? "Yes" : "No"}</p>
        </div>

        <div className="border p-4 bg-red-50 rounded">
          <h2 className="font-bold mb-2">AI Insights</h2>

          {score && <p>Score: <strong>{score.score}</strong></p>}
          {summary && <p dangerouslySetInnerHTML={{ __html: summary.summary }} />}
          {value && <p>Estimated Value: <strong>{value.estimated_value_chf} CHF</strong></p>}
          {potential && <p>Potential: <strong>{potential.development_potential}</strong></p>}
        </div>
      </div>
    </div>
  );
}
