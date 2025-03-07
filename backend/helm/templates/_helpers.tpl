{{/*
Returns the full name of the release
*/}}
{{- define "my-helm-chart.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}

{{/*
Returns the name of the chart
*/}}
{{- define "my-helm-chart.name" -}}
{{ .Chart.Name }}
{{- end -}}
