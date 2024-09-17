# Chaos Mesh

## Introduction
Chaos Mesh is a cloud-native Chaos Engineering platform that orchestrates chaos on Kubernetes environments.

## Perequisites
To check weather Helm is installed or not, execute the following command:
```
helm version
```
Install Chaos Mesh using helm


Step 1: Add Chaos Mesh repository
```
helm repo add chaos-mesh https://charts.chaos-mesh.org
```

Step 2: Create the namespace to install Chaos Mesh
```
kubectl create ns <namespace_name>
```

Step 3: Install Chaos Mesh in Containerd
```
helm install chaos-mesh chaos-mesh/chaos-mesh -n=chaos-testing --set chaosDaemon.runtime=containerd --set chaosDaemon.socketPath=/run/containerd/containerd.sock --set dashboard.securityMode=false --version 2.3.0
```
## Installation

```
helm install chaosmesh-chart chaosmesh-helm/ --values chaosmesh-helm/values.yaml
```

## Configuration

Default values are provided for a recommended setup. Check the values.yaml file for possible customizations.


## Uninstalling the Chart

To uninstall/delete: 
```
helm delete chaosmesh-chart
