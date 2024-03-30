from kubernetes import client, config
from kubernetes.client import V1Pod, V1Deployment, V1Service


class KubeClient:

    def __init__(self):
        config.load_kube_config()
        self.core_client = client.CoreV1Api()
        self.app_client = client.AppsV1Api()

    def get_pods(self, namespace: str) -> list[V1Pod]:
        return self.core_client.list_namespaced_pod(namespace).items

    def get_deployments(self, namespace: str) -> list[V1Deployment]:
        return self.app_client.list_namespaced_deployment(namespace).items

    def get_services(self, namespace: str) -> list[V1Service]:
        return self.core_client.list_namespaced_service(namespace).items
