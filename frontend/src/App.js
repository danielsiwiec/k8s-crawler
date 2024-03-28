import * as d3 from "d3";
import {useEffect, useState} from "react";
import "./styles.css";
import Graph from "./Graph";

export default function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/graph')
      .then((res) => {
        return res.json()
      })
      .then((data) => {
        console.log(data)
        setData(data)
      })
  }, []);

  return (
    <div>
      <Graph graph={data} />
    </div>
  );
}
