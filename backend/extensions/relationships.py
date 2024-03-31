from dataclasses import dataclass
from typing import Type

from base import KubeResource, get_type, KubeRelationship
from extensions.resources import Pod, Deployment, Service


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
