from k8s import KubeClient
from models import KubeEnvironment, Deployment, Pod, Service


def crawl(namespace: str, client: KubeClient) -> KubeEnvironment:
    env = KubeEnvironment()
    Deployment.fetch_into(client=client, namespace=namespace, env=env)
    Pod.fetch_into(client=client, namespace=namespace, env=env)
    Service.fetch_into(client=client, namespace=namespace, env=env)
    return env
