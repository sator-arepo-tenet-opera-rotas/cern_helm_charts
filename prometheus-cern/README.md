## Prometheus CERN

This chart holds the default setup for CERN aggregated metric setup.

### Installation

You need the cern repo configured:
```bash
helm repo add cern https://registry.cern.ch/chartrepo/cern

helm repo update

helm install --name prometheus-cern --namespace kube-system cern/prometheus-cern
```

### Configuration

Default values are provided for a recommended setup.

Check the values.yaml file for possible customizations.
