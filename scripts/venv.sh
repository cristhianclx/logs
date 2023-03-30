#!/bin/bash

pip install \
  --user \
  -r requirements/requirements-docker.txt \
  --src $HOME/src \
  --upgrade
