import { NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import SwissParcelLogo from "../assets/logoswiss.png";

const navLinkClasses = ({ isActive }) =>
  `px-3 py-2 rounded-md text-sm font-medium transition
   ${
     isActive
       ? "bg-red-600 text-white"
       : "text-slate-700 dark:text-slate-200 hover:bg-red-50 dark:hover:bg-slate-800 hover:text-red-700"
   }`;

export default function MainLayout({ children }) {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [dark]);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-black transition-colors">

      {/* HEADER / NAVBAR */}
      <header className="bg-white dark:bg-black border-b border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">

          {/* LOGO → LANDING PAGE */}
          <NavLink
            to="/"
            className="flex items-center gap-3 hover:opacity-90 transition"
          >
            <img
              src={SwissParcelLogo}
              alt="SwissParcel Logo"
              className="h-10 w-auto object-contain"
            />

            <span className="text-xl font-semibold tracking-tight">
              <span className="text-red-500">swiss</span>
              <span className="text-slate-800 dark:text-white">parcel</span>
            </span>
          </NavLink>

          {/* NAV LINKS */}
          <nav className="flex gap-2 items-center">
            <NavLink to="/parcels" className={navLinkClasses}>
              Parcels
            </NavLink>
            <NavLink to="/search" className={navLinkClasses}>
              Search
            </NavLink>
            <NavLink to="/stats" className={navLinkClasses}>
              Stats
            </NavLink>
            <NavLink to="/methodology" className={navLinkClasses}>
              Methodology
            </NavLink>
          </nav>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="flex-1">
        <div className="max-w-6xl mx-auto px-4 py-6 text-slate-900 dark:text-slate-100 transition-colors">
          {children}
        </div>
      </main>

      {/* FOOTER */}
      <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-black transition-colors">
        <div className="max-w-6xl mx-auto px-4 py-6 text-sm text-slate-600 dark:text-slate-400 space-y-3 flex flex-col sm:flex-row sm:items-center sm:justify-between">

          <div className="text-xs text-slate-400">
            © {new Date().getFullYear()} SwissParcel - Exploratory land intelligence platform for Switzerland (Demo)
          </div>

          {/* DARK MODE TOGGLE */}
          <button
            onClick={() => setDark((prev) => !prev)}
            className="text-xs px-3 py-1 rounded-md border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-900 transition"
          >
            {dark ? "☀️ Light mode" : "🌙 Dark mode"}
          </button>
        </div>
      </footer>
    </div>
  );
}
