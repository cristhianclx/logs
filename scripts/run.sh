#!/bin/bash

uvicorn main:app \
  --reload \
  --reload-dir /code \
  --host 0.0.0.0 \
  --port $PORT \
  --use-colors \
  --timeout-keep-alive 60 \
  --limit-max-requests 1000 \
  --log-level info
