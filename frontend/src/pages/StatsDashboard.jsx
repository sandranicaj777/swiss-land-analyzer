import { useEffect, useState } from "react";
import api from "../services";

export default function StatsDashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.get("/parcels/stats").then(res => setStats(res.data));
  }, []);

  if (!stats) return <div className="p-6">Loading…</div>;

  const buildablePct = parseFloat(stats.buildable_percentage);
  const notBuildablePct = 100 - buildablePct;

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold">Parcel Statistics</h1>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Total Parcels"
          value={stats.total_parcels.toLocaleString()}
        />
        <StatCard
          title="Buildable Parcels"
          value={`${buildablePct.toFixed(1)}%`}
        />
        <StatCard
          title="Average Area"
          value={`${Math.round(stats.average_area_m2)} m²`}
        />
      </div>

      {/* BUILDABLE BAR */}
      <div className="bg-white rounded-xl p-6 shadow">
        <h2 className="font-semibold mb-4">Buildable vs Not Buildable</h2>

        <div className="h-6 w-full rounded-full overflow-hidden flex">
          <div
            className="bg-green-600"
            style={{ width: `${buildablePct}%` }}
          />
          <div
            className="bg-gray-400"
            style={{ width: `${notBuildablePct}%` }}
          />
        </div>

        <div className="flex justify-between text-sm mt-2 text-gray-600">
          <span>Buildable: {buildablePct.toFixed(1)}%</span>
          <span>Not buildable: {notBuildablePct.toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
}

/* ---------- SMALL COMPONENT ---------- */

function StatCard({ title, value }) {
  return (
    <div className="bg-white rounded-xl p-6 shadow">
      <div className="text-sm text-gray-500">{title}</div>
      <div className="text-3xl font-bold mt-2">{value}</div>
    </div>
  );
}
