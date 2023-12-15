import os
import os
import shutil

directory = r"C:\Laing ORourke\Laing ORourke\OneDrive - Laing ORourke\Documents\trimble-connect-py"


def remove_pycache(directory):
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            print(f'Removed: {pycache_path}')

# Replace with your directory path
remove_pycache(directory)


def print_tree_folder(directory, indent=0):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    # Print the directory name with the appropriate indentation
    print('  ' * indent + os.path.basename(directory) + '/')

    # Iterate through each item in the directory
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        # If the item is a directory, recurse into it
        if os.path.isdir(path):
            print_tree_folder(path, indent + 1)
        else:
            # If the item is a file, print its name with indentation
            print('  ' * (indent + 1) + item)

# Example usage
print_tree_folder(directory)
