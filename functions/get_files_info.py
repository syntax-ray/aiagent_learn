import os
from .is_within_directory import is_within_directory
from google.genai import types


def get_files_info(working_directory, directory="."):
    files_info = ''
    if not is_within_directory(working_directory, directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    full_path = os.path.join(working_directory, directory)
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    try:
        path_items = os.listdir(full_path)
    except Exception as e:
        return f'Error: {e}'
    for i in range(0, len(path_items)):
        file_name = path_items[i]
        try:
            full_file_path = os.path.join(full_path, file_name)
            file_size = os.path.getsize(full_file_path)
            is_dir = os.path.isdir(full_file_path)
        except Exception as e:
            return f'Error: {e}'
        if i != len(path_items) - 1:
            files_info += f'- {file_name}: file_size={file_size} bytes, is_dir={is_dir}\n'
        else:
            files_info += f'- {file_name}: file_size={file_size} bytes, is_dir={is_dir}'
    return files_info

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)