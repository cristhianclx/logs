#!/bin/bash

terraform apply \
  -auto-approve \
  -var-file=./vars/main.tfvars
