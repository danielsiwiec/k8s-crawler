import time
from dataclasses import asdict

from fastapi import FastAPI

from crawler import crawl
from k8s import KubeClient
from state import GraphState
import threading

app = FastAPI()
registered_namespace = "otel-demo"
state = GraphState()


@app.get("/api/graph")
async def read_item():
    return {
        'nodes': state.nodes,
        'links': state.links,
        'types': state.types
    }


def start_crawler():
    client = KubeClient()
    while True:
        environment = crawl(namespace=registered_namespace, client=client)
        state.nodes = environment.to_nodes()

        state.links = [asdict(i) for i in environment.to_links()]
        state.types = {i['type'] for i in state.nodes}
        time.sleep(5)


crawler_thread = threading.Thread(target=start_crawler)
crawler_thread.start()
