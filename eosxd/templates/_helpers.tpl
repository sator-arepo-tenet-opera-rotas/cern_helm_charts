{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "eosxd.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "eosxd.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "eosxd.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Return configuration for a mountpoint
*/}}
{{- define "mountpoint.config" -}}
{{- $default_config := dict "name" .name "hostport" (printf "eos%s.cern.ch" .server) "localmountdir" (printf "/eos/%s/" .name) "remotemountdir" (printf "/eos/%s/" .remote) }}
{{- $mount_config  := ternary (get .config .name) dict (hasKey .config .name) -}}
{{- $global_config  := ternary (get .config "global") dict (hasKey .config "global") -}}
{{- $extra_config  := ternary (get . "extra_config") dict (hasKey . "extra_config") -}}
{{ merge dict $default_config $extra_config $global_config $mount_config | toJson | indent 4 }}
{{- end -}}
