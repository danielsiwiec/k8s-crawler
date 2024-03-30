from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Type, TypeVar

from kubernetes import client, config
from kubernetes.client import V1Pod, V1Service, V1Deployment

from models import Node, Link


class KubeClient:

    def __init__(self):
        config.load_kube_config()
        self.core_client = client.CoreV1Api()
        self.app_client = client.AppsV1Api()


class KubeResource(ABC):

    def to_node(self) -> Node:
        return Node(name=self.name(), type=self.type(), id=self.id())

    def id(self) -> str:
        return f'{self.type()}:{self.name()}'

    @abstractmethod
    def name(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def type() -> str:
        pass

    @staticmethod
    @abstractmethod
    def find(kube_client: KubeClient, namespace: str) -> list['KubeResource']:
        pass


@dataclass
class Pod(KubeResource):
    resource: V1Pod

    @staticmethod
    def find(kube_client: KubeClient, namespace: str) -> list['Pod']:
        return [Pod(resource=item) for item in kube_client.core_client.list_namespaced_pod(namespace).items]

    def name(self) -> str:
        return self.resource.metadata.name

    @staticmethod
    def type() -> str:
        return 'pod'


@dataclass
class Deployment(KubeResource):
    resource: V1Deployment

    @staticmethod
    def find(kube_client: KubeClient, namespace: str) -> list['Deployment']:
        return [Deployment(resource=item) for item in kube_client.app_client.list_namespaced_deployment(namespace).items]

    def name(self) -> str:
        return self.resource.metadata.name

    @staticmethod
    def type() -> str:
        return 'deployment'


@dataclass
class Service(KubeResource):
    resource: V1Service

    @staticmethod
    def find(kube_client: KubeClient, namespace: str):
        return [Service(resource=item) for item in kube_client.core_client.list_namespaced_service(namespace).items]

    def name(self) -> str:
        return self.resource.metadata.name

    @staticmethod
    def type() -> str:
        return 'service'


class KubeRelationship(ABC):
    source: KubeResource
    target: KubeResource

    def to_link(self) -> Link:
        return Link(source=self.source.id(), target=self.target.id())

    @staticmethod
    @abstractmethod
    def find(resources: list[KubeResource]) -> list['KubeRelationship']:
        pass


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


@dataclass
class KubeEnvironment:
    resources: list[KubeResource] = field(default_factory=list)
    relationships: list[KubeRelationship] = field(default_factory=list)

    @staticmethod
    def discover(kube_client: KubeClient, namespace: str) -> 'KubeEnvironment':

        resources: list[KubeResource] = []
        for resource_type in KubeResource.__subclasses__():
            resources.extend(resource_type.find(kube_client=kube_client, namespace=namespace))

        relationships: list[KubeRelationship] = []
        for relationship_type in KubeRelationship.__subclasses__():
            relationships.extend(relationship_type.find(resources))

        return KubeEnvironment(resources=resources, relationships=relationships)


T = TypeVar('T', bound=KubeResource)


def get_type(resources: list[KubeResource], cls: T) -> list[T]:
    return [resource for resource in resources if cls.__args__[0] == resource.__class__]
