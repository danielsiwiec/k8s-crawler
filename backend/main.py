import threading
import time

from fastapi import FastAPI

from k8s import KubeEnvironment
from extensions import *
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
        environment = KubeEnvironment.discover(kube_client=client, namespace=registered_namespace)
        state.update_from_env(env=environment)
        time.sleep(5)


crawler_thread = threading.Thread(target=start_crawler)
crawler_thread.start()
