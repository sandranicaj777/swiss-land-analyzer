import { useEffect, useState } from "react";
import api from "../services";

export default function StatsDashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.get("/parcels/stats").then(res => setStats(res.data));
  }, []);

  if (!stats)
    return (
      <div className="p-6 text-slate-700 dark:text-slate-300">
        Loading…
      </div>
    );

  const buildablePct = parseFloat(stats.buildable_percentage);
  const notBuildablePct = 100 - buildablePct;

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
        Parcel Statistics
      </h1>

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

      <div className="rounded-xl p-6 shadow bg-white dark:bg-black border border-slate-200 dark:border-slate-800">
        <h2 className="font-semibold mb-4 text-slate-800 dark:text-slate-200">
          Buildable vs Not Buildable
        </h2>

        <div className="h-6 w-full rounded-full overflow-hidden flex bg-slate-200 dark:bg-slate-800">
          <div
            className="bg-green-600"
            style={{ width: `${buildablePct}%` }}
          />
          <div
            className="bg-slate-400 dark:bg-slate-600"
            style={{ width: `${notBuildablePct}%` }}
          />
        </div>

        <div className="flex justify-between text-sm mt-2 text-slate-600 dark:text-slate-400">
          <span>Buildable: {buildablePct.toFixed(1)}%</span>
          <span>Not buildable: {notBuildablePct.toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
}


function StatCard({ title, value }) {
  return (
    <div className="rounded-xl p-6 shadow bg-white dark:bg-black border border-slate-200 dark:border-slate-800">
      <div className="text-sm text-slate-500 dark:text-slate-400">
        {title}
      </div>
      <div className="text-3xl font-bold mt-2 text-slate-900 dark:text-white">
        {value}
      </div>
    </div>
  );
}
