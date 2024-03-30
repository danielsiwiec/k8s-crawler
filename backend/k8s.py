from kubernetes import client, config


class KubeClient:

    def __init__(self):
        config.load_kube_config()
        self.core_client = client.CoreV1Api()

    def list_pods(self, namespace: str):
        print("Listing pods with their IPs:")
        ret = self.core_client.list_namespaced_pod(namespace)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
