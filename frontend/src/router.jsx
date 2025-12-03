import { Routes, Route, Navigate } from "react-router-dom";
import ParcelList from "./pages/ParcelList.jsx";
import ParcelDetail from "./pages/ParcelDetail.jsx";
import ParcelCreate from "./pages/ParcelCreate.jsx";
import ParcelEdit from "./pages/ParcelEdit.jsx";
import ParcelSearch from "./pages/ParcelSearch.jsx";
import StatsDashboard from "./pages/StatsDashboard.jsx";

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/parcels" replace />} />
      <Route path="/parcels" element={<ParcelList />} />
      <Route path="/parcels/new" element={<ParcelCreate />} />
      <Route path="/parcels/:id" element={<ParcelDetail />} />
      <Route path="/parcels/:id/edit" element={<ParcelEdit />} />
      <Route path="/search" element={<ParcelSearch />} />
      <Route path="/stats" element={<StatsDashboard />} />
      <Route path="*" element={<div>Page not found</div>} />
    </Routes>
  );
}
