from abc import ABC, abstractmethod
from typing import TypeVar, Any

from kubernetes import client, config

from models import Node, Link


class KubeResource(ABC):
    resource: Any
    type: str

    @property
    def name(self) -> str:
        return self.resource.metadata.name

    @property
    def type(self) -> str:
        return str(self.resource.__class__.__name__)

    @property
    def id(self) -> str:
        return f'{self.type}:{self.name}'

    def to_node(self) -> Node:
        return Node(name=self.name, type=self.type, id=self.id)

    @staticmethod
    @abstractmethod
    def find(kube_client: 'KubeClient', namespace: str) -> list['KubeResource']:
        pass


class KubeRelationship(ABC):
    source: KubeResource
    target: KubeResource

    def to_link(self) -> Link:
        return Link(source=self.source.id, target=self.target.id)

    @staticmethod
    @abstractmethod
    def find(resources: list[KubeResource]) -> list['KubeRelationship']:
        pass


class KubeClient:

    def __init__(self):
        config.load_kube_config()
        self.core_client = client.CoreV1Api()
        self.app_client = client.AppsV1Api()


T = TypeVar('T', bound=KubeResource)


def get_type(resources: list[KubeResource], cls: T) -> list[T]:
    return [resource for resource in resources if cls.__args__[0] == resource.__class__]
