import {
  MapContainer,
  TileLayer,
  GeoJSON,
  LayersControl,
  ZoomControl,
  useMap,
} from "react-leaflet";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "leaflet/dist/leaflet.css";

const { BaseLayer } = LayersControl;

/* ===========================
   HELPERS
=========================== */

function zoningBucket(zoning) {
  const z = String(zoning || "").toLowerCase();
  if (z.includes("boisee")) return "forest";
  if (z.includes("champ") || z.includes("pre")) return "agriculture";
  if (z.includes("eau")) return "water";
  if (z.includes("revetement") || z.includes("bati") || z.includes("habitat"))
    return "built";
  return "other";
}

function zoningColor(zoning) {
  const bucket = zoningBucket(zoning);
  if (bucket === "forest") return "#14532d";
  if (bucket === "agriculture") return "#facc15";
  if (bucket === "water") return "#0284c7";
  if (bucket === "built") return "#16a34a";
  return "#6b7280";
}

/* Auto-zoom */
function FitBounds({ geojson }) {
  const map = useMap();

  useEffect(() => {
    if (!geojson?.features?.length) return;
    const layer = new window.L.GeoJSON(geojson);
    const bounds = layer.getBounds();
    if (bounds.isValid()) map.fitBounds(bounds, { padding: [40, 40] });
  }, [geojson, map]);

  return null;
}

/* ===========================
   MAIN MAP
=========================== */

export default function ParcelMap({
  geojson,
  height = "520px",
  showLegend = true, // 👈 KEY LINE
}) {
  const navigate = useNavigate();

  if (!geojson) return <div>Loading map…</div>;

  return (
    <div style={{ position: "relative" }}>
      {/* LEGEND (OPTIONAL) */}
      {showLegend && (
        <div
          style={{
            position: "absolute",
            zIndex: 1000,
            bottom: 12,
            left: 12,
            background: "rgba(255,255,255,0.75)",
            backdropFilter: "blur(6px)",
            padding: 12,
            borderRadius: 14,
            width: 240,
            boxShadow: "0 8px 24px rgba(0,0,0,0.15)",
            fontSize: 13,
          }}
        >
          <strong>Legend</strong>
          <LegendItem color="#14532d" label="Forest" />
          <LegendItem color="#facc15" label="Agriculture" />
          <LegendItem color="#0284c7" label="Water" />
          <LegendItem color="#16a34a" label="Built / buildable-ish" />
          <LegendItem color="#6b7280" label="Other" />
        </div>
      )}

      {/* MAP */}
      <MapContainer
        style={{ height, width: "100%" }}
        zoomControl={false}
        scrollWheelZoom
      >
        <ZoomControl position="bottomright" />

        <LayersControl position="topright">
          <BaseLayer checked name="Map">
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          </BaseLayer>
          <BaseLayer name="Satellite">
            <TileLayer url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" />
          </BaseLayer>
        </LayersControl>

        <GeoJSON
          data={geojson}
          style={(feature) => ({
            color: zoningColor(feature.properties?.zoning),
            weight: 2,
            fillOpacity: 0.35,
          })}
          onEachFeature={(feature, layer) => {
            const p = feature.properties || {};

            layer.bindTooltip(
              `<b>${p.id}</b><br/>
               ${Math.round(p.area_m2 || 0).toLocaleString()} m²<br/>
               ${p.is_buildable ? "Buildable" : "Not buildable"}`,
              { sticky: true }
            );

            layer.on("mouseover", () =>
              layer.setStyle({ fillOpacity: 0.65 })
            );
            layer.on("mouseout", () =>
              layer.setStyle({ fillOpacity: 0.35 })
            );

            layer.on("click", () => {
              if (p.id) navigate(`/parcels/${p.id}`);
            });
          }}
        />

        <FitBounds geojson={geojson} />
      </MapContainer>
    </div>
  );
}

function LegendItem({ color, label }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 6 }}>
      <span
        style={{
          width: 14,
          height: 14,
          background: color,
          borderRadius: 4,
          display: "inline-block",
        }}
      />
      <span>{label}</span>
    </div>
  );
}
