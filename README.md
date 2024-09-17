## Helm Charts [![pipeline status](https://gitlab.cern.ch/helm/charts/cern/badges/master/pipeline.svg)](https://gitlab.cern.ch/helm/charts/cern/commits/master)

This is the CERN Helm Chart repository.

[Check here](https://gitlab.cern.ch/helm/charts) for additional charts from upstream repositories mirrored at CERN.

For more information about installing and using Helm, see its [README.md](https://github.com/kubernetes/helm/tree/master/README.md).

To get a quick introduction to Charts see this [chart document](https://github.com/kubernetes/helm/blob/master/docs/charts.md).

## How do i enable this repository?

To add the CERN Charts repository, run `helm repo add`:
```
helm repo add cern https://registry.cern.ch/chartrepo/cern
```

To check available charts do a `helm search`.

## How do i install these charts?

After enabling the repository, just:
```
helm install <chart>
```

You can pass the `--verify` option to check chart provenance:
```bash
helm install --verify <chart>
```

For more information on using Helm, refer to the [Helm's documentation](https://github.com/kubernetes/helm#docs).

## Contributing a Chart

If you would like to add a chart to this repository, please open a Merge
Request with the new chart.

