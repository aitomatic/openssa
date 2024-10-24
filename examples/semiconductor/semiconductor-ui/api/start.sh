#!/bin/bash
uvicorn main:app --loop "asyncio" --proxy-headers --host 0.0.0.0 --port 8080
