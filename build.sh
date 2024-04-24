#!/bin/bash
set -e

isort .
black .
mypy .
docker compose up