variables = {}
types = {}

# 🔥 TOKENIZER for expressions
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


# 🔥 Convert to postfix (Shunting Yard Algorithm)
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
            stack.pop()

    while stack:
        output.append(stack.pop())

    return output


# 🔥 Evaluate postfix
def eval_postfix(postfix):
    stack = []

    for token in postfix:
        if token not in "+-*/":
            if token in variables:
                stack.append(variables[token])
            else:
                stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                stack.append(a / b)

    return stack[0]


# 🔥 Full expression evaluator
def eval_expr(expr):
    tokens = tokenize_expr(expr)
    postfix = to_postfix(tokens)
    return eval_postfix(postfix)


def execute(ast):
    global variables, types

    # 🔹 Declaration
    if ast["type"] == "declare":
        types[ast["name"]] = ast["var_type"]
        variables[ast["name"]] = None

    # 🔹 Input
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
                value = int(value)
            elif var_type == "letF":
                value = float(value)
            elif var_type == "letB":
                value = value.lower() == "true"
            elif var_type == "letS":
                value = str(value)
        except:
            print("Type Error")
            return

        variables[name] = value

    # 🔹 say(expr)
    elif ast["type"] == "say_expr":
        result = eval_expr(ast["expr"])
        print(result)

    # 🔹 say("text"; exprs)
    elif ast["type"] == "say":
        text = ast["text"].strip('"')
        output = text

        for v in ast["values"]:
            val = eval_expr(v)
            output += " " + str(val)

        print(output)

    else:
        raise Exception("Unknown AST type")