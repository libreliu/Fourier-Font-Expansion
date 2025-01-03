#!/usr/bin/env python3
import sys, json

def main():
    import bpy

    # Parse command line arguments
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # Blender passes its own arguments, so we need to get the ones after '--'

    # Check if the user provided a path
    if len(argv) > 0:
        output_file_path = argv[0]  # Get the first argument as the file path
    else:
        output_file_path = "flag-spline.json"  # Default path if none is provided

    if len(argv) > 1:
        target_text = argv[1]
    else:
        target_text = "example_text"

    if len(argv) > 2:
        font_ttf_path = argv[2]
    else:
        font_ttf_path = None

    print(f"Output file path: {output_file_path}, target text: {target_text}")

    # Delete any existing objects
    bpy.ops.object.delete(use_global=False)

    # Add new text object
    bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    ob = bpy.context.scene.objects['Text']

    # change font to desired if specified
    if font_ttf_path is not None:
        bpy.ops.font.open(filepath=font_ttf_path, relative_path=True)
        ob.data.font = bpy.data.fonts[1]

    # Modify the text body
    ob.data.body = f"{target_text}"

    # Set active object to the text object and convert it to a curve
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.convert(target='CURVE')

    # Prepare to store the output in JSON format
    output_data = []

    # Collect spline and bezier points data
    for splineIdx, splineObj in enumerate(ob.data.splines):
        spline_data = {
            "spline_index": splineIdx,
            "bezier_points": []
        }
        for bezPointIdx, bezPointObj in enumerate(splineObj.bezier_points):
            bezier_point_data = {
                "bezier_index": bezPointIdx,
                "coordinates": list(bezPointObj.co),
                "handle_left": list(bezPointObj.handle_left),
                "handle_right": list(bezPointObj.handle_right)
            }
            spline_data["bezier_points"].append(bezier_point_data)
        
        output_data.append(spline_data)

    # Write the JSON data to the file
    with open(output_file_path, 'w') as file:
        json.dump(output_data, file, indent=4)

    print(f"Output written to {output_file_path}")

import importlib.util

bpySpec = importlib.util.find_spec("bpy")
isInBlenderEnv = bpySpec is not None

if isInBlenderEnv:
    main()
else:
    import subprocess
    import os

    script_path = os.path.abspath(__file__)
    blender_executable = sys.argv[1]

    try:
        subprocess.run([
            blender_executable, 
            "--background",  # Run without GUI
            "--python", script_path,  # Execute this script
            "--", *sys.argv[2:]  # Pass remaining arguments
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing Blender: {e}")
