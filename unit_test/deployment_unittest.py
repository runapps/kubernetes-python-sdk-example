from auth.api_instance_getter import ApiInstanceGetter
from resources.deployment_examples import DeploymentExamples
from messages.deployment_message import DeploymentMessage
from resources.serviceaccount_examples import ServiceaccountExamples
import unittest


class DeplymentUnittest(unittest.TestCase):
    api_instance_appv1 = None
    api_instance_corev1 = None
    api_instance_rbac = None

    def setUp(self):
        self.api_instance_appv1 = ApiInstanceGetter().get_appv1_api_instance()
        self.api_instance_corev1 = ApiInstanceGetter().get_corev1_api_instance()
        self.api_instance_rbac = ApiInstanceGetter().get_rbac_api_instance()

        ServiceaccountExamples().create_serviceaccount(api_instance=self.api_instance_corev1,
                                                       namespace='default', name='alicek106',
                                                       image_pull_secret_name=None)

        ServiceaccountExamples().create_role_binding(api_instance=self.api_instance_rbac,
                                                     namespace='default',
                                                     sa_name='alicek106')

        secret_token = ServiceaccountExamples().get_serviceaccount_secret_token(api_instance=self.api_instance_corev1,
                                                                                namespace='default',
                                                                                name='alicek106')

        self.api_instance_appv1_custom = ApiInstanceGetter().get_appv1_api_instance(
            custom_token_auth=bytes(secret_token.data['token'], 'utf-8'))

    def test_sample_deployment(self):
        # List all deployments in namespace -> If kubernetes 1.14+, below error occurs.
        #  User \"system:serviceaccount:default:alicek106\" cannot list resource \"deployments\" in API group \"apps\" at the cluster scope"
        # deployments_all_ns = DeploymentExamples().list_deployment_all_namespace(self.api_instance_appv1_custom)
        # self.assertGreater(len((deployments_all_ns.items)), 0)

        # Create sample deployment
        result, status = DeploymentExamples().create_deployment_sample(self.api_instance_appv1_custom, DeploymentMessage('sample-deployment'))
        self.assertEqual(result['error_code'], 200)

        # Check deployment is created
        deployment_ns = DeploymentExamples().list_deployment_namespace(self.api_instance_appv1_custom, 'default')
        self.assertGreater(len((deployment_ns.items)), 0)

        # Get deployment by metadata.name (selector)
        deployment_by_selector = DeploymentExamples().list_deployment_namespace_by_selector(self.api_instance_appv1_custom, 'default', 'metadata.name=sample-deployment')
        self.assertEqual(len(deployment_by_selector.items), 1)

        # Get deployment by label
        deployment_by_selector = DeploymentExamples().list_deployment_namespace_by_label(self.api_instance_appv1_custom, 'default', 'alicek106_love_is_you=ls')
        self.assertEqual(len(deployment_by_selector.items), 1)

        result, status = DeploymentExamples().delete_deployment_sample(self.api_instance_appv1_custom, DeploymentMessage('sample-deployment'))
        self.assertEqual(result['error_code'], 200)

    def tearDown(self):
        ServiceaccountExamples().delete_role_binding(api_instance=self.api_instance_rbac,
                                                     namespace='default',
                                                     sa_name='alicek106')

        ServiceaccountExamples().delete_role(api_instance=self.api_instance_rbac,
                                             namespace="default",
                                             sa_name="alicek106")

        self.api_instance_appv1 = ApiInstanceGetter().get_appv1_api_instance()
        ServiceaccountExamples().delete_serviceaccount(api_instance=self.api_instance_corev1,
                                                       namespace='default',
                                                       name='alicek106')

if __name__ == '__main__':
    unittest.main()