import pandas as pd
import os
import shutil

# Read the modified_merged.csv file
data = pd.read_csv('modified_merged.csv')

# Create the selected_files folder if it doesn't exist
selected_files_folder = "selected_files"
if not os.path.exists(selected_files_folder):
    os.makedirs(selected_files_folder)

# Iterate over each row in the DataFrame
for index, row in data.iterrows():
    # Copy heart rate data file if path is not null
    hr_file_path = row['hr_path']
    if pd.notna(hr_file_path):
        hr_file_name = os.path.basename(hr_file_path)
        hr_id_prefix = row['ID']
        hr_new_file_name = f"{hr_id_prefix}_{hr_file_name}"
        try:
            shutil.copy(hr_file_path, os.path.join(selected_files_folder, hr_new_file_name))
            print(f"Copied: {hr_file_path}")
        except FileNotFoundError:
            print(f"File not found: {hr_file_path}")
            continue

    # Copy audio file if path is not null
    audio_file_path = row['audio_path']
    if pd.notna(audio_file_path):
        audio_file_name = os.path.basename(audio_file_path)
        audio_id_prefix = row['ID']
        audio_new_file_name = f"{audio_id_prefix}_{audio_file_name}"
        try:
            shutil.copy(audio_file_path, os.path.join(selected_files_folder, audio_new_file_name))
            print(f"Copied: {audio_file_path}")
        except FileNotFoundError:
            print(f"File not found: {audio_file_path}")
            continue

print("Files copied successfully.")
