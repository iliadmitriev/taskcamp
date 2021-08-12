# minikube

create and start 3 node minikube installation with ingress, dashboard and metrics server
```shell
minikube start --nodes=3 --addons=ingress,dashboard,metrics-server
```

# deploy

apply rabbimq cluster operator service and custom resource
```shell
kubectl apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"
```

apply postgres database
```shell
kubectl apply -f kubernetes
```
wait for pods to start

```shell
kubectl get pods -w
```

migrate database and create superuser
```shell
kubectl exec -ti deployment/taskcamp -- sh
python3 manage.py migrate
python3 manage.py createsuperuser
```

load data from fixture file `data.json`
```shell
cat data.json | kubectl exec -i deploy/taskcamp -- python3 manage.py loaddata --format=json -
```

# expose

create secrets
```shell
# for email web interface
kubectl create secret tls mail-taskcamp-tls \
  --key mail.taskcamp.info.key \
  --cert mail.taskcamp.info.pem

# for rabbitmq web interface
kubectl create secret tls rmq-taskcamp-tls \
  --key rmq.taskcamp.info.key \
  --cert rmq.taskcamp.info.pem 

# for taskcamp UI
kubectl create secret tls taskcamp-tls \
  --cert taskcamp.info.pem \
  --key taskcamp.info.key                                
```

create ingress
```shell
# for mail https://mail.taskcamp.info/
kubectl create ingress mail-taskcamp-ingress \
  --default-backend=mailcatcher-node-port:1080 \
  --rule="mail.taskcamp.info/*=mailcatcher-node-port:1080,tls=mail-taskcamp-tls"

# for rabbitmq https://rmq.taskcamp.info/
kubectl create ingress rmq-taskcamp-ingress \
  --default-backend=rmq-management-nodeport:15672 \
  --rule="rmq.taskcamp.info/*=rmq-management-nodeport:15672,tls=rmq-taskcamp-tls"
    
# for web UI https://taskcamp.info/
kubectl create ingress taskcamp-ingress \
  --default-backend=taskcamp:8080 \
  --rule="taskcamp.info/*=taskcamp:8000,tls=taskcamp-tls"
```

minikube tunnel
```shell
minikube tunnel
# ask for user password (for tcp port binding < 1024)
```