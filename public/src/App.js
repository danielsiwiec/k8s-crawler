import * as d3 from "d3";
import { useState } from "react";
import "./styles.css";
import Graph from "./Graph";

export default function App() {
  const [data, setData] = useState(() => d3.ticks(-2, 2, 200).map(Math.sin));

  const suits = [
    {
      source: "Microsoft",
      target: "Amazon",
      type: "licensing",
    },
    {
      source: "Microsoft",
      target: "HTC",
      type: "licensing",
    },
    {
      source: "Samsung",
      target: "Apple",
      type: "suit",
    },
    {
      source: "Motorolla",
      target: "Apple",
      type: "suit",
    },
  ];

  return (
    <div>
      <Graph suits={suits} />
    </div>
  );
}
