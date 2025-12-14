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
    <div className="min-h-screen flex flex-col bg-gray-50">
      
      {/* HEADER / NAVBAR */}
      <header className="bg-white border-b shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          
          {/* LOGO */}
          <div className="flex items-center gap-2">
          <NavLink to="/parcels" className="flex items-center gap-3">
  <img
    src={SwissParcelLogo}
    alt="SwissParcel Logo"
 className="h-20 w-auto object-contain"
  />
</NavLink>

          </div>

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
        <div className="max-w-6xl mx-auto px-4 py-6">
          {children}
        </div>
      </main>

      {/* FOOTER */}
      <footer className="border-t bg-white">
        <div className="max-w-6xl mx-auto px-4 py-6 text-sm text-slate-600 space-y-2">
        


          <div className="pt-2 text-xs text-slate-400">
            © {new Date().getFullYear()} SwissParcel - Exploratory land intelligence platform for Switzerland Demo
          </div>
        </div>
      </footer>
    </div>
  );
}
