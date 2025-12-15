from tree_sitter_language_pack import get_parser

#Checking syntax validity 
def validate_code_syntax(code: str, language: str) -> tuple[bool, str]:
    """
    Syntax Validation: Checks the input code for basic syntax errors using Tree-Sitter.

    Args:
        code: The source code string to validate.
        language_name: The name of the source language (e.g., 'python', 'javascript', 'go').

    Returns:
        A tuple: (is_valid: bool, error_message: str)
    """

    try:
        parser = get_parser(language)

    except Exception as e:
        return False, f"🛑 Unsupported language for syntax validation: {language}. Error: {str(e)}"
    
    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node

    has_errors = bool(root_node.has_error)

    if not has_errors:
        return True, "✅ Code is has no syntax errors! Good to go for conversion."
    
    else:
        cursor = tree.walk()
        error_node = None

        while True:
            node = cursor.node

            if node.type == "ERROR":
                error_node = node
                break

            if cursor.goto_first_child():
                continue

            if cursor.goto_next_sibling():
                continue

            while True:
                if not cursor.goto_parent():
                    return False, "🚨 Code contains syntax errors, but specific error node not found."
                
                if cursor.goto_next_sibling():
                    break

            if cursor.node.type == root_node.type:
                break   

            if error_node:

                start_row, start_col = error_node.start_point
                error_line = code.splitlines()[start_row].strip()

                error_msg = (
                    f'''🚨 TIER 1 SYNTAX ERROR DETECTED in {language}. \n'''
                    f'''AT LOCATION: Line {start_row + 1}, Column {start_col + 1} \n'''
                    f'''ERROR IS IN THE CODE SNIPPET: "{error_line}" \n'''
                    f'''Please fix the syntax error before running the LLM conversion (Tier 2).'''
                )

                return False, error_msg
            
            else:
                return False, "🚨 Code contains syntax errors, but specific error node not found."