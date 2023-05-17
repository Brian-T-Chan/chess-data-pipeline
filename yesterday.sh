#!/bin/bash

path=$(readlink -f -- "$0")
location=${path%/*}

activate="/chessenv/bin/activate"
fullpathactivate="$location$activate"

source $fullpathactivate

yesterday="/yesterday.py"
fullpathyesterday="$location$yesterday"

python $fullpathyesterday

