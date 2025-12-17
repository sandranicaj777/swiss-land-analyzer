import { useNavigate } from "react-router-dom";
import { useState } from "react";
import LandingImage from "../assets/landing.png";

export default function LandingPage() {
  const navigate = useNavigate();
  const [canton, setCanton] = useState("FR");

  const handleStart = () => {
    navigate("/parcels");
  };

  return (
    <>
      {/* LOCAL, CONTINUOUS ANIMATIONS */}
      <style>
        {`
          @keyframes floatSoft {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
            100% { transform: translateY(0px); }
          }

          @keyframes floatImage {
            0% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-10px) scale(1.01); }
            100% { transform: translateY(0px) scale(1); }
          }

          .headline-float {
            animation: floatSoft 6s ease-in-out infinite;
          }

          .image-float {
            animation: floatImage 8s ease-in-out infinite;
          }
        `}
      </style>

      <div className="min-h-[75vh] flex items-center justify-center px-6">
        <div className="max-w-6xl w-full grid grid-cols-1 md:grid-cols-2 gap-12 items-center">

          {/* LEFT: TEXT */}
          <div className="space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight leading-tight headline-float text-slate-900 dark:text-white">
              Ready to find your parcel’s{" "}
              <span className="text-red-600">true potential</span>?
            </h1>

            <p className="text-slate-600 dark:text-slate-300 text-lg">
              SwissParcel is an exploratory land intelligence platform that uses
              official cadastral data and AI-assisted analysis to help you
              understand zoning context, buildability, and development potential
              across Switzerland.
            </p>

            {/* VALUE POINTS */}
            <ul className="space-y-2 text-slate-700 dark:text-slate-300">
              <li>✓ Parcel-level valuation estimates</li>
              <li>✓ Zoning & buildability context</li>
              <li>✓ AI-assisted development insights</li>
              <li>✓ Transparent methodology & limitations</li>
            </ul>

            {/* SELECT */}
            <div className="pt-4 space-y-2">
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
                Select canton
              </label>

              <select
                value={canton}
                onChange={(e) => setCanton(e.target.value)}
                className="
                  px-4 py-2 rounded-md border
                  border-slate-300 dark:border-slate-700
                  bg-white dark:bg-black
                  text-slate-800 dark:text-white
                  focus:outline-none focus:ring-2 focus:ring-red-500
                "
              >
                <option value="FR">Fribourg (available)</option>
                <option disabled>Vaud (coming soon)</option>
                <option disabled>Bern (coming soon)</option>
                <option disabled>Zurich (coming soon)</option>
              </select>
            </div>

            {/* CTA */}
            <div className="pt-6">
              <button
                onClick={handleStart}
                className="px-8 py-3 rounded-md bg-red-600 text-white font-semibold text-lg hover:bg-red-700 transition transform hover:scale-[1.03] hover:shadow-lg"
              >
                Start exploring
              </button>
            </div>

            {/* DISCLAIMER */}
            <p className="text-xs text-slate-400 pt-2">
              Heuristic estimates · Not legal or financial advice ·{" "}
              <span className="underline cursor-pointer">
                See methodology & limitations
              </span>
            </p>
          </div>

          {/* RIGHT: IMAGE */}
          <div className="flex justify-center image-float">
            <img
              src={LandingImage}
              alt="SwissParcel land intelligence illustration"
              className="w-full max-w-md drop-shadow-xl"
            />
          </div>
        </div>
      </div>
    </>
  );
}
