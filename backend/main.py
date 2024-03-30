from fastapi import FastAPI
from k8s import KubeClient
from state import GraphState
import threading

app = FastAPI()
registered_namespace = "otel-demo"
state = GraphState()


@app.get("/api/graph")
async def read_item():
    return state.graph


def start_crawler():
    state.graph = [
        {
            "source": "Microsoft",
            "target": "Amazon",
            "type": "licensing",
        },
        {
            "source": "Microsoft",
            "target": "HTC",
            "type": "licensing",
        },
        {
            "source": "Samsung",
            "target": "Apple",
            "type": "suit",
        },
        {
            "source": "Motorola",
            "target": "Apple",
            "type": "suit",
        },
        {
            "source": "NXD",
            "target": "Tesla",
            "type": "suit",
        },
        {
            "source": "NXD",
            "target": "Apple",
            "type": "suit",
        },
    ]


crawler_thread = threading.Thread(target=start_crawler)
crawler_thread.start()

# client = KubeClient()
# client.list_pods(namespace=registered_namespace)
