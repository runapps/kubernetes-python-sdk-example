from __future__ import print_function
from auth.auth_parser import AuthParser
import urllib3, base64, os
from kubernetes import client, config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiInstanceGetter:
    auth_parser = AuthParser()
    auth_type = auth_parser.get_auth_type()

    def __set_default_auth(self):


        if self.auth_type == self.auth_parser.IN_CLUSTER_POD_AUTH:
            config.load_incluster_config()

        else:
            configuration = client.Configuration()
            configuration.host = self.auth_parser.kube_api_server_ip
            configuration.verify_ssl = False  # can be True with ca.crt issued by Kubernetes

            if self.auth_type == self.auth_parser.SERVICE_ACCOUNT_TOKEN_AUTH:
                configuration.api_key = {"authorization": "Bearer " + base64.decodebytes(str.encode(self.auth_parser.service_account_token)).decode()}

            elif self.auth_type == self.auth_parser.CERTIFICATE_AUTH:
                configuration.cert_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.auth_parser.cert_file_name)
                configuration.key_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),  self.auth_parser.cert_key_file_name)

            client.Configuration.set_default(configuration)

    def __get_custom_token_auth(self, token):
        configuration = client.Configuration()
        """
        If you are developing in local IDE, you can use self.auth_parser.kube_api_server_ip for remote connect.
        But if not, (If you deploy pod in kubernetes) just use Environment Variable :D
        """
        # configuration.host = self.auth_parser.kube_api_server_ip
        configuration.host = 'https://kubernetes' #'https://' + os.environ['KUBERNETES_SERVICE_HOST']
        configuration.verify_ssl = False  # can be True with ca.crt issued by Kubernetes
        configuration.api_key = {"authorization": "Bearer " + base64.decodebytes(token).decode()}
        client.Configuration.set_default(configuration)

    def get_appv1_api_instance(self, custom_token_auth=None):
        if custom_token_auth == None:
            """ Use default auth mounted into pod """
            self.__set_default_auth()
        else:
            self.__get_custom_token_auth(custom_token_auth)

        return client.AppsV1Api()

    def get_corev1_api_instance(self, custom_token_auth=None):
        if custom_token_auth == None:
            """ Use default auth mounted into pod """
            self.__set_default_auth()
        else:
            self.__get_custom_token_auth(custom_token_auth)
        return client.CoreV1Api()

    def get_rbac_api_instance(self, custom_token_auth=None):
        if custom_token_auth == None:
            """ Use default auth mounted into pod """
            self.__set_default_auth()
        else:
            self.__get_custom_token_auth(custom_token_auth)
        return client.RbacAuthorizationV1Api()


    def getApiInstance(self, decodedToken):
        configuration = client.Configuration()
        configuration.host = ("https://" + os.environ['KUBERNETES_PORT_443_TCP_ADDR'])
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + base64.decodebytes(str.encode(decodedToken)).decode()}
        client.Configuration.set_default(configuration)
        v1 = client.AppsV1Api(client.ApiClient(configuration))
        return v1


#
# from auth.api_instance_getter import ApiInstanceGetter
# from resources.deployment_examples import DeploymentExamples
# from messages.deployment_message import DeploymentMessage
# from resources.serviceaccount_examples import ServiceaccountExamples
# import unittest
#
#
# if __name__ == "__main__":
#     # default
#     decodedTokenA = 'ZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNklpSjkuZXlKcGMzTWlPaUpyZFdKbGNtNWxkR1Z6TDNObGNuWnBZMlZoWTJOdmRXNTBJaXdpYTNWaVpYSnVaWFJsY3k1cGJ5OXpaWEoyYVdObFlXTmpiM1Z1ZEM5dVlXMWxjM0JoWTJVaU9pSmtaV1poZFd4MElpd2lhM1ZpWlhKdVpYUmxjeTVwYnk5elpYSjJhV05sWVdOamIzVnVkQzl6WldOeVpYUXVibUZ0WlNJNkltUmxabUYxYkhRdGRHOXJaVzR0TW5vM1pEVWlMQ0pyZFdKbGNtNWxkR1Z6TG1sdkwzTmxjblpwWTJWaFkyTnZkVzUwTDNObGNuWnBZMlV0WVdOamIzVnVkQzV1WVcxbElqb2laR1ZtWVhWc2RDSXNJbXQxWW1WeWJtVjBaWE11YVc4dmMyVnlkbWxqWldGalkyOTFiblF2YzJWeWRtbGpaUzFoWTJOdmRXNTBMblZwWkNJNklqTXpZVFZrWW1VM0xUWTBZemN0TVRGbE9TMDVZMlZoTFRBeVl6aG1abUkyTVdObVl5SXNJbk4xWWlJNkluTjVjM1JsYlRwelpYSjJhV05sWVdOamIzVnVkRHBrWldaaGRXeDBPbVJsWm1GMWJIUWlmUS5nNUkxVXFkVjlHOE1pbUxZTjA4QUhHckJmSXhzQWF3dHMwQlJMNzdRY0tBdVU4RzVISTJEVTlJOHk3cTJpaXJPdkt3OElVZEdvX1lZS3otSDQtRlVuamhXWjJxMTV1cVMtdkR0LTgwTVdvNHJoUHpBY2RYU3Q1Tms5bmRIYVI4XzBjMjNHel8ya3pIX1p3Y1E1d0U0ZVduZHVqNTI0MHhNRjB4TzNraUtzWHRiRzUxLTgyNWVCYVROcGtDMGh3amxoeFpROTJpckNxRFFhR3dILTRkTkIwTFhNSHBNNEJHaXc5d3lXdVZPVkNyV0ZQZWV1UjJpUzQ0YzdkMEVlWWp6TVNuc1hOWEJCMnk5ZVVBaVBVLUZCSnYxa29Rc0hGcU44UjhIT3kwZW1QOHUzb3lwYW5iUFFsSkFoajE0ZU1fNFJVaVFZZFExQ3diSEM3S2RmdWF2LVE='
#
#     # alicek106
#     decodedTokenB = 'ZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNklpSjkuZXlKcGMzTWlPaUpyZFdKbGNtNWxkR1Z6TDNObGNuWnBZMlZoWTJOdmRXNTBJaXdpYTNWaVpYSnVaWFJsY3k1cGJ5OXpaWEoyYVdObFlXTmpiM1Z1ZEM5dVlXMWxjM0JoWTJVaU9pSmtaV1poZFd4MElpd2lhM1ZpWlhKdVpYUmxjeTVwYnk5elpYSjJhV05sWVdOamIzVnVkQzl6WldOeVpYUXVibUZ0WlNJNkltRnNhV05sYXpFd05pMTBiMnRsYmkxdGVEYzVlQ0lzSW10MVltVnlibVYwWlhNdWFXOHZjMlZ5ZG1salpXRmpZMjkxYm5RdmMyVnlkbWxqWlMxaFkyTnZkVzUwTG01aGJXVWlPaUpoYkdsalpXc3hNRFlpTENKcmRXSmxjbTVsZEdWekxtbHZMM05sY25acFkyVmhZMk52ZFc1MEwzTmxjblpwWTJVdFlXTmpiM1Z1ZEM1MWFXUWlPaUk1T0RJMFlUVXlOeTAyWVRreExURXhaVGt0WW1Zek1pMHdNbU00Wm1aaU5qRmpabU1pTENKemRXSWlPaUp6ZVhOMFpXMDZjMlZ5ZG1salpXRmpZMjkxYm5RNlpHVm1ZWFZzZERwaGJHbGpaV3N4TURZaWZRLlhaQk10Ml9ROVpUdjVVQnRGdG56Q0JpTTBMRkdIQ09yQTQwMFZxVUpMUUdMeHRCMXo5WVZoYTRnYzdEUzl5d2ZFaDRWMDNRZW4yXzRUMExWSXNVbmdOMDRNRmhUOVJtci05TkdpRVVmUVFpUEd5SjNiN0MyZ1NtN1JNNWxHWVZGeGRfcXZybTBHWlotVUpnY054aXdnME9Ea3dOVkEwZ1FSVkhqemhoZUlZOWk0dUhaN1NtRVNMTk0xRk5XYjhBd3NCeWdhaUF2ZlBndVRmc216U3BsLUxwTVZqT3RTcEN3RUs5NEQ2djg0eGFSVzB4SDlORW9VSUZ4a2NxZlpheVVIMFF6d2lWQ0tuVThnWHpPMFd5OVV5aTJrS2FidlRGODZVdkR6SnAxR0tPdWZnRFV1REpiRkV2ZjNjSTFfdnFhQzNBUlFvdHlEejZ4dnJveC0zLTZHQQ=='
#
#     clientA = ApiInstanceGetter().getApiInstance(decodedTokenA)
#     clientB = ApiInstanceGetter().getApiInstance(decodedTokenB)
#
#     result, status = DeploymentExamples().create_deployment_sample(
#         clientB, DeploymentMessage('sample-deployment'))
