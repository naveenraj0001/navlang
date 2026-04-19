def tokenize(line):
    tokens = []
    current = ""
    in_string = False

    for char in line:
        if char == '"':
            in_string = not in_string
            current += char
            continue

        if char == " " and not in_string:
            if current:
                tokens.append(current)
                current = ""
        else:
            current += char

    if current:
        tokens.append(current)

    return tokens