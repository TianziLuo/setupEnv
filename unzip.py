import os
import shutil
import zipfile

def unzip():

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    downloadenv_folder = os.path.join(desktop_path, "downloadenv")
    final_folder_name = "downloadenv"  # Final folder name
    d_drive_target = r"C:\downloadenv"  # Target path on D drive

    # Find .zip files starting with "downloadenv"
    files = [f for f in os.listdir(downloadenv_folder) if f.startswith("downloadenv") and f.endswith(".zip")]

    if not files:
        print("No .zip file starting with 'downloadenv' was found!")
    else:
        print(f"File found: {files[0]}")

        try:
            # Full path to the .zip file
            zip_file = os.path.join(downloadenv_folder, files[0])
            
            # Temporary extraction directory
            temp_extract_dir = os.path.join(desktop_path, "temp_extracted")
            if not os.path.exists(temp_extract_dir):
                os.makedirs(temp_extract_dir)
            
            # Extract the .zip file
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_dir)
            
            # Handle extracted content
            extracted_items = os.listdir(temp_extract_dir)
            if len(extracted_items) == 1 and os.path.isdir(os.path.join(temp_extract_dir, extracted_items[0])):
                # If a single folder exists, rename it directly
                extracted_folder = os.path.join(temp_extract_dir, extracted_items[0])
            else:
                # If multiple items exist, treat temp_extract_dir as the folder
                extracted_folder = temp_extract_dir

            # Final target folder on Desktop
            final_path = os.path.join(desktop_path, final_folder_name)
            
            # Remove existing folder with the same name, if it exists
            if os.path.exists(final_path):
                shutil.rmtree(final_path)
            
            # Rename or move extracted folder to the final name
            shutil.move(extracted_folder, final_path)
            
            # Cleanup temporary directory if it was not renamed
            if os.path.exists(temp_extract_dir):
                try:
                    os.rmdir(temp_extract_dir)
                except OSError as e:
                    print(f"Failed to remove temp directory {temp_extract_dir}: {e}")

            # Handle the D drive target
            if os.path.exists(d_drive_target):
                shutil.rmtree(d_drive_target)  # Remove the old folder if it exists
                print(f"Old folder on D drive has been deleted: {d_drive_target}")
            
            # Copy to D drive
            shutil.copytree(final_path, d_drive_target)
            print(f"Files have been successfully copied to D drive: {d_drive_target}")
            
            # Delete the renamed folder on Desktop
            shutil.rmtree(final_path)
            print(f"The folder on the Desktop has been deleted: {final_path}")
            
        except zipfile.BadZipFile:
            print("Unable to read the .zip file. Please check if the file is corrupted or the path is correct!")
        except Exception as e:
            print(f"An error occurred during extraction or copying: {e}")
            
'''
if __name__ == "__main__":
    unzip()
'''