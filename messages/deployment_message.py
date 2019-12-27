import json
import os


class DeploymentMessage:

    deployment_name = None
    image = None
    replicas = None
    namespace = None
    publish_ports = []
    env_vars = []
    labels = []
    resources = []

    def __init__(self, type):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_data/deployment_examples_data.json')) as data_file:
            json_data = json.load(data_file)[type]

        # Default Settings
        self.namespace = json_data['namespace']
        self.deployment_name = json_data['deployment_name']
        self.image = json_data['image']
        self.replicas = json_data['replicas']
        self.publish_ports = json_data['publish_ports'] # Array
        self.env_vars = json_data['env_vars'] # Array
        self.labels = json_data['labels'] # Array
        self.resources = json_data['resources']

        # TODO : Add another conditional statement for extended examples.