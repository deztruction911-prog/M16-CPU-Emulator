tokens = [
    ["EndLine"], # End of Line (EoL)
    ["variable", "assignment", "value"], # variables
    ["LabAssign", "LabName"], # Labels
    ["compare", "arga", "argb", "goto"] # if statements
]

TokenReference = []
token = []
variables = {}
comparisons = {
    "==": "eq",
    "!=": "neq",
    ">": "grt",
    "<": "les",
    ">=": "geq",
    "<=": "leq"
}

def compile():
    FinalCode = []
    for CurrentTokenIndex in range(len(TokenReference)):
        if TokenReference[CurrentTokenIndex] == "variable":
            VarName = token[CurrentTokenIndex]
            VarVal = token[CurrentTokenIndex + 2]
            FinalCode.append(("var", f"{VarName}", f"{VarVal}"))
        elif TokenReference[CurrentTokenIndex] == "LabAssign":
            LabelName = token[CurrentTokenIndex + 1]
            FinalCode.append(("label", f"{LabelName}"))
        elif TokenReference[CurrentTokenIndex] == "compare":
            pass
    return FinalCode


def tokenise(code):
    global token, TokenReference
    for CurrentLine in code:
        if ';' not in CurrentLine:
            exit(f"Expected ';' token")
        if '=' in CurrentLine and "if" not in CurrentLine:
            parts = CurrentLine.split("=",1)
            variable = parts[0].strip()
            value = parts[1].strip().split(";")[0]
            for var_name in variables:
                if var_name in value:
                    value = value.replace(var_name, str(variables[var_name]))
            value = int(eval(value))
            variables[variable] = value
            token.extend([variable, "=", str(value), ";"])
            TokenReference.extend([tokens[1][0], tokens[1][1], tokens[1][2], tokens[0][0]])
        elif "label" in CurrentLine and "if" not in CurrentLine:
            parts = CurrentLine.split(" ", 1)
            token.extend([parts[0], parts[1].removesuffix(";"), ";"])
            TokenReference.extend([tokens[2][0], tokens[2][1], tokens[0][0]])
        elif "if" in CurrentLine:
            parts = CurrentLine.removesuffix(";").split(" ", 4)
            parts.append(";")
            token.extend(*[parts[0:6]])
            TokenReference.extend([tokens[3][0], tokens[3][1], comparisons[parts[2]], tokens[3][2], tokens[3][3], tokens[0][0]])



code = [
    ("x = 7;"),
    ("y = x*5;")
]
tokenise(code)
print(token)
print(TokenReference)
print(compile())