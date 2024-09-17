# Telegraf

[Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) is the open source server agent to help you collect metrics from your stacks, sensors and systems.

## Introduction

This chart manages the deployment of telegraf on a [Kubernetes](http://kubernetes.io)
cluster using the [Helm](https://helm.sh) package manager.

## Prerequisites

- Kubernetes cluster, version >=1.15.3
- Helm version >= 3.x

## Installing the Chart

To install the chart with release name `my-release`:
```bash
helm install my-release telegraf
```
You can override the defaults with an additional configuration file (for now a secret file with the dbod secret is expected to be passed):
```bash
helm install my-release telegraf -f secrets.yaml
```

For the cassandra image, the secrets file includes the password for an influxdb (DBOD) instance.

## Uninstalling the Chart

To uninstall / delete deployment `my-release`:
```bash
helm delete my-release
```
