## Landb Sync

This chart manages the deployment and configuration of the landb-sync component.

### Requirements

### Installation

You need the cern repo configured:
```bash
helm repo add cern https://registry.cern.ch/chartrepo/cern

helm repo update

helm install --name landb-sync --namespace kube-system cern/landb-sync
```

### Configuration

Default values are provided for a recommended setup.

Check the values.yaml file for possible customizations.
