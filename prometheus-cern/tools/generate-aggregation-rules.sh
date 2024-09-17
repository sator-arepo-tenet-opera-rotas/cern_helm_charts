#!/bin/bash

# To automatically update the upstream PrometheusRules into aggregated rules
#     you must:
# 1. Create an upstream only magnum cluster fresh install with the default
#     prometheus server.
# 2. Clone this repo into said server.
# 3. Run this script in place.
# 4. Commit changes.

# TODO: We can do everything automatically.
# 1. create cluster with needed flags automatically
# 2. After cluster created, setup kubectl configs.
# 3. Run script automatically
# 4. Add, commit and push (optionally) to upstream corresponding repo.

# Get all available PrometheusRules under kube-system Namespace
PROMETHEUS_RULES=$(kubectl -n kube-system get PrometheusRules --template '{{range .items}}{{.metadata.name}}{{","}}{{end}}' -o go-template )

# Change to working directory
cd $(dirname "$0")

# Call generator
python generator-rules_aggregation.py --rules "${PROMETHEUS_RULES}"
