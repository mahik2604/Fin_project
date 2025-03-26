// Subscription.jsx
const Subscription = () => {
    return (
      <section className="py-12 text-center">
        <h2 className="text-3xl font-bold text-gray-900">Stay Updated</h2>
        <p className="mt-2 text-gray-700">Subscribe for IPO updates via Email or WhatsApp</p>
        <div className="mt-6 flex flex-col md:flex-row justify-center gap-4">
          <input type="email" placeholder="Enter your email" className="p-2 border rounded-lg" />
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg">Subscribe</button>
        </div>
      </section>
    );
  };
  
  export default Subscription;