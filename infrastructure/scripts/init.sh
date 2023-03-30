#!/bin/bash

terraform init \
  -backend=true \
  -get=true \
  -reconfigure \
  -upgrade
