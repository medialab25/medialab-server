#!/bin/bash
cd /workspace/server
uvicorn src.main:app --host 0.0.0.0 --port 4800 --reload 