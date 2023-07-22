#!/bin/sh
alembic upgrade head
uvicorn app.main:init_app --factory --host 0.0.0.0 --port 8000
