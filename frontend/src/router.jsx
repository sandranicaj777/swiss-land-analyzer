import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage.jsx";
import ParcelList from "./pages/ParcelList.jsx";
import ParcelDetail from "./pages/ParcelDetail.jsx";
import ParcelCreate from "./pages/ParcelCreate.jsx";
import ParcelEdit from "./pages/ParcelEdit.jsx";
import ParcelSearch from "./pages/ParcelSearch.jsx";
import StatsDashboard from "./pages/StatsDashboard.jsx";
import Methodology from "./pages/Methodology.jsx";

export default function AppRouter() {
  return (
    <Routes>
      {/* LANDING */}
      <Route path="/" element={<LandingPage />} />

      {/* PARCELS */}
      <Route path="/parcels" element={<ParcelList />} />
      <Route path="/parcels/new" element={<ParcelCreate />} />
      <Route path="/parcels/:id" element={<ParcelDetail />} />
      <Route path="/parcels/:id/edit" element={<ParcelEdit />} />

      {/* OTHER */}
      <Route path="/search" element={<ParcelSearch />} />
      <Route path="/stats" element={<StatsDashboard />} />
      <Route path="/methodology" element={<Methodology />} />

      <Route path="*" element={<div>Page not found</div>} />
    </Routes>
  );
}
