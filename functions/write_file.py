import os
from .is_within_directory import is_within_directory
from google.genai import types

def write_file(working_directory, file_path, content):
    if not is_within_directory(working_directory, file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    full_path = os.path.join(working_directory, file_path)
    if not os.path.exists(full_path):
        with open(full_path, "w", encoding="utf-8") as f:
            pass
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written in the given file.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The full path of the file where content will be written.",
            )
        },
    ),
)
    
    
