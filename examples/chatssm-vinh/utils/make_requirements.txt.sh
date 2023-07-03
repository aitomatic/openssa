#!/bin/bash -x
poetry export --with dev --format requirements.txt --output requirements.txt
