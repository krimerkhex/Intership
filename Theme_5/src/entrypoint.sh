#!/bin/bash

export PYTHONENV=$(pwd)

alembic upgrade head

nohup python3 fastapi_main --host "0.0.0.0" > /dev/null 2>&1 &
