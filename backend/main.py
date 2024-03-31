import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi_utils.tasks import repeat_every

from extensions import *
from k8s import KubeEnvironment
from state import GraphState

app = FastAPI()
registered_namespace = "otel-demo"
state = GraphState()
client = KubeClient()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        previous = {}

        await websocket.accept()
        while True:
            payload = state.serialize()
            if payload != previous:
                await websocket.send_json(payload)
                previous = payload
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("Client disconnected")


@app.get("/api/graph")
async def read_item():
    return state.serialize()


@app.on_event("startup")
@repeat_every(seconds=2)  # 1 hour
def remove_expired_tokens_task() -> None:
    environment = KubeEnvironment.discover(kube_client=client, namespace=registered_namespace)
    state.update_from_env(env=environment)
