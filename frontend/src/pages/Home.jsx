import Hero from "../components/Hero";
import UpcomingIPOs from "../components/UpcomingIPOs";
import AIInsights from "../components/AIInsights";
import Subscription from "../components/Subscription";

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Hero />
      <UpcomingIPOs />
      <AIInsights />
      <Subscription />
    </div>
  );
};

export default Home;