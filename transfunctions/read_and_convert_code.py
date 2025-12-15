import os
import re
from openrouter import OpenRouter
import sys
from dotenv import load_dotenv

# SETUP

load_dotenv()

llm_api_key = os.getenv("OPENROUTER_API_KEY") #Don't forget to import your LLM Api Key
model = "google/gemini-2.5-flash" #Adjust Model Accordingly 

if not llm_api_key:
    print("🚨 ERROR: The OPENROUTER_API_KEY environment variable is not set.")
    sys.exit(1)

try:
    client = OpenRouter(
    api_key = llm_api_key,
    server_url = "https://ai.hackclub.com/proxy/v1"
    ) #Adjust this Accordingly, This Uses a Hack Club API (For Demo)

except Exception as e:
    print("🚨 ERROR: Failed to initialize OpenRouter client. Check your API key and network connection.")
    print("Details:", str(e))
    sys.exit(1)        


def read_and_convert_code(input_code, target_language):

    """
    Tier 2: Conversion Using large language model

    Args:
        code: The source code string to validate.
        file_path: path of file to be converted
        language_name: The name of the source language (e.g., 'python', 'javascript', 'go').

    Returns:
        Converted Code
    """

    prompt_for_conversion = f""" CONVERSION TASK: Convert the provided code from its source language to {target_language}.

    RULES:
    1. OUTPUT FORMAT: Raw code block only. NO markdown, NO explanation, NO wrappers (e.g., ```go).
    2. SEMANTICS: Preserve the original logic (mathematical, business) STRICTLY. Do NOT rewrite or re-implement logic (e.g., a simple 'return n > 1' must remain minimal).
    3. STYLE: Use idiomatic, modern {target_language}. Prioritize concision and functional style if the source code is minimal.
    4. COMPILATION: Include ALL necessary imports/packages for {target_language} (e.g., 'fmt' for Go, 'System.out' for Java output).
    SOURCE CODE:
    ---
    {input_code}
    ---

    CONVERTED_CODE:
    """        

    print(f"🧠 Starting Conversion: {len(input_code)} chars. Model: {model}...")

    try:

        response = client.chat.send(
            model = model,
            messages = [
                {"role":"user","content": prompt_for_conversion}
            ],
            stream = False
        )

        converted_code = response.choices[0].message.content
        converted_code = re.sub(r'^\s*```[a-zA-Z]*\n|\n```\s*$', '', converted_code, flags=re.MULTILINE).strip()

        return converted_code

    except Exception as e:
        print(f"\n🚨 FAILURE: LLM Conversion Failed.")
        print(f"Error Report: {e}")
        print("Please check your API key usage limits or network connection.") 