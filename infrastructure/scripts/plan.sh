#!/bin/bash

terraform fmt \
  -check \
  -diff \
  -recursive

terraform plan \
  -refresh=true \
  -var-file=./vars/main.tfvars
