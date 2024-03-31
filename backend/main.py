import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from extensions import *
from k8s import KubeEnvironment
from state import GraphState

app = FastAPI()
registered_namespace = "otel-demo"
state = GraphState()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        previous = {}
        client = KubeClient()
        await websocket.accept()
        while True:
            environment = KubeEnvironment.discover(kube_client=client, namespace=registered_namespace)
            state.update_from_env(env=environment)
            payload = state.serialize()
            if payload != previous:
                await websocket.send_json(payload)
                previous = payload
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        print("Client disconnected")
