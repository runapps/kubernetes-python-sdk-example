from auth.api_instance_getter import ApiInstanceGetter
from resources.serviceaccount_examples import ServiceaccountExamples
import unittest


class ServiceaccountUnittest(unittest.TestCase):
    api_instance = None

    def setUp(self):
        self.api_instance = ApiInstanceGetter().get_corev1_api_instance()

    def test_sample_serviceaccount(self):
        ServiceaccountExamples().create_serviceaccount(api_instance=self.api_instance, namespace='default', name='alicek106')
        serviceaccount_info = ServiceaccountExamples().get_serviceaccount_secret_token(api_instance=self.api_instance,
                                                                            namespace='default', name='alicek106')
        ServiceaccountExamples().delete_serviceaccount(api_instance=self.api_instance, namespace='default', name='alicek106')

if __name__ == '__main__':
    unittest.main()