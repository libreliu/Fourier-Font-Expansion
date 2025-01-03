#!/bin/bash

BLENDER_EXECUTABLE=/opt/blender-lts/blender
EXTRA_LD_LIBRARY_PATH=/opt/blender-lts/lib

# Function to display usage
usage() {
  echo "Usage: $0 filename_prefix text <font_path>"
  echo "  filename_prefix: The prefix of the JSON filename"
  echo "  text: text to be converted to bezier splines"
  echo "  <font_path>: Optional, ttf font to be used"
  exit 1
}

# Function to run Blender script
runBlender() {
  if [[ $# -eq 2 ]]; then
    LD_LIBRARY_PATH=${EXTRA_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH} python TextToSpline.py "${BLENDER_EXECUTABLE}" "$1.json" "$2"
  elif [[ $# -eq 3 ]]; then
    LD_LIBRARY_PATH=${EXTRA_LD_LIBRARY_PATH}:${LD_LIBRARY_PATH} python TextToSpline.py "${BLENDER_EXECUTABLE}" "$1.json" "$2" "$3"
  fi
}

# Validate arguments
if [[ $# -ne 2 ]] && [[ $# -ne 3 ]]; then
  echo "Error: Invalid number of arguments."
  usage
fi

filename_prefix="$1"
text="$2"
font_path="$3"

# Call the function with validated arguments
runBlender "$filename_prefix" "$text" "$font_path"
