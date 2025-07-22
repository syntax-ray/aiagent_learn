import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
FREE_TEIR_MODEL = 'gemini-2.0-flash-001'
cli_arguements = sys.argv

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
                                                    contents=messages)
        print(f'The ai agent says:::: {ai_response.text}')
        if verbose:
            print(f'Prompt tokens: {ai_response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {ai_response.usage_metadata.candidates_token_count}')


if __name__ == "__main__":
    main()
