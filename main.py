import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
FREE_TEIR_MODEL = 'gemini-2.0-flash-001'
cli_arguements = sys.argv

def main():
    if len(cli_arguements) == 1:
        print('No prompt was provided')
        exit(1)
    else:
        user_prompt = cli_arguements[1]
        print("Hello from aiagent!")
        print(f'The prompt entered is {user_prompt}')
        exit()
        ai_response = client.models.generate_content(model=FREE_TEIR_MODEL,
                                                    contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.')
        print(f'The ai agent says::::\n {ai_response.text}')
        print(f'Prompt tokens: {ai_response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {ai_response.usage_metadata.candidates_token_count}')


if __name__ == "__main__":
    main()
