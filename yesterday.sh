#!/bin/bash

# Get the full paths for this bash script 
# and the folder containing this script.
path=$(readlink -f -- "$0")
location=${path%/*}

# Activate the chessenv venv environment.
activate="/chessenv/bin/activate"
fullpathactivate="$location$activate"

source $fullpathactivate

# Run yesterday.py
yesterday="/yesterday.py"
fullpathyesterday="$location$yesterday"

python $fullpathyesterday

