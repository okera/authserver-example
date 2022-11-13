#!/bin/bash
set -e

# start a local kind cluster with a registry running in it
bin/kind-with-registry.sh

# build images and push into local registry
docker build -t localhost:5001/authserver:v0.1 authserver && docker push localhost:5001/authserver:v0.1
docker build -t localhost:5001/myservice:v0.1 service && docker push localhost:5001/myservice:v0.1

# deploy the K8s manifests
kubectl apply -f k8s.yaml

# test the service
kubectl exec -it myservice -c myservice -- curl http://test:test@myservice:5010