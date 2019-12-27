from kubernetes import client
from auth.api_instance_getter import ApiInstanceGetter
import time
import hashlib

# Admission Controller for Service Account should be activated.
class ServiceaccountExamples():
    def create_serviceaccount(self, api_instance, namespace, name, image_pull_secret_name=None):
        body = client.V1ServiceAccount(api_version='v1',
                                       kind='ServiceAccount',
                                       metadata=client.V1ObjectMeta(name=name, namespace=namespace),
                                       automount_service_account_token=True,
                                       image_pull_secrets=image_pull_secret_name if image_pull_secret_name is None else
                                       [client.V1LocalObjectReference(name=image_pull_secret_name)])
        result = api_instance.create_namespaced_service_account(namespace, body)
        return result

    def get_serviceaccount_secret_token(self, api_instance, namespace, name):
        """ Wait for creation of secret """
        while True:
            try:
                """ exact and export will be removed in 1.18 (currently, deprecated) """
                serviceaccount_response = api_instance.read_namespaced_service_account(name=name, namespace=namespace,
                                                                                       exact=True, export=True)
                if serviceaccount_response.secrets != None:
                    secret_response = api_instance.read_namespaced_secret(name=serviceaccount_response.secrets[0].name,
                                                                      namespace=namespace, exact=True, export=True)
                    return secret_response
            except Exception as e:
                time.sleep(1)
                continue

    def delete_serviceaccount(self, api_instance, namespace, name):
        result = api_instance.delete_namespaced_service_account(namespace=namespace, name=name,
                                                       body=client.V1DeleteOptions(), grace_period_seconds=10)
        return result

    def create_role_binding(self, api_instance, namespace, sa_name):
        role_name = hashlib.sha1(str.encode(sa_name)).hexdigest()[:8]  # $ID-role trigger bug! HaHa
        binding_name = "{}-binding".format(role_name)

        body = client.V1Role(api_version='rbac.authorization.k8s.io/v1',
                             kind='Role',
                             metadata=client.V1ObjectMeta(name=role_name, namespace=namespace),
                             rules=[client.V1PolicyRule(api_groups=['*'], resources=['*'], verbs=['*'])])
        api_instance.create_namespaced_role(namespace=namespace, body=body)

        role_binding = client.V1RoleBinding(
            metadata=client.V1ObjectMeta(namespace=namespace, name=binding_name),
            subjects=[client.V1Subject(name=sa_name, kind="ServiceAccount", api_group="")],
            role_ref=client.V1RoleRef(kind="Role", api_group="rbac.authorization.k8s.io",
                                      name=role_name))
        api_instance.create_namespaced_role_binding(namespace=namespace, body=role_binding)

    def delete_role_binding(self, api_instance, namespace, sa_name):
        role_name = hashlib.sha1(str.encode(sa_name)).hexdigest()[:8]  # $ID-role trigger bug! HaHa
        binding_name = "{}-binding".format(role_name)
        api_instance.delete_namespaced_role_binding(name=binding_name, namespace=namespace, body=client.V1DeleteOptions())

    def delete_role(self, api_instance, namespace, sa_name):
        role_name = hashlib.sha1(str.encode(sa_name)).hexdigest()[:8]  # $ID-role trigger bug! HaHa
        api_instance.delete_namespaced_role(name=role_name, namespace=namespace, body=client.V1DeleteOptions())


if __name__ == '__main__':
    api_instance = ApiInstanceGetter().get_corev1_api_instance()
    ServiceaccountExamples().create_serviceaccount(api_instance=api_instance, namespace='default', name='alicek106', image_pull_secret_name=None)

    api_rbac_instance = ApiInstanceGetter().get_rbac_api_instance()
    ServiceaccountExamples().create_role_binding(api_instance=api_rbac_instance, namespace='default',sa_name='alicek106')

    api_rbac_instance = ApiInstanceGetter().get_rbac_api_instance()
    ServiceaccountExamples().delete_role_binding(api_instance=api_rbac_instance, namespace='default',sa_name='alicek106')
    ServiceaccountExamples().delete_role(api_instance=api_rbac_instance, namespace="default", sa_name="alicek106")

    serviceaccount_info = ServiceaccountExamples().get_serviceaccount_secret_token(api_instance=api_instance, namespace='default', name='alicek106')
    ServiceaccountExamples().delete_serviceaccount(api_instance=api_instance, namespace='default', name='alicek106')
