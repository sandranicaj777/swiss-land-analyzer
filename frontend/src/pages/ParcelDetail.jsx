import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../services";
import ParcelMap from "../components/ParcelMap";

function Card({ title, children }) {
  return (
    <div className="bg-white rounded-xl shadow p-5 space-y-2">
      {title && <h2 className="text-lg font-semibold">{title}</h2>}
      {children}
    </div>
  );
}

export default function ParcelDetail() {
  const { id } = useParams();

  const [parcel, setParcel] = useState(null);
  const [summary, setSummary] = useState(null);
  const [score, setScore] = useState(null);
  const [value, setValue] = useState(null);
  const [potential, setPotential] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [restrictions, setRestrictions] = useState(null);
  const [zoningExplanation, setZoningExplanation] = useState(null);

  useEffect(() => {
    api.get(`/parcels/${id}`).then(res => setParcel(res.data));
    api.get(`/parcels/${id}/summary`).then(res => setSummary(res.data));
    api.get(`/parcels/${id}/score`).then(res => setScore(res.data));
    api.get(`/parcels/${id}/value-estimate`).then(res => setValue(res.data));
    api.get(`/parcels/${id}/development-potential`).then(res => setPotential(res.data));
    api.get(`/parcels/${id}/recommendations`).then(res => setRecommendations(res.data));
    api.get(`/parcels/${id}/restrictions`).then(res => setRestrictions(res.data));
    api.get(`/parcels/${id}/zoning-explanation`).then(res => setZoningExplanation(res.data));
  }, [id]);

  if (!parcel) return <div className="p-6">Loading parcel…</div>;

  const geojson = parcel.geometry
    ? {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            geometry: parcel.geometry,
            properties: {
              id: parcel.id,
              is_buildable: parcel.is_buildable,
              zoning: parcel.zoning,
            },
          },
        ],
      }
    : null;

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold">Parcel {parcel.id}</h1>

      {geojson && (
        <div className="rounded-xl overflow-hidden shadow">
          <ParcelMap geojson={geojson} height="320px" showLegend={false} />
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        <Card title="Overview">
          <p><strong>Canton:</strong> {parcel.canton}</p>
          <p><strong>Area:</strong> {Math.round(parcel.area_m2)} m²</p>
          <p><strong>Zoning:</strong> {parcel.zoning}</p>
          <p>
            <strong>Status:</strong>{" "}
            <span className={parcel.is_buildable ? "text-green-600" : "text-gray-500"}>
              {parcel.is_buildable ? "Buildable" : "Not buildable"}
            </span>
          </p>
        </Card>

        <Card title="Value & Potential">
          {value && (
            <>
              <p className="text-2xl font-bold">
                {Math.round(value.estimated_value_chf).toLocaleString()} CHF
              </p>
              <p className="text-sm text-gray-600">{value.method}</p>
            </>
          )}

          {potential && (
            <div className="mt-3">
              <p>
                <strong>Development potential:</strong>{" "}
                {potential.development_potential}
              </p>
              <p className="text-sm text-gray-600">
                {potential.highest_best_use}
              </p>
            </div>
          )}

          <div className="mt-3 text-xs text-gray-500">
            Estimates are illustrative ·{" "}
            <Link
              to="/methodology"
              className="text-red-600 hover:underline"
            >
              See methodology & limitations
            </Link>
          </div>
        </Card>

        {summary && (
          <Card title="AI Summary">
            <div
              className="prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ __html: summary.summary }}
            />
          </Card>
        )}

        {score && (
          <Card title="Development Score">
            <p className="text-2xl font-bold">{score.score} / 100</p>
            <p className="text-sm text-gray-600">{score.explanation}</p>
          </Card>
        )}
      </div>

      {zoningExplanation && (
        <Card title="Zoning Explanation">
          <div
            className="prose prose-sm max-w-none"
            dangerouslySetInnerHTML={{
              __html: zoningExplanation.zoning_explanation,
            }}
          />
        </Card>
      )}

      {restrictions && (
        <Card title="Restrictions">
          <ul className="list-disc pl-5 space-y-1">
            {restrictions.major_restrictions.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </Card>
      )}

      {recommendations && (
        <Card title="Recommendations">
          <ul className="list-disc pl-5 space-y-1">
            {recommendations.recommendations.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
