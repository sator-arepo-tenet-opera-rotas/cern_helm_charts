# SSSD

[SSSD](https://pagure.io/SSSD/sssd/) provides a set of daemons to manage access
to remote directories and authentication mechanisms such as LDAP, Kerberos or
FreeIPA.

It provides an NSS and PAM interface toward the system and a pluggable backend
system to connect to multiple different account services.

## Introduction

This chart manages the deployment of sssd on a [Kubernetes](http://kubernetes.io)
cluster using the [Helm](https://helm.sh) package manager.

## Prerequisites

- Kubernetes cluster, version >=1.9

## Installing the Chart

To install the chart with release name `my-release`:
```bash
helm install --namespace=my-release --name=my-release sssd
```
You can override the defaults with an additional configuration file:
```bash
helm install --namespace=my-release --name=my-release sssd -f myconfig.yaml
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
