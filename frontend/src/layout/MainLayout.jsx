import { NavLink } from "react-router-dom";
import SwissParcelLogo from "../assets/logo.png"; 
const navLinkClasses = ({ isActive }) =>
  `px-3 py-2 rounded-md text-sm font-medium ${
    isActive
      ? "bg-red-600 text-white"
      : "text-slate-700 hover:bg-red-50 hover:text-red-700"
  }`;

export default function MainLayout({ children }) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          
          <div className="flex items-center gap-2">
            <img 
              src={SwissParcelLogo} 
              alt="SwissParcel Logo"
              className="h19 w-40 object-contain"
              style={{ imageRendering: "crisp-edges" }}
            />
          </div>

          <nav className="flex gap-2">
            <NavLink to="/parcels" className={navLinkClasses}>
              Parcels
            </NavLink>
            <NavLink to="/search" className={navLinkClasses}>
              Search
            </NavLink>
            <NavLink to="/parcels/new" className={navLinkClasses}>
              Create
            </NavLink>
            <NavLink to="/stats" className={navLinkClasses}>
              Stats
            </NavLink>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <div className="max-w-6xl mx-auto px-4 py-6">{children}</div>
      </main>

      <footer className="border-t bg-white mt-4">
        <div className="max-w-6xl mx-auto px-4 py-3 text-xs text-slate-500">
          SwissParcel - Demo frontend
        </div>
      </footer>
    </div>
  );
}