#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_folder> <filename_prefix>"
    exit 1
fi

OUTPUT_FOLDER=$1
FILENAME_PREFIX=$2

# Create the output folder if it doesn't exist
mkdir -p "$OUTPUT_FOLDER"

# Loop through all letters a-z and A-Z
for CHAR in {a..z} {A..Z}; do
    if [[ $CHAR =~ [A-Z] ]]; then
        # Capital letters: prepend "CAPITAL"
        OUTPUT_FILE="$OUTPUT_FOLDER/${FILENAME_PREFIX}_CAPITAL_$CHAR"
    else
        # Lowercase letters
        OUTPUT_FILE="$OUTPUT_FOLDER/${FILENAME_PREFIX}_$CHAR"
    fi
    
    # Run the script with the current character
    ./RunBlender.sh "$OUTPUT_FILE" "$CHAR"
done


echo "All files have been processed and stored in $OUTPUT_FOLDER."
