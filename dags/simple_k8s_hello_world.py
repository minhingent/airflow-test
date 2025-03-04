from airflow.utils.dates import days_ago
from airflow.models.param import Param
from airflow.decorators import dag, task
import boto3
from botocore.exceptions import ClientError
from collections import namedtuple
from kubernetes.client import models as k8s
import logging
import time
from datetime import datetime
import uuid


AccessKey = namedtuple('AccessKey', 'access_key_id secret_key')
RackInfo = namedtuple('RackCapabilities', 'ip_addresses access_keys')

default_args = {
    'owner': 'minh',
}

LOGGER = logging.getLogger("airflow.task")  # Get Airflow logger

# @dag(
#     schedule=None,
#     start_date=days_ago(1),
#     description='KubernetesExecutor with Taskflow API',
#     schedule_interval=None,
#     default_args=default_args,
# )
# def simple_k8s_hello_world():
#     @task.kubernetes(image="apache/airflow:2.9.3", namespace="airflow")
#     def hello_world():
#         print('hello k8s')

#     hello_world()

# simple_k8s_hello_world()


new_config ={ "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            )
                        ]
                    )
                )
            }

default_args = {
    'start_date': datetime(2021, 1, 1)
}

@dag('simple_k8s_hello_world', schedule_interval=None, default_args=default_args, catchup=False)
def taskflow():

    @task(executor_config=new_config)
    def get_testing_increase():
        print('hello k8s')

    get_testing_increase()

dag = taskflow()