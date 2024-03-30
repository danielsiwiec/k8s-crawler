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
            'name': 'foo',
            'type': 'pod',
            'id': 'pod:foo'
        },
        {
            'name': 'bar',
            'type': 'pod',
            'id': 'pod:bar'
        },
        {
            'name': 'foo',
            'type': 'service',
            'id': 'service:foo'
        },
        {
            'name': 'bar',
            'type': 'service',
            'id': 'service:bar'
        },
        {
            'name': 'foo',
            'type': 'deployment',
            'id': 'deployment:foo'
        },
        {
            'name': 'bar',
            'type': 'deployment',
            'id': 'deployment:bar'
        },
        {
            'name': 'baz',
            'type': 'deployment',
            'id': 'deployment:baz'
        },
    ]

    state.links = [
        {
            'source': 'deployment:foo',
            'target': 'pod:foo'
        },
        {
            'source': 'service:foo',
            'target': 'pod:foo'
        },
        {
            'source': 'deployment:bar',
            'target': 'pod:bar'
        },
        {
            'source': 'service:bar',
            'target': 'pod:bar'
        }
    ]

    state.types = {i['type'] for i in state.nodes}


crawler_thread = threading.Thread(target=start_crawler)
crawler_thread.start()

# client = KubeClient()
# client.list_pods(namespace=registered_namespace)
