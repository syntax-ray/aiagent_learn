import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
import sys

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
FREE_TEIR_MODEL = 'gemini-2.0-flash-001'
cli_arguements = sys.argv
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


def call_function(function_call_part, verbose=False):
    available_functions = {
        'get_file_content': get_file_content,
        'get_files_info': get_files_info,
        'run_python_file': run_python_file,
        'write_file': write_file
    }
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    if not available_functions.get(function_call_part.name, False):
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    function_result = available_functions[function_call_part.name]('./calculator', **function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )
    



def main():
    verbose = False
    if len(cli_arguements) == 1:
        print('No prompt was provided')
        exit(1)
    else:
        if cli_arguements and len(cli_arguements) >= 3:
            if cli_arguements[2] == '--verbose':
                verbose = True
        user_prompt = cli_arguements[1]
        messages = [
            types.Content(role='user', parts=[types.Part(text=user_prompt)])
        ]
        print("Hello from aiagent!")
        if verbose:
            print(f'The prompt entered is:::: {user_prompt}')
        ai_response = client.models.generate_content(model=FREE_TEIR_MODEL,
                                                    contents=messages,
                                                    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[available_functions])
                                                    )
        print(f'The ai agent says:::: {ai_response.text}')
        if verbose:
            if ai_response.function_calls:
                for call in ai_response.function_calls:
                    print(f"Calling function: {call.name}({call.args})")
                    function_call_result = call_function(call)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception(f'Function {call.name} was called but it did not return anything')
                    else:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
            print(f'Prompt tokens: {ai_response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {ai_response.usage_metadata.candidates_token_count}')


if __name__ == "__main__":
    main()