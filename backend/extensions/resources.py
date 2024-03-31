from dataclasses import dataclass

from kubernetes.client import V1Pod, V1Service, V1Deployment

from base import KubeResource, KubeClient


@dataclass
class Pod(KubeResource):
    resource: V1Pod

    @staticmethod
    def find(kube_client: KubeClient, namespace: str) -> list['Pod']:
        return [Pod(resource=item) for item in kube_client.core_client.list_namespaced_pod(namespace).items]


@dataclass
class Deployment(KubeResource):
    resource: V1Deployment

    @staticmethod
    def find(kube_client: KubeClient, namespace: str) -> list['Deployment']:
        return [Deployment(resource=item) for item in kube_client.app_client.list_namespaced_deployment(namespace).items]


@dataclass
class Service(KubeResource):
    resource: V1Service

    @staticmethod
    def find(kube_client: KubeClient, namespace: str):
        return [Service(resource=item) for item in kube_client.core_client.list_namespaced_service(namespace).items]
