#!/bin/bash

# Check if both parameters are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 model_name log_file"
    exit 1
fi

MODEL_NAME="$1"
LOG_FILE="$2"

# Check if the log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found."
    exit 1
fi

# Use grep to efficiently filter the log file
grep -E 'WARNING|ERROR|CRITICAL' "$LOG_FILE" | grep "$MODEL_NAME"

