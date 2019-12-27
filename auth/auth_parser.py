import configparser
import os


class AuthParser:
    IN_CLUSTER_POD_AUTH = 1
    SERVICE_ACCOUNT_TOKEN_AUTH = 2
    CERTIFICATE_AUTH = 3

    auth_type = None
    service_account_token = None
    cert_file_name = None
    cert_key_file_name = None
    kube_api_server_ip = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config/auth_config.ini'))
        self.auth_type = int(config['AUTH_CONFIG']['AUTH_TYPE'])
        self.kube_api_server_ip = config['AUTH_CONFIG']['KUBE_API_SERVER_IP']

        if self.auth_type == self.SERVICE_ACCOUNT_TOKEN_AUTH:
            self.service_account_token = config['AUTH_CONFIG']['SERVICE_ACCOUNT_TOKEN']
        elif self.auth_type == self.CERTIFICATE_AUTH:
            self.cert_file_name = config['AUTH_CONFIG']['CERT_FILE_NAME']
            self.cert_key_file_name = config['AUTH_CONFIG']['CERT_KEY_FILE_NAME']
        else:
            pass

    def get_auth_type(self):
        return self.auth_type