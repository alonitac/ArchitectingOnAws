# Kubernetes tutorials

## Deploy the Chat app

1. In the AWS EC2 console, connect to your EC2 Windows server via RDS.
2. Add the following IAM role to your EC2 instance `eks-cluster-management`.
3. If needed, install the AWS cli tool by running the following command from PowerShell:
```shell
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```
3. Get credentials to communicate with the k8s cluster by:
```shell
aws eks update-kubeconfig --region us-east-1 --name big-data
```
4. First, create a namespace in k8s in which you will deploy your workloads:
```shell
kubectl create namespace <your-namespace>
```
5. Great! Now open a PowerShell terminal or CMD and type
```shell
kubectl proxy
```
This command proxies the whole cluster API into your local machine.
6. Open a web browser and go to the K8S dashboard: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#!/login

7. The token can be found [here](https://docs.google.com/document/d/1LyIv38irNgaPf63yAG40hDzNj20-u3EMIJRc0CyclQU/edit?usp=sharing).

8. Deploy the chat app and the worker. Make sure you specify the relevant env vars:
    - `<your-namespace>` - your cluster namespace
    - `<sqs-region>` - the region of your SQS queue
    - `<sqs-queue-name>` - the SQS queue name
    - `<mysql-db-name>` - the MySQL data endpoint

```shell
kubectl apply -f k8s/chat-app-webserver.yaml
kubectl apply -f k8s/chat-app-worker.yaml
```
If you don't see those files in your source code, execute `git pull` from your source code directory.  

9. In order to visit your app you need to forward the service to be available in your local machine. You can do it using the `kubectl port-forward` command:
```shell
kubectl port-forward -n <your-namespace> svc/chat-app-webserver-service 8080:8080
```
10. Open a web browser and visit the app in `http://localhost:8080`

## Perform a rolling update 

1. Apply the following resource to perform a rolling update
```shell
kubectl apply -f k8s/chat-app-worker-bad.yaml
```

How k8s reacted to your new replicaset? 

## Add liveness probes


1. Apply the following resource to perform let k8s monitor you containers
```shell
kubectl apply -f k8s/chat-app-webserver-liveness.yaml
```

What happen when a container become unhealthy?

## Resource cpu allocation

Apply `kubectl apply -f k8s/cpu-stress-test.yaml`

## Autoscaling

Apply `kubectl apply -f k8s/worker-pod-autoscale.yaml` (change relevant values).
Test your app under load!


## Deploy MongoDB and NodeJs webapp

Apply the resources in `k8s/mongo` in the following order:

- `kubectl apply -f k8s/mongo-secret.yaml`
- `kubectl apply -f k8s/mongo-config.yaml`
- `kubectl apply -f k8s/mongo.yaml`
- `kubectl apply -f k8s/webapp.yaml`

And if needed:

- `kubectl apply -f k8s/mongo-express.yaml`