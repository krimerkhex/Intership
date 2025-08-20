#!/bin/bash

export PYTHONENV=$(pwd)

alembic downgrade base

alembic upgrade head

python3 fastapi_server.py --host "0.0.0.0"
