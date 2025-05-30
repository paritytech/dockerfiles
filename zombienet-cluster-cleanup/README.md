### Zombie Namespace Cleanup Script

This Python script is designed to identify and delete "zombie-" prefixed Kubernetes namespaces and PodMonitors that are older than 2 hours of age. It uses the Kubernetes Python client library to connect to the API server and query the list of namespaces and podmonitors and then proceeds with deleting them.

### Usage

- Ensure that the Kubernetes Python client library is installed (`pip install -r requirements.txt`);
- Update the `NS_LIFE_TIME` env variables if needed (default value is 2);
- Run the script with python `cluster_cleanup.py`;

### CronJob

To automate the zombie namespace cleanup process, the following Kubernetes CronJob can be used:

```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cluster-cleanup
  namespace: cluster-cleanup
spec:
  schedule: "0 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: cluster-cleanup
          containers:
            - name: cluster-cleanup
              image: paritytech/zombienet-cluster-cleanup
              env:
                - name: NS_LIFE_TIME
                  value: "2"
          restartPolicy: OnFailure
```

This CronJob will run the `paritytech/zombienet-cluster-cleanup` image with the cluster-cleanup service account every hour in the cluster-cleanup namespace.

To deploy the CronJob, save the manifest to a file (e.g. cronjob.yaml) and run the following command:

```
kubectl apply -f cronjob.yaml
```

This will create the CronJob in the cluster and start running it on the specified schedule.
