from k8s import KubeClient
from models import KubeEnvironment, Deployment, Pod, Service


def crawl(namespace: str, client: KubeClient) -> KubeEnvironment:
    deployments = Deployment.fetch(client=client, namespace=namespace)
    pods = Pod.fetch(client=client, namespace=namespace)
    services = Service.fetch(client=client, namespace=namespace)
    return KubeEnvironment(deployments=deployments, pods=pods, services=services)
