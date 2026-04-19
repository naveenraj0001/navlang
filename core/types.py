def declare(var_type, name, value, variables):
    if var_type == "letI":
        variables[name] = int(value)

    elif var_type == "letF":
        variables[name] = float(value)

    elif var_type == "letS":
        if value.startswith('"') and value.endswith('"'):
            variables[name] = value[1:-1]
        else:
            raise Exception("String must be in quotes")

    elif var_type == "letB":
        if value == "true":
            variables[name] = True
        elif value == "false":
            variables[name] = False
        else:
            raise Exception("Invalid boolean")

    else:
        raise Exception("Unknown datatype")