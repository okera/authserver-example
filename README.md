# Authserver Example

This repository contains the definition of two containers, one for the `authserver` binary Okera provides, and another that shows how it is used.

See the `./run.sh` script to start a local `kind` based K8s cluster and then build, push and deploy the containers into it.

Note: You can build the container images separately and push it to any other registry, then deploy them into your own K8s infrastructure.