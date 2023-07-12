#!/bin/sh

curl https://dust.tt/api/v1/w/3e26b0e764/data_sources/kayobe/documents/page2 \
  -H "Authorization: Bearer sk-b329e4058b9abc058a329ed021edea96" \
  -H "Content-Type: application/json" \
  -d "{"text":\"$(cat "object.txt")\"}" 
