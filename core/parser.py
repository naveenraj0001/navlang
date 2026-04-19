def parse(line):
    line = line.strip()

    # 🔹 Declaration
    if line.startswith(("letI", "letF", "letS", "letB")):
        parts = line.split()
        return {
            "type": "declare",
            "var_type": parts[0],
            "name": parts[1]
        }

    # 🔹 Input assignment
    elif "=" in line and "give(" in line:
        name = line.split("=")[0].strip()

        inside = line.split("give(")[1].rstrip(")")
        prompt = inside.strip() if inside.strip() else None

        return {
            "type": "input_assign",
            "name": name,
            "prompt": prompt
        }

    # 🔹 say(...)
    elif line.startswith("say(") and line.endswith(")"):
        inside = line[4:-1].strip()

        if ";" not in inside:
            return {
                "type": "say_expr",
                "expr": inside
            }

        parts = inside.split(";")
        text = parts[0].strip()
        values = [v.strip() for v in parts[1].split(",")]

        return {
            "type": "say",
            "text": text,
            "values": values
        }

    else:
        raise Exception("Syntax error")