#!/bin/bash

# Get the full paths for this bash script 
# and a folder containing both the venv
# environment and (a clone of) this repo.
path=$(readlink -f -- "$0")
location=$(dirname "$(dirname "$path")")

# Activate the chessenv venv environment.
activate="/chessenv/bin/activate"
fullpathactivate="$location$activate"

source $fullpathactivate

# Run yesterday.py
yesterday="/chess-data-pipeline/yesterday.py"
fullpathyesterday="$location$yesterday"

python $fullpathyesterday

