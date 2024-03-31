import {useEffect, useState} from "react";
import "./styles.css";
import Graph from "./Graph";
import useWebSocket from "react-use-websocket"

export default function App() {
  const [data, setData] = useState([]);

  const WS_URL = 'ws://localhost:8000/ws';

  const {lastJsonMessage} = useWebSocket(WS_URL);

  useEffect(() => {
    if (lastJsonMessage !== null) {
      setData(lastJsonMessage)
    }
  }, [lastJsonMessage]);


  return (
    <div>
      <Graph data={{nodes: data.nodes, links: data.links, types: data.types}}/>
    </div>
  );
}
