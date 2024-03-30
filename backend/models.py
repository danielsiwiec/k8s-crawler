from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import cast

from kubernetes.client import V1Pod, V1Service, V1Deployment

from k8s import KubeClient


@dataclass
class Node:
    id: str
    name: str
    type: str


@dataclass
class Link:
    source: str
    target: str


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
    def find(client: KubeClient, namespace: str) -> list['KubeResource']:
        pass


@dataclass
class Pod(KubeResource):
    resource: V1Pod

    @staticmethod
    def find(client: KubeClient, namespace: str) -> list['Pod']:
        return [Pod(resource=item) for item in client.core_client.list_namespaced_pod(namespace).items]

    def name(self) -> str:
        return self.resource.metadata.name

    @staticmethod
    def type() -> str:
        return 'pod'

    @staticmethod
    def get_from(resources: list[KubeResource]) -> list['Pod']:
        return [cast('Pod', resource) for resource in resources if resource.type() == Pod.type()]


@dataclass
class Deployment(KubeResource):
    resource: V1Deployment

    @staticmethod
    def find(client: KubeClient, namespace: str) -> list['Deployment']:
        return [Deployment(resource=item) for item in client.app_client.list_namespaced_deployment(namespace).items]

    def name(self) -> str:
        return self.resource.metadata.name

    @staticmethod
    def get_from(resources: list[KubeResource]) -> list['Deployment']:
        return [cast('Deployment', resource) for resource in resources if resource.type() == Deployment.type()]

    @staticmethod
    def type() -> str:
        return 'deployment'


@dataclass
class Service(KubeResource):
    resource: V1Service

    @staticmethod
    def find(client: KubeClient, namespace: str):
        return [Service(resource=item) for item in client.core_client.list_namespaced_service(namespace).items]

    def name(self) -> str:
        return self.resource.metadata.name

    @staticmethod
    def get_from(resources: list[KubeResource]) -> list['Service']:
        return [cast('Service', resource) for resource in resources if resource.type() == Service.type()]

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

        for deployment in Deployment.get_from(resources):
            relationships += [PodToDeployment(source=pod, target=deployment) for pod in Pod.get_from(resources) if PodToDeployment.__pod_matches_deployment(pod, deployment)]

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

        for service in Service.get_from(resources):
            relationships += [ServiceToPod(source=pod, target=service) for pod in Pod.get_from(resources) if ServiceToPod.__pod_matches_service(pod, service)]

        return relationships

    @staticmethod
    def __pod_matches_service(pod: Pod, service: Service) -> bool:
        return all(pod.resource.metadata.labels.get(key, None) == val for key, val in service.resource.spec.selector.items())


@dataclass
class KubeEnvironment:
    resources: list[KubeResource] = field(default_factory=list)
    relationships: list[KubeRelationship] = field(default_factory=list)

    @staticmethod
    def discover(client: KubeClient, namespace: str) -> 'KubeEnvironment':

        resources: list[KubeResource] = []
        for resource_type in KubeResource.__subclasses__():
            resources.extend(resource_type.find(client=client, namespace=namespace))

        relationships: list[KubeRelationship] = []
        for relationship_type in KubeRelationship.__subclasses__():
            relationships.extend(relationship_type.find(resources))

        return KubeEnvironment(resources=resources, relationships=relationships)
