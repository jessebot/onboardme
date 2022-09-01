---
layout: default
title: Kubernetes
permalink: /docs/k8s
---

# K8s stuff
## KIND - because easy local testing on linux

```bash
# creating a quick small cluster (unnamed, defaults to name: kind)
sudo kind create cluster

# adding newly created KIND kubeconfig
sudo kind get kubeconfig > ~/.kube/kubeconfig
```

## HELM - package manager for k9s

### installing helm
```bash
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```
