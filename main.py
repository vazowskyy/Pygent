import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    response_candidates = []

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        
        response_candidates.append(response.candidates[0].content)

        if response_candidates:
            for candidate in response_candidates:
                messages.append(candidate)

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                # print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call, verbose)

                if not function_call_result.parts:
                    raise Exception("Function returned empty parts list")

                part = function_call_result.parts[0]

                if part.function_response is None or not isinstance(part.function_response, types.FunctionResponse):
                    raise Exception("Function response is None or call_function returned wrong type")
                
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("Response is None")

                function_responses.append(part)
                
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

        else:
            if verbose:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
            print("Final response:")
            print(response.text)
            return None

        messages.append(types.Content(role="user", parts=function_responses))
    
    print("Something went wrong, maximum iterations reached")

if __name__ == "__main__":
    main()