import os
import shutil

# Define the directories to clear
directories = ['trimmed', 'mp3raw', 'withaudio', 'mp3']

# Loop through each directory and remove its contents
for directory in directories:
    # Check if the directory exists
    if os.path.exists(directory):
        # Loop through and remove each item in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                # Remove file or directory
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file or symbolic link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove the directory
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        print(f'Directory {directory} does not exist.')