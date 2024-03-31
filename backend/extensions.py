from dataclasses import dataclass
from typing import Type

from kubernetes.client import V1Pod, V1Service, V1Deployment

from base import KubeResource, KubeClient, get_type, KubeRelationship


@dataclass
class Pod(KubeResource):
    type = 'pod'
    resource: V1Pod

    @staticmethod
    def find(kube_client: KubeClient, namespace: str) -> list['Pod']:
        return [Pod(resource=item) for item in kube_client.core_client.list_namespaced_pod(namespace).items]


@dataclass
class Deployment(KubeResource):
    type = 'deployment'
    resource: V1Deployment

    @staticmethod
    def find(kube_client: KubeClient, namespace: str) -> list['Deployment']:
        return [Deployment(resource=item) for item in kube_client.app_client.list_namespaced_deployment(namespace).items]


@dataclass
class Service(KubeResource):
    type = 'service'
    resource: V1Service

    @staticmethod
    def find(kube_client: KubeClient, namespace: str):
        return [Service(resource=item) for item in kube_client.core_client.list_namespaced_service(namespace).items]


@dataclass
class PodToDeployment(KubeRelationship):
    source: Pod
    target: Deployment

    @staticmethod
    def find(resources: list[KubeResource]) -> list['PodToDeployment']:
        relationships: list[PodToDeployment] = []

        for deployment in get_type(resources, Type[Deployment]):
            relationships += [PodToDeployment(source=pod, target=deployment) for pod in get_type(resources, Type[Pod]) if PodToDeployment.__pod_matches_deployment(pod, deployment)]

        return relationships

    @staticmethod
    def __pod_matches_deployment(pod: Pod, deployment: Deployment) -> bool:
        return all(pod.resource.metadata.labels.get(key, None) == val for key, val in deployment.resource.spec.template.metadata.labels.items())


@dataclass
class ServiceToPod(KubeRelationship):
    source: Pod
    target: Service

    @staticmethod
    def find(resources: list[KubeResource]) -> list['ServiceToPod']:
        relationships: list[ServiceToPod] = []

        for service in get_type(resources, Type[Service]):
            relationships += [ServiceToPod(source=pod, target=service) for pod in get_type(resources, Type[Pod]) if ServiceToPod.__pod_matches_service(pod, service)]

        return relationships

    @staticmethod
    def __pod_matches_service(pod: Pod, service: Service) -> bool:
        return all(pod.resource.metadata.labels.get(key, None) == val for key, val in service.resource.spec.selector.items())
