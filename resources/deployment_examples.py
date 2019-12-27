from auth.api_instance_getter import ApiInstanceGetter
from kubernetes import client
from messages.general_error import GeneralError
from messages.deployment_message import DeploymentMessage
from kubernetes.client.rest import ApiException
import json


class DeploymentExamples():

    # List Deployment Object
    def list_deployment_all_namespace(self, api_instance):
        result = api_instance.list_deployment_for_all_namespaces()
        return result

    def list_deployment_namespace(self, api_instance, namespace):
        result = api_instance.list_namespaced_deployment(namespace)
        return result

    def list_deployment_namespace_by_selector(self, api_instance, namespace, selector):
        result = api_instance.list_namespaced_deployment(namespace=namespace, field_selector=selector, limit=5)
        return result

    def list_deployment_namespace_by_label(self, api_instance, namespace, label):
        result = api_instance.list_namespaced_deployment(namespace=namespace, label_selector=label, limit=5)
        return result

    # Create Deployment Object From Sample Data
    def create_deployment_sample(self, api_instance, deployment_sample_data):
        labels = {'alicek106_love_is_you': 'ls'} # Default Label for matching ReplicaSets
        labels.update(deployment_sample_data.labels)

        env_vars = [client.V1EnvVar(name=env['name'], value=env['value']) for env in deployment_sample_data.env_vars]
        publish_ports = [client.V1ContainerPort(name=port['name'], container_port=int(port['port'])) for port in deployment_sample_data.publish_ports]

        metadata = client.V1ObjectMeta(
            namespace=deployment_sample_data.namespace,
            name=deployment_sample_data.deployment_name,
            labels=labels)

        spec_pod = client.V1PodSpec(
            containers=[
                client.V1Container(
                    name=deployment_sample_data.deployment_name,
                    image=deployment_sample_data.image,
                    env=env_vars,
                    ports=publish_ports,
                    image_pull_policy="Always",
                    resources=client.V1ResourceRequirements(
                        limits=deployment_sample_data.resources['limit'],
                        requests=deployment_sample_data.resources['request']
                    )
                )
            ]
        )

        spec_deployment = client.V1DeploymentSpec(
            replicas=deployment_sample_data.replicas,
            selector=client.V1LabelSelector(
                match_labels={'alicek106_love_is_you': 'ls'},  # Default Label for matching ReplicaSets
            ),

            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=spec_pod
            )
        )

        deployment_body = client.AppsV1beta1Deployment(
            kind='Deployment',
            metadata=metadata,
            spec=spec_deployment
        )

        try:
            api_instance.create_namespaced_deployment(namespace=deployment_sample_data.namespace, body=deployment_body)
            return GeneralError(200, 'success').serialize(), 200
        except ApiException as e:
            error = json.loads(e.body)
            return GeneralError(409, 'Reason: %s, %s' % (error['reason'], error['message'])).serialize(), 409

    def delete_deployment_sample(self, api_instance, deployment_sample_data):
        deleteOptions = client.V1DeleteOptions()  # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1DeleteOptions.md
        try:
            api_response = api_instance.delete_namespaced_deployment(
                name=deployment_sample_data.deployment_name,
                namespace=deployment_sample_data.namespace,
                body=deleteOptions
            )
            return GeneralError(200, 'success').serialize(), 200
        except ApiException as e:
            error = json.loads(e.body)
            return GeneralError(e.status, 'Reason: %s, %s' % (error['reason'], error['message'])).serialize(), e.status


if __name__ == '__main__':
    api_instance = ApiInstanceGetter().get_appv1_api_instance()
    api_instance.delete_namespaced_deployment()
    print(DeploymentExamples().list_deployment_all_namespace(api_instance))
