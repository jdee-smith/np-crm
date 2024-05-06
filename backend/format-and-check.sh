#!/bin/bash
set -e

isort .
black .
mypy .