#!/bin/sh

curl https://dust.tt/api/v1/w/b74db6909a/apps/ed5b092a75/runs \
    -H "Authorization: Bearer sk-b329e4058b9abc058a329ed021edea96" \
    -H "Content-Type: application/json" \
    -d '{
      "specification_hash": "fd89f27d5b93e02466d61e0b224b876e20f2e2ed258447ba676725e31c65152d",
      "config": {"DATASOURCE":{"data_sources":[{"workspace_id":"b74db6909a","data_source_id":"kayobe"}],"top_k":12,"filter":{"tags":null,"timestamp":null},"use_cache":false},"MODEL":{"provider_id":"openai","model_id":"gpt-3.5-turbo","function_call":null,"use_cache":true}},
      "blocking": true,
      "inputs": [{ "question": "Explain how to setup a machine for OpenStack." }]
    }'