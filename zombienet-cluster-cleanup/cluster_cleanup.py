import os
from datetime import datetime, timedelta
from kubernetes import client, config
import requests
import pytz

NS_LIFE_TIME = os.getenv('NS_LIFE_TIME', "2")


def main():
    print("Starting cluster cleanup...")
    config.load_incluster_config()

    v1 = client.CoreV1Api()

    prefix = 'zombie-'
    time_delta = timedelta(hours=int(NS_LIFE_TIME))

    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    cutoff_time = now - time_delta
    print(f"Current time: {now}, Cutoff time for deletion: {cutoff_time}")
    print(f"Looking for namespaces with prefix '{prefix}' older than {NS_LIFE_TIME} hours...")
    namespace_list = v1.list_namespace().items
    for ns in namespace_list:
        if ns.metadata.name.startswith(prefix):
            creation_time = ns.metadata.creation_timestamp.replace(tzinfo=pytz.UTC)
            if creation_time < cutoff_time:
                print(f"Found zombie namespace {ns.metadata.name} (created {now - creation_time} ago and matches the prefix).")
                v1.delete_namespace(ns.metadata.name)

    api_version = 'v1'
    group = 'monitoring.coreos.com'
    plural = 'podmonitors'
    namespace = 'monitoring'

    print(f"Looking for PodMonitors in namespace '{namespace}' older than {NS_LIFE_TIME} hours...")
    try:
        custom_api = client.CustomObjectsApi()
        pm_list = custom_api.list_namespaced_custom_object(group, api_version, namespace, plural)['items']

        for pm in pm_list:
            name = pm['metadata']['name']
            creation_time = datetime.strptime(pm['metadata']['creationTimestamp'], '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
            creation_time = creation_time.astimezone(pytz.UTC)
            if creation_time < cutoff_time:
                print(f"Found old PodMonitor {name} in namespace {namespace} (created {now - creation_time} ago).")
                custom_api.delete_namespaced_custom_object(group, api_version, namespace, plural, name, body={}, grace_period_seconds=0)
    except Exception as e:
        print(f"Error while checking PodMonitors: {e}")

    print("Cluster cleanup completed.")


if __name__ == "__main__":
    main()
