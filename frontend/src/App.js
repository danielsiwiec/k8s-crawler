import {useEffect, useState} from "react";
import "./styles.css";
import Graph from "./Graph";

export default function App() {
  const [data, setData] = useState([]);

  const getGraph = async () => {
    const res = await fetch('/api/graph')
    const data = await res.json()
    setData(data)
  }

  useEffect(() => {
    const timer = setInterval(getGraph, 3000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div>
      <Graph data={{nodes: data.nodes, links: data.links, types: data.types}} />
    </div>
  );
}
