// Hero.jsx
import { useState } from "react";

const Hero = () => {
  const [search, setSearch] = useState("");
  return (
    <section className="bg-blue-100 py-16 text-center">
      <h1 className="text-4xl font-bold text-gray-900">AI-Driven IPO Analysis</h1>
      <p className="mt-4 text-lg text-gray-700">Get data-driven insights on upcoming IPOs</p>
      <div className="mt-6 flex justify-center">
        <input
          type="text"
          placeholder="Search for an IPO..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="p-2 rounded-l-lg border border-gray-300 w-64"
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded-r-lg">Search</button>
      </div>
    </section>
  );
};

export default Hero;