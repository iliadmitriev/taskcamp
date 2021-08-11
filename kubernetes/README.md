# deploy to kubernetes

apply rabbimq cluster operator service and custom resource
```shell
kubectl apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"
```

apply postgres database
```shell
kubectl apply -f postgres.yaml
```
wait for pods to start

and check cluster health
```shell
kubectl exec -ti pg-etcd-0 -- /opt/etcd/etcdctl member list
kubectl exec -ti pg-postgres-0 -- patronictl list
```

you don't need to do it, but in case your kubernetes cluster malfunction
you have to set label role=master manually
```shell
kubectl label pod pg-postgres-0 role=master
```

create database
```shell
kubectl exec -ti pg-postgres-0 -- sh
psql -U postgres -d postgres -h localhost -p 5432
psql -U postgres -d postgres -h localhost -p 5432 \
  -c "create user taskcamp with password 'secret' superuser;"
psql -U taskcamp -d postgres -h localhost -p 5432 -c "create database taskcamp;"
```

create rabbitmq cluster
```shell
kubectl apply -f rmq.yaml
```

check logs 
```shell
kubectl logs -f rmq-taskcamp-server-0
```

create mailcatcher service
```shell
kubectl apply -f mailcatcher.yaml
```

create memcached service
```shell
kubectl apply -f memcached.yaml
```

# deploy application

create taskcamp secret config
```shell
kubectl apply -f taskcamp-secret.yaml
```

deploy web application and celery
```shell
kubectl apply -f taskcamp-deploy.yaml
```

migrate database
```shell
kubectl exec -ti taskcamp-64558cf845-bm8fr -- sh
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