def generate_log(lx_errors: list, p_errors: list, a_errors: list, is_compiling = False, is_formatting = False) -> dict:
        is_passed = not lx_errors and not p_errors and not a_errors
        status = None

        if is_passed:
            if is_formatting:
                status = "Your source code has been formatted!"
            else:
                if is_compiling:
                    status = "[PASSED] Lexer, [PASSED] Parser, [PASSED] Analyzer. Compiling..."
                else:
                    status = "UwU++ Compiler compiled successfully!"
        else:
            if is_formatting:
                status = "Formatting unsuccessful. Resolve the following errors first:"
            else:
                status = "UwU++ Compiler compilation unsuccessful. Following errors were found:"

        return {
            "Status": status,
            "Lexical Errors": len(lx_errors) if len(lx_errors) > 0 else None,
            "Syntax Errors": len(p_errors) if len(p_errors) > 0 else None,
            "Semantic Errors": len(a_errors) if len(a_errors) > 0 else None
        }