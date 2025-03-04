from airflow.utils.dates import days_ago
from airflow.models.param import Param
from airflow.decorators import dag, task
import boto3
from botocore.exceptions import ClientError
from collections import namedtuple
from kubernetes.client import models as k8s
import logging
import time
import uuid


AccessKey = namedtuple('AccessKey', 'access_key_id secret_key')
RackInfo = namedtuple('RackCapabilities', 'ip_addresses access_keys')

default_args = {
    'owner': 'minh',
}

LOGGER = logging.getLogger("airflow.task")  # Get Airflow logger

@dag(
    schedule=None,
    start_date=days_ago(1),
    description='KubernetesExecutor with Taskflow API',
    schedule_interval=None,
    default_args=default_args,
)
def simple_k8s_hello_world():
    @task.kubernetes(image="python:3.9", namespace="airflow")
    def hello_world():
        print('hello k8s')

    hello_world()

simple_k8s_hello_world()
