from dataclasses import dataclass

from kubernetes.client import V1Pod, V1Service, V1Deployment


@dataclass
class Node:
    id: str
    name: str
    type: str


@dataclass
class Link:
    source: str
    target: str


class KubeEnvironment:
    pods: list[V1Pod]
    services: list[V1Service]
    deployments: list[V1Deployment]

    def __init__(self, pods, services, deployments):
        self.pods = pods
        self.services = services
        self.deployments = deployments

    def to_nodes(self):
        pod_nodes = [{
            'name': pod.metadata.name,
            'type': 'pod',
            'id': f'pod:{pod.metadata.name}'
        } for pod in self.pods]

        service_nodes = [{
            'name': service.metadata.name,
            'type': 'service',
            'id': f'service:{service.metadata.name}'
        } for service in self.services]

        deployment_nodes = [{
            'name': deployment.metadata.name,
            'type': 'deployment',
            'id': f'deployment:{deployment.metadata.name}'
        } for deployment in self.deployments]

        return pod_nodes + service_nodes + deployment_nodes

    def to_links(self) -> list[Link]:
        pod_service_links: list[Link] = []

        for service in self.services:
            linked_pods = [pod for pod in self.pods if self.__pod_matches_service(pod, service)]
            links = [Link(source=f'pod:{pod.metadata.name}', target=f'service:{service.metadata.name}') for pod in linked_pods]
            pod_service_links += links

        pod_deployment_links: list[Link] = []

        for deployment in self.deployments:
            linked_pods = [pod for pod in self.pods if self.__pod_matches_deployment(pod, deployment)]
            links = [Link(source=f'pod:{pod.metadata.name}', target=f'deployment:{deployment.metadata.name}') for pod in linked_pods]
            pod_deployment_links += links

        return pod_service_links + pod_deployment_links

    @staticmethod
    def __pod_matches_service(pod: V1Pod, service: V1Service) -> bool:
        return all(pod.metadata.labels.get(key, None) == val for key, val in service.spec.selector.items())

    @staticmethod
    def __pod_matches_deployment(pod: V1Pod, deployment: V1Deployment) -> bool:
        return all(pod.metadata.labels.get(key, None) == val for key, val in deployment.spec.template.metadata.labels.items())
