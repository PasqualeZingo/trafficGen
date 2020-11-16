#!/bin/bash
curl -X POST localhost:5601/api/kibana/dashboards/import?force=true -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d @$1
