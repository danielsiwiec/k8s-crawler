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

  // const nodes = Array.from(
  //   new Set(data.flatMap((l) => [l.source, l.target])),
  //   (id) => ({id})
  // )
  //
  // const links = data.map((d) => Object.create(d));
  // const types = Array.from(new Set(data.map((d) => d.type)));

  return (
    <div>
      <Graph data={{nodes: data.nodes, links: data.links, types: data.types}} />
    </div>
  );
}
