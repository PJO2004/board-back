new_dash: dict = {
    "dashboard": {
        "annotations": {
            "list": [
                {
                    "builtIn": 1,
                    "datasource": {"type": "grafana", "uid": "-- Grafana --"},
                    "enable": True,
                    "hide": True,
                    "iconColor": "rgba(0, 211, 255, 1)",
                    "name": "Annotations & Alerts",
                    "target": {"limit": 100, "matchAny": False, "tags": [], "type": "dashboard"},
                    "type": "dashboard",
                }
            ]
        },
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 0,
        "id": None,
        "links": [],
        "liveNow": False,
        "panels": [
            {
                "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "continuous-GrYlRd"},
                        "custom": {
                            "axisLabel": "",
                            "axisPlacement": "auto",
                            "barAlignment": 0,
                            "drawStyle": "line",
                            "fillOpacity": 20,
                            "gradientMode": "scheme",
                            "hideFrom": {"legend": False, "tooltip": False, "viz": False},
                            "lineInterpolation": "smooth",
                            "lineWidth": 3,
                            "pointSize": 5,
                            "scaleDistribution": {"type": "linear"},
                            "showPoints": "auto",
                            "spanNones": False,
                            "stacking": {"group": "A", "mode": "none"},
                            "thresholdsStyle": {"mode": "off"},
                        },
                        "mappings": [],
                        "max": 1,
                        "min": 0,
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "red", "value": 80},
                            ],
                        },
                        "unit": "percentunit",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                "id": None,
                "options": {
                    "legend": {"calcs": [], "displayMode": "hidden", "placement": "bottom"},
                    "tooltip": {"mode": "single", "sort": "none"},
                },
                "pluginVersion": "9.0.1",
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                        "editorMode": "code",
                        "exemplar": False,
                        "expr": 'sum(rate(container_cpu_usage_seconds_total{name=~"(Project_name)"}[5m])) by (name) *100',
                        "format": "time_series",
                        "instant": False,
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "cpu_usage",
                "type": "timeseries",
            },
            {
                "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "continuous-GrYlRd"},
                        "custom": {
                            "axisLabel": "",
                            "axisPlacement": "auto",
                            "barAlignment": 0,
                            "drawStyle": "bars",
                            "fillOpacity": 90,
                            "gradientMode": "scheme",
                            "hideFrom": {"legend": False, "tooltip": False, "viz": False},
                            "lineInterpolation": "linear",
                            "lineWidth": 1,
                            "pointSize": 5,
                            "scaleDistribution": {"type": "linear"},
                            "showPoints": "auto",
                            "spanNones": False,
                            "stacking": {"group": "A", "mode": "none"},
                            "thresholdsStyle": {"mode": "off"},
                        },
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "red", "value": 80},
                            ],
                        },
                        "unit": "bytes",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                "id": None,
                "options": {
                    "legend": {"calcs": [], "displayMode": "hidden", "placement": "bottom"},
                    "tooltip": {"mode": "single", "sort": "none"},
                },
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                        "editorMode": "code",
                        "expr": 'sum(container_memory_rss{name=~"(Project_name)"}) by (name)',
                        "legendFormat": "{{name}}",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Memory Usage",
                "type": "timeseries",
            },
            {
                "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "noValue": "0",
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "green", "value": None}],
                        },
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 8, "w": 6, "x": 0, "y": 8},
                "None": 2,
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {"calcs": [], "fields": "", "values": False},
                    "textMode": "auto",
                },
                "pluginVersion": "8.5.5",
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                        "editorMode": "code",
                        "expr": 'sum(starlette_requests_total{job="(Project_name)",path!="/(Project_name)/metrics"})',
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Total Request",
                "type": "stat",
            },
            {
                "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "continuous-GrYlRd"},
                        "mappings": [],
                        "noValue": "0",
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "green", "value": None}],
                        },
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 8, "w": 6, "x": 6, "y": 8},
                "id": None,
                "options": {
                    "displayMode": "lcd",
                    "minVizHeight": 10,
                    "minVizWidth": 0,
                    "orientation": "horizontal",
                    "reduceOptions": {"calcs": [], "fields": "", "values": False},
                    "showUnfilled": True,
                    "text": {},
                },
                "pluginVersion": "8.5.5",
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                        "editorMode": "code",
                        "exemplar": False,
                        "expr": 'starlette_request_duration_seconds_sum{job="(Project_name)", path!="/(Project_name)/metrics", path!="/(Project_name)/docs", path!="/(Project_name)/openapi.json", path!="/(Project_name)/favicon.ico"}/starlette_request_duration_seconds_count{job="(Project_name)", path!="/(Project_name)/metrics", path!="/(Project_name)/docs", path!="/(Project_name)/openapi.json", path!="/(Project_name)/favicon.ico"}',
                        "instant": False,
                        "interval": "",
                        "legendFormat": "{{method}} {{path}}",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Requests Average Duration",
                "type": "bargauge",
            },
            {
                "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "max": 100,
                        "min": 0,
                        "noValue": "0",
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "dark-red", "value": None},
                                {"color": "green", "value": 70},
                            ],
                        },
                        "unit": "percent",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 8, "w": 6, "x": 12, "y": 8},
                "id": None,
                "options": {
                    "orientation": "auto",
                    "reduceOptions": {"calcs": ["lastNotNone"], "fields": "", "values": False},
                    "showThresholdLabels": False,
                    "showThresholdMarkers": True,
                },
                "pluginVersion": "8.5.5",
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                        "editorMode": "code",
                        "exemplar": False,
                        "expr": '(sum(starlette_requests_total{job="(Project_name)", path!="/(Project_name)/metrics", status_code=~"2.*"})/sum(starlette_requests_total{job="(Project_name)", path!="/(Project_name)/metrics"}))*100',
                        "instant": False,
                        "interval": "",
                        "legendFormat": "{{path}}",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Percent of 2xx Requests",
                "type": "gauge",
            },
            {
                "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "max": 100,
                        "min": 0,
                        "noValue": "0",
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "dark-red", "value": 30},
                            ],
                        },
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 8, "w": 6, "x": 18, "y": 8},
                "id": None,
                "options": {
                    "orientation": "auto",
                    "reduceOptions": {"calcs": [], "fields": "", "values": False},
                    "showThresholdLabels": False,
                    "showThresholdMarkers": True,
                },
                "pluginVersion": "8.5.5",
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                        "editorMode": "code",
                        "exemplar": False,
                        "expr": '(sum(starlette_requests_total{job="(Project_name)", path!="/(Project_name)/metrics", status_code!~"2.*"})/sum(starlette_requests_total{job="(Project_name)", path!="/(Project_name)/metrics"}))*100',
                        "instant": False,
                        "interval": "",
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Total Exception",
                "type": "gauge",
            },
            {
                "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "noValue": "0",
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "green", "value": None}],
                        },
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16},
                "id": None,
                "options": {
                    "colorMode": "value",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {"calcs": ["lastNotNone"], "fields": "", "values": False},
                    "text": {},
                    "textMode": "value_and_name",
                },
                "pluginVersion": "8.5.5",
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                        "editorMode": "code",
                        "expr": 'starlette_requests_total{job="(Project_name)", path!="/(Project_name)/metrics", path!="/(Project_name)/docs", path!="/(Project_name)/openapi.json", path!="/(Project_name)/favicon.ico"}',
                        "legendFormat": "{{method}} {{path}}",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Each Request",
                "type": "stat",
            },
            {
                "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "continuous-GrYlRd"},
                        "custom": {
                            "axisLabel": "",
                            "axisPlacement": "auto",
                            "barAlignment": 0,
                            "drawStyle": "line",
                            "fillOpacity": 20,
                            "gradientMode": "scheme",
                            "hideFrom": {"legend": False, "tooltip": False, "viz": False},
                            "lineInterpolation": "smooth",
                            "lineWidth": 3,
                            "pointSize": 5,
                            "scaleDistribution": {"type": "linear"},
                            "showPoints": "auto",
                            "spanNones": False,
                            "stacking": {"group": "A", "mode": "none"},
                            "thresholdsStyle": {"mode": "off"},
                        },
                        "mappings": [],
                        "max": 100,
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "red", "value": 80},
                            ],
                        },
                        "unit": "percent",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16},
                "id": None,
                "options": {
                    "legend": {"calcs": [], "displayMode": "list", "placement": "bottom"},
                    "tooltip": {"mode": "single", "sort": "none"},
                },
                "targets": [
                    {
                        "datasource": {"type": "prometheus", "uid": "(prometheus_uid)"},
                        "editorMode": "code",
                        "exemplar": False,
                        "expr": '(sum(starlette_requests_total{job="(Project_name)", path!="/(Project_name)/metrics", status_code!~"2.*",path!="/(Project_name)/docs", path!="/(Project_name)/openapi.json", path!="/(Project_name)/favicon.ico"})/sum(starlette_requests_total{job="(Project_name)", path!="/(Project_name)/metrics",path!="/(Project_name)/docs", path!="/(Project_name)/openapi.json", path!="/(Project_name)/favicon.ico"}))*100',
                        "instant": False,
                        "legendFormat": "{{path}}",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Error ",
                "type": "timeseries",
            },
            {
                "datasource": {"type": "loki", "uid": "(loki_uid)"},
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "palette-classic"},
                        "custom": {
                            "axisLabel": "",
                            "axisPlacement": "auto",
                            "axisSoftMin": 0,
                            "fillOpacity": 80,
                            "gradientMode": "none",
                            "hideFrom": {"legend": False, "tooltip": False, "viz": False},
                            "lineWidth": 2,
                            "scaleDistribution": {"type": "linear"},
                        },
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [
                                {"color": "green", "value": None},
                                {"color": "red", "value": 80},
                            ],
                        },
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 24},
                "id": None,
                "options": {
                    "barRadius": 0,
                    "barWidth": 0.97,
                    "groupWidth": 0.7,
                    "legend": {"calcs": [], "displayMode": "list", "placement": "bottom"},
                    "orientation": "auto",
                    "showValue": "auto",
                    "stacking": "none",
                    "tooltip": {"mode": "single", "sort": "none"},
                    "xField": "Time",
                    "xTickLabelRotation": 0,
                    "xTickLabelSpacing": 200,
                },
                "targets": [
                    {
                        "datasource": {"type": "loki", "uid": "(loki_uid)"},
                        "editorMode": "builder",
                        "expr": 'count_over_time({container_name="(Project_name)"} |= `` [$__interval])',
                        "legendFormat": "logs_number",
                        "maxLines": 0,
                        "queryType": "range",
                        "refId": "A",
                        "resolution": 1,
                    }
                ],
                "title": "Log Number for container",
                "type": "barchart",
            },
            {
                "datasource": {"type": "loki", "uid": "(loki_uid)"},
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 24},
                "id": None,
                "options": {
                    "dedupStrategy": "none",
                    "enableLogDetails": True,
                    "prettifyLogMessage": False,
                    "showCommonLabels": False,
                    "showLabels": False,
                    "showTime": False,
                    "sortOrder": "Descending",
                    "wrapLogMessage": False,
                },
                "pluginVersion": "9.0.1",
                "targets": [
                    {
                        "datasource": {"type": "loki", "uid": "(loki_uid)"},
                        "editorMode": "builder",
                        "expr": '{container_name="(Project_name)"} |= ``',
                        "queryType": "range",
                        "refId": "A",
                    }
                ],
                "title": "Logs from container",
                "type": "logs",
            },
        ],
        "refresh": "5s",
        "schemaVersion": 36,
        "style": "dark",
        "tags": [],
        "templating": {"list": []},
        "time": {"from": "now-15m", "to": "now"},
        "timepicker": {},
        "timezone": "",
        "title": "(Project_name)",
        "uid": None,
        "version": 1,
        "weekStart": "",
    }
}