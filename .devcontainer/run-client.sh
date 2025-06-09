#!/bin/bash
cd /workspace/client
uvicorn src.main:app --host 0.0.0.0 --port 4810 --reload 