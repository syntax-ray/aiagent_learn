import os
from .is_within_directory import is_within_directory
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    if not is_within_directory(working_directory, file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    full_path = os.path.join(working_directory, file_path)
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(full_path, "r") as f:
        try:
            content = f.read()
        except Exception as e:
            return f'Error: {e}'
        num_chars = len(content)
        if num_chars > MAX_CHARS:
            return f'{content[0: MAX_CHARS]} [...File "{file_path}" truncated at 10000 characters]'
        else:
            return content
        

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get contents of a file up to a certain character limit defined by MAX_CHARS",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The full path of the file which contents are to be read from",
            ),
        },
    ),
)


    