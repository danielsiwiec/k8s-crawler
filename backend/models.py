from abc import ABC, abstractmethod
from dataclasses import dataclass

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

    @abstractmethod
    def to_node(self) -> Node:
        pass

    @abstractmethod
    def id(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def fetch(client: KubeClient, namespace: str) -> list['KubeResource']:
        pass


@dataclass
class Pod(KubeResource):
    resource: V1Pod

    @staticmethod
    def fetch(client: KubeClient, namespace: str) -> list['Pod']:
        return [Pod(resource=item) for item in client.core_client.list_namespaced_pod(namespace).items]

    def to_node(self) -> Node:
        return Node(name=self.resource.metadata.name, type='pod', id=f'pod:{self.resource.metadata.name}')

    def id(self) -> str:
        return f'pod:{self.resource.metadata.name}'


@dataclass
class Deployment(KubeResource):
    resource: V1Deployment

    @staticmethod
    def fetch(client: KubeClient, namespace: str) -> list['Deployment']:
        return [Deployment(resource=item) for item in client.app_client.list_namespaced_deployment(namespace).items]

    def to_node(self) -> Node:
        return Node(name=self.resource.metadata.name, type='deployment', id=f'deployment:{self.resource.metadata.name}')

    def id(self) -> str:
        return f'deployment:{self.resource.metadata.name}'


@dataclass
class Service(KubeResource):
    resource: V1Service

    @staticmethod
    def fetch(client: KubeClient, namespace: str) -> list['Service']:
        return [Service(resource=item) for item in client.core_client.list_namespaced_service(namespace).items]

    def to_node(self) -> Node:
        return Node(name=self.resource.metadata.name, type='service', id=f'service:{self.resource.metadata.name}')

    def id(self) -> str:
        return f'service:{self.resource.metadata.name}'


class Relationship(ABC):
    source: KubeResource
    target: KubeResource

    def to_link(self) -> Link:
        return Link(source=self.source.id(), target=self.target.id())

    @staticmethod
    @abstractmethod
    def find(env: 'KubeEnvironment') -> list['KubeResource']:
        pass


@dataclass
class PodToDeployment(Relationship):
    source: Pod
    target: Deployment

    @staticmethod
    def find(env: 'KubeEnvironment') -> list['PodToDeployment']:
        pod_deployment_links: list[PodToDeployment] = []

        for deployment in env.deployments:
            matched_pods = [PodToDeployment(source=pod, target=deployment) for pod in env.pods if PodToDeployment.__pod_matches_deployment(pod, deployment)]
            pod_deployment_links += matched_pods

        return pod_deployment_links

    @staticmethod
    def __pod_matches_deployment(pod: Pod, deployment: Deployment) -> bool:
        return all(pod.resource.metadata.labels.get(key, None) == val for key, val in deployment.resource.spec.template.metadata.labels.items())


@dataclass
class ServiceToPod(Relationship):
    source: Pod
    target: Service

    @staticmethod
    def find(env: 'KubeEnvironment') -> list['ServiceToPod']:
        pod_service_links: list[ServiceToPod] = []

        for service in env.services:
            matched_pods = [ServiceToPod(source=pod, target=service) for pod in env.pods if ServiceToPod.__pod_matches_service(pod, service)]
            pod_service_links += matched_pods

        return pod_service_links

    @staticmethod
    def __pod_matches_service(pod: Pod, service: Service) -> bool:
        return all(pod.resource.metadata.labels.get(key, None) == val for key, val in service.resource.spec.selector.items())


@dataclass
class KubeEnvironment:
    pods: list[Pod]
    services: list[Service]
    deployments: list[Deployment]

    def resource(self) -> list[KubeResource]:
        return self.pods + self.services + self.deployments

    def relationships(self) -> list[Relationship]:
        return ServiceToPod.find(self) + PodToDeployment.find(self)