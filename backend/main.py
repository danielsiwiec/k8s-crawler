from fastapi import FastAPI
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
    state.nodes = [
        {
            'name': 'pod-foo',
            'type': 'pod',
            'id': 'pod:pod-foo'
        },
        {
            'name': 'pod-bar',
            'type': 'pod',
            'id': 'pod:pod-bar'
        },
        {
            'name': 'service-foo',
            'type': 'service',
            'id': 'service:service-foo'
        },
        {
            'name': 'service-bar',
            'type': 'service',
            'id': 'service:service-bar'
        },
        {
            'name': 'depl-foo',
            'type': 'deployment',
            'id': 'deployment:deployment-foo'
        },
        {
            'name': 'depl-bar',
            'type': 'deployment',
            'id': 'deployment:deployment-bar'
        },
        {
            'name': 'depl-baz',
            'type': 'deployment',
            'id': 'deployment:deployment-baz'
        },
    ]

    state.links = [
        {
            'source': 'deployment:deployment-foo',
            'target': 'pod:pod-foo'
        },
        {
            'source': 'service:service-foo',
            'target': 'pod:pod-foo'
        },
        {
            'source': 'deployment:deployment-bar',
            'target': 'pod:pod-bar'
        },
        {
            'source': 'service:service-bar',
            'target': 'pod:pod-bar'
        }
    ]

    state.types = {i['type'] for i in state.nodes}


crawler_thread = threading.Thread(target=start_crawler)
crawler_thread.start()

# client = KubeClient()
# client.list_pods(namespace=registered_namespace)
