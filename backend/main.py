import threading
import time

from fastapi import FastAPI

from crawler import crawl
from k8s import KubeClient
from state import GraphState

app = FastAPI()
registered_namespace = "otel-demo"
state = GraphState()


@app.get("/api/graph")
async def read_item():
    return state.serialize()


def start_crawler():
    client = KubeClient()
    while True:
        environment = crawl(namespace=registered_namespace, client=client)
        state.update_from_env(env=environment)
        time.sleep(5)


crawler_thread = threading.Thread(target=start_crawler)
crawler_thread.start()
