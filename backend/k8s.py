from kubernetes import client, config


class KubeClient:

    def __init__(self):
        config.load_kube_config()
        self.core_client = client.CoreV1Api()
        self.app_client = client.AppsV1Api()
