#!/bin/bash

branch=$(git rev-parse --abbrev-ref HEAD)
commit=$(git log -1 --pretty=%B)
hex=$(git rev-parse --short HEAD)

echo "{\"branch\": \"$branch\", \"commit\": \"$commit\", \"hex\": \"$hex\"}" > info.json
