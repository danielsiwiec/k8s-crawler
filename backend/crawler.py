from k8s import KubeClient
from models import KubeEnvironment, KubeResource, KubeRelationship


def crawl(namespace: str, client: KubeClient) -> KubeEnvironment:
    env = KubeEnvironment()
    for subclass in KubeResource.__subclasses__():
        subclass.fetch_into(client=client, namespace=namespace, env=env)

    for subclass in KubeRelationship.__subclasses__():
        subclass.fetch_into(env=env)

    return env
