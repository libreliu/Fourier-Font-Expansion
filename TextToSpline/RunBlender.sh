#!/bin/bash

BLENDER_EXECUTABLE=/opt/blender-lts/blender
EXTRA_LD_LIBRARY_PATH=/opt/blender-lts/lib

# Function to display usage
usage() {
  echo "Usage: $0 <filename_prefix> <text>"
  echo "  <filename_prefix>: The prefix of the JSON filename"
  echo "  <text>: text to be converted to bezier splines"
  exit 1
}

# Function to run Blender script
runBlender() {
  LD_LIBRARY_PATH=${EXTRA_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH} python TextToSpline.py "${BLENDER_EXECUTABLE}" "$1.json" "$2"
}

# Validate arguments
if [[ $# -ne 2 ]]; then
  echo "Error: Invalid number of arguments."
  usage
fi

filename_prefix="$1"
text="$2"

# Call the function with validated arguments
runBlender "$filename_prefix" "$text"
