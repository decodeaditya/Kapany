import argparse
import sys 
import os
from colorama import Fore, init, Style
from consts.file_extensions import file_extension_map

from transfunctions.validation import validate_code_syntax
from transfunctions.read_and_convert_code import read_and_convert_code 

init(autoreset=True)

#TERMINAL ENHANCEMENT

def display_header():
    # displays Header and logo

    logo = f"""
    {Fore.GREEN}       _-_-_
    {Fore.GREEN}    /    / /     
    {Fore.GREEN}   /____/_/       {Fore.YELLOW}CodeMend - The Autonomous Code Agent{Style.RESET_ALL}
    {Fore.GREEN}  (______)        {Fore.GREEN}Tier 1: Zero-Cost Validation{Style.RESET_ALL}
    {Fore.GREEN}

    """

    print(logo)


# SETTING UP CLI

def setup_cli():
    parser = argparse.ArgumentParser(
        description="CodeMend: Autonomous Agent for Language Migration and Correction."
    )

    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input code file to be converted."
    )

    parser.add_argument(
        "--target",
        type=str,
        required=True
    )

    return parser.parse_args()


# MAIN LOGIC

if __name__ == "__main__":
    args = setup_cli()

    try:
        with open(args.input_file, "r") as file:
            input_code = file.read()
    except FileNotFoundError:
        print(f"🚨 ERROR: The file '{args.input_file}' was not found.")
        sys.exit(1)        

    print("\n--- TIER 1: RUNNING SYNTAX VALIDATION (Zero Cost Guardrail) ---")

    root, extension = os.path.splitext(args.input_file)
    source_language = [key if value == extension[1:] else "Identify Language" for key, value in file_extension_map.items()][0]

    output_filename = f"transformed_Code{extension}"


    isValid,message = validate_code_syntax(
        input_code, source_language
    )

    if isValid:
        print("✅ Code Syntax Validation Passed. Proceeding to LLM Conversion.")
        print("\n--- TIER 2: RUNNING THE SECOND STAGE - LLM BASED CODE CONVERSION [GEMINI 2.5 FLASH/GPT-5 mini] ---")
        final_code = read_and_convert_code(input_code, args.target)
        output_extension = file_extension_map.get(args.target, "txt")
        filepath = f"converted-code.{output_extension}"
        with open(filepath,"w") as output_file:
            output_file.write(final_code)

        print(f"✅ SUCCESS! Checkout for the Magic that just Did happen now in the file: {filepath}")
    else:
        print("🛑 Code Syntax Validation Failed. Migration Halted.")
        print(f"Details: {message}")
        print("No API cost incurred.")
        sys.exit(1)
