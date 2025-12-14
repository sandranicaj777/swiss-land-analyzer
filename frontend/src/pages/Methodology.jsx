export default function Methodology() {
    return (
      <div className="max-w-3xl mx-auto p-6 space-y-6">
        <h1 className="text-3xl font-bold">Methodology & Limitations</h1>
  
        <section>
          <h2 className="font-semibold text-lg mb-2">Purpose of this tool</h2>
          <p className="text-gray-700">
            Swiss Land Analyzer is an exploratory land intelligence platform designed
            to help users compare parcels, understand zoning context, and assess
            relative development potential across Switzerland.
          </p>
        </section>
  
        <section>
          <h2 className="font-semibold text-lg mb-2">Data sources</h2>
          <ul className="list-disc pl-5 text-gray-700">
            <li>Swiss cadastral parcel geometries (Swisstopo / cantonal sources)</li>
            <li>Derived parcel area calculations</li>
            <li>Rule-based zoning classification</li>
          </ul>
        </section>
  
        <section>
          <h2 className="font-semibold text-lg mb-2">Valuation approach</h2>
          <p className="text-gray-700">
            Estimated values are heuristic and illustrative. They are based on
            parcel size, buildability, and generalized assumptions rather than
            transaction-level market data.
          </p>
        </section>
  
        <section>
          <h2 className="font-semibold text-lg mb-2">Limitations & disclaimer</h2>
          <p className="text-gray-700">
            This platform does not provide legal, financial, or planning advice.
            Zoning laws, land-use restrictions, and development feasibility must
            always be confirmed with official cantonal authorities.
          </p>
          <p className="mt-2 italic text-gray-500">
            This tool is not a legal document.
          </p>
        </section>
      </div>
    );
  }
  