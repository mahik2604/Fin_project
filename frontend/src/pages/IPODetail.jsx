import { useParams } from "react-router-dom";

const IPODetail = () => {
  const { id } = useParams();
  return <div>Details of IPO: {id}</div>;
};

export default IPODetail;
