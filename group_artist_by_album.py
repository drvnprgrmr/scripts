import os
import sys
import subprocess
import argparse
from collections import defaultdict
from time import sleep

# Initialize parser
parser = argparse.ArgumentParser()

# Add arguments to parser
parser.add_argument("folder")

# Get the arguments
args = parser.parse_args()


# Function to extract album name from file
def get_album(file):
    # Get the result from running the command
    res = subprocess.run(["exiftool", "-s3", "-Album", file], capture_output=True)

    # Return the decoded and stripped output
    return res.stdout.decode().strip()


# Ensure the folder exists
if os.path.exists(args.folder) and os.path.isdir(args.folder):
    # Process the files from the directory
    files = []
    for sub in os.listdir((args.folder)):
        full_path = os.path.join(args.folder, sub)
        # Add to list if it is a file
        if os.path.isfile(full_path):
            files.append(full_path)

    print("Number of files found: ", len(files), end="\n\n")

    # Group mp3 files by their album name
    albums = defaultdict(list)
    for file in files:
        albums[get_album(file)].append(file)

    for album_name, album_files in albums.items():
        if len(album_files) > 1:
            # Make album directory
            album_dir = os.path.join(args.folder, album_name)
            print(f"Creating '{album_dir}'")
            os.mkdir(album_dir)

            # Move all files under album into this folder
            for album_file in album_files:
                album_file_basename = os.path.basename(album_file)

                # Get source and final destinations
                src = os.path.join(args.folder, album_file_basename)
                dest = os.path.join(album_dir, album_file_basename)

                # Move files
                print(f"Moving '{src}' into '{dest}'")
                os.rename(src, dest)

                # Sleep a bit as it moves too fast on my system
                sleep(.1)
        else:
            print(f"Skipping '{album_name}' as there's only one file.")

        print()

else:
    print(f"{args.folder} is not a valid folder", file=sys.stderr)
    exit()
