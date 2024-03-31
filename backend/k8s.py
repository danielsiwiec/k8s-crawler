from dataclasses import field, dataclass

from base import KubeResource, KubeRelationship, KubeClient


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
