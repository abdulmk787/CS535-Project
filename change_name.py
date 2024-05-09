import pandas as pd
import os
import subprocess
import shutil

# Specify the base directories
# directory = '/project/msoleyma_1026/TILES/tiles-phase2-opendataset-audio/raw-features'
# destination_directory = '/project/msoleyma_1026/TILES/tiles-phase2-opendataset-audio/raw-features-named'
directory = '/Users/abdulmk/Multimodal/Project/TILES/raw-features'
destination_directory = '/Users/abdulmk/Multimodal/Project/TILES/raw-features-named'


def rename_csv_and_copy(file_path, destination_directory):
    """Renames a CSV file (based on its first timestamp) and copies it to a destination directory. """
    try:
        df = pd.read_csv(file_path)
        first_timestamp = df.iloc[-1]['timeStamp'] 
        formatted_timestamp = pd.to_datetime(first_timestamp).strftime('%Y-%m-%d %H-%M-%S')
        new_filename = f"{formatted_timestamp}.csv"  

        # Create the corresponding subdirectory in the destination
        original_dir_path, _ = os.path.split(file_path)
        relative_dir = original_dir_path.replace(directory, "")  # Get subdirectory relative to the base directory
        destination_dir = os.path.join(destination_directory, relative_dir[1:])

        os.makedirs(destination_dir, exist_ok=True)  # Create if it doesn't exist

        # Construct the destination file path
        destination_file_path = os.path.join(destination_dir, new_filename) 

        # Copy the file (shutil.copyfile preserves metadata)
        shutil.copyfile(file_path, destination_file_path)
    except Exception as e:
        print(f"Error renaming and copying file: {file_path}")
        print(e)

# Iterate through the directory
for dir in os.listdir(directory):
    if dir.startswith('.') or dir.endswith('.md'):
        continue
    directory_path = os.path.join(directory, dir)
    
    print("Processing: ", dir)
    for filename in os.listdir(os.path.join(directory,dir)):
        if filename.endswith('.csv'):
            directory_path = os.path.join(directory, dir)
            file_path = os.path.join(directory_path, filename)
            rename_csv_and_copy(file_path,destination_directory)
    print("Renamed and copied: ", dir)

print("Done renaming and copying files.")