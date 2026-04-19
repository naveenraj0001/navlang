variables = {}
types = {}


# 🔥 TOKENIZER
def tokenize_expr(expr):
    tokens = []
    num = ""

    for char in expr:
        if char.isalnum():
            num += char
        else:
            if num:
                tokens.append(num)
                num = ""
            if char in "+-*/()":
                tokens.append(char)

    if num:
        tokens.append(num)

    return tokens


# 🔥 INFIX → POSTFIX
def to_postfix(tokens):
    precedence = {"+":1, "-":1, "*":2, "/":2}
    output = []
    stack = []

    for token in tokens:
        if token.isalnum():
            output.append(token)

        elif token in "+-*/":
            while (stack and stack[-1] != "(" and
                   precedence.get(stack[-1], 0) >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise Exception("Mismatched parentheses")
            stack.pop()

    while stack:
        if stack[-1] == "(":
            raise Exception("Mismatched parentheses")
        output.append(stack.pop())

    return output


# 🔥 POSTFIX EVALUATION
def eval_postfix(postfix):
    stack = []

    for token in postfix:
        if token not in "+-*/":

            # 🔹 Variable
            if token in variables:
                val = variables[token]
                if val is None:
                    raise Exception(f"Variable '{token}' not assigned")
                stack.append(val)

            # 🔹 Number
            elif token.isdigit():
                stack.append(int(token))

            else:
                raise Exception(f"Variable '{token}' not defined")

        else:
            if len(stack) < 2:
                raise Exception("Invalid expression")

            b = stack.pop()
            a = stack.pop()

            # 🔥 TYPE SAFETY
            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                raise Exception("Type mismatch in expression")

            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                if b == 0:
                    raise Exception("Division by zero")
                stack.append(a / b)

    if len(stack) != 1:
        raise Exception("Invalid expression")

    return stack[0]


# 🔥 FULL EXPRESSION ENGINE
def eval_expr(expr):
    tokens = tokenize_expr(expr)
    postfix = to_postfix(tokens)
    return eval_postfix(postfix)


# 🔥 MAIN EXECUTION
def execute(ast, line_no):
    global variables, types

    # 🔹 DECLARE
    if ast["type"] == "declare":
        types[ast["name"]] = ast["var_type"]
        variables[ast["name"]] = None
        return True

    # 🔹 INPUT
    elif ast["type"] == "input_assign":
        name = ast["name"]
        prompt = ast.get("prompt")

        if prompt:
            prompt = prompt.strip('"')
        else:
            prompt = name

        value = input(f"{prompt}: ")
        var_type = types.get(name)

        try:
            if var_type == "letI":
                if not value.isdigit():
                    raise Exception("Expected integer")
                value = int(value)

            elif var_type == "letF":
                try:
                    value = float(value)
                except:
                    raise Exception("Expected float")

            elif var_type == "letB":
                if value.lower() not in ["true", "false"]:
                    raise Exception("Expected boolean (true/false)")
                value = value.lower() == "true"

            elif var_type == "letS":
                if value.isdigit():
                    raise Exception("Expected string, got number")
                value = str(value)

            else:
                raise Exception("Variable not declared")

        except Exception as e:
            print(f"Line {line_no}: Type Error in '{name}' -> {e}")
            return False

        variables[name] = value
        return True

    # 🔹 say(expr)
    elif ast["type"] == "say_expr":
        try:
            result = eval_expr(ast["expr"])
            print(result)
            return True
        except Exception as e:
            print(f"Line {line_no}: {e}")
            return False

    # 🔹 say("text"; exprs)
    elif ast["type"] == "say":
        text = ast["text"].strip('"')
        output = text

        for v in ast["values"]:
            try:
                val = eval_expr(v)
                output += " " + str(val)
            except Exception as e:
                print(f"Line {line_no}: {e}")
                return False

        print(output)
        return True

    # 🔹 UNKNOWN
    else:
        print(f"Line {line_no}: Unknown command")
        return False