from k8s import KubeClient
from models import KubeEnvironment


def crawl(namespace: str, client: KubeClient) -> KubeEnvironment:
    deployments = client.get_deployments(namespace)
    pods = client.get_pods(namespace)
    services = client.get_services(namespace)
    return KubeEnvironment(deployments=deployments, pods=pods, services=services)