import os
import subprocess
from .is_within_directory import is_within_directory
from google.genai import types

FILE_EXECUTION_TIMEOUT = 30

def run_python_file(working_directory, file_path: str, args=[]):
    if file_path.split('.')[-1] != 'py':
        return f'Error: "{file_path}" is not a Python file.'
    if not is_within_directory(working_directory, file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    full_path = os.path.join(working_directory, file_path)
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    try:
        result = subprocess.run(
            ["python", full_path] + (args or [])
            ,timeout=FILE_EXECUTION_TIMEOUT
            ,cwd=working_directory
            ,capture_output=True
            ,text=True)
        exit_code_msg = '' if result.returncode == 0 else f'Process exited with code {result.returncode}'
        if not result.stderr and not result.stdout:
            return 'No output produced'
        else:
            return f'STDOUT: {result.stdout} STDERR: {result.stderr} {exit_code_msg}'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file with given args if any",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The full path of the python script which is to be run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING, description="Argument string."),
                description="Arguements to be passed to the python script if any"
            )
        },
    ),
)
    