// UpcomingIPOs.jsx
const UpcomingIPOs = () => {
    const ipos = [
      { name: "XYZ Ltd.", date: "March 25, 2025", price: "₹750" },
      { name: "ABC Corp.", date: "April 5, 2025", price: "₹620" },
    ];
    return (
      <section className="py-12 px-4">
        <h2 className="text-3xl font-bold text-gray-900 text-center">Upcoming IPOs</h2>
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          {ipos.map((ipo, index) => (
            <div key={index} className="bg-white p-4 shadow-md rounded-lg">
              <h3 className="text-xl font-semibold">{ipo.name}</h3>
              <p className="text-gray-600">Listing Date: {ipo.date}</p>
              <p className="text-gray-600">Expected Price: {ipo.price}</p>
            </div>
          ))}
        </div>
      </section>
    );
  };
  
  export default UpcomingIPOs;