import { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, X } from "lucide-react";

const Navbar = () => {
  return (
    <nav className="flex justify-center py-4 bg-gray-100">
      <div className="flex items-center justify-between w-[80%] bg-white shadow-md rounded-2xl px-8 py-3">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <img src="/logo.png" alt="Logo" className="w-6 h-6" />
          <span className="text-lg font-semibold text-blue-600">Sitemark</span>
        </div>

        {/* Navigation Links */}
        <ul className="flex space-x-6 text-gray-600 text-sm">
          {["Features", "Testimonials", "Highlights", "Pricing", "FAQ", "Blog"].map((item, index) => (
            <li key={index} className="hover:text-black cursor-pointer transition duration-300">
              {item}
            </li>
          ))}
        </ul>

        {/* Sign In & Sign Up */}
        <div className="flex items-center space-x-4">
          <button className="text-gray-600 text-sm hover:text-black transition duration-300">Sign in</button>
          <button className="bg-black text-white px-4 py-2 text-sm rounded-lg hover:opacity-80 transition duration-300">
            Sign up
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;


