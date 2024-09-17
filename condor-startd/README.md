# HTCondor StartD

[HTCondor](https://research.cs.wisc.edu/htcondor/) is a specialized
workload management system for compute-intensive jobs.

## Introduction

This chart manages the deployment of HTCondor startd on a [Kubernetes](http://kubernetes.io)
cluster using the [Helm](https://helm.sh) package manager.

## Prerequisites

- Kubernetes cluster, version >=1.9

## Installing the Chart

You can either clone the chart locally, or better add the cern repo to helm:
```
helm repo add cern https://cern.ch/test-charts
```

To install the chart with release name `my-release`:
```bash
helm install --namespace=my-release --name=my-release condor-startd
```

The command deploys a startd instance in each of the cluster nodes using the
default configuration, all defined and documented in values.yaml.

You can override the defaults with an additional configuration file:
```bash
helm install --namespace=my-release --name=my-release -f myconfig.yaml
```

## Uninstalling the Chart

To uninstall / delete deployment 'my-release':
```bash
helm delete my-release
```

To get rid of all the resources, use purge:
```bash
helm delete --purge my-release
```
