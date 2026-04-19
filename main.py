import sys
from core.parser import parse
from core.interpreter import execute


def run_line(line, line_no):
    if not line.strip():
        return True  # skip empty lines

    try:
        ast = parse(line)
        return execute(ast, line_no)  # must return True/False
    except Exception as e:
        print(f"Line {line_no}: Error -> {e}")
        return False


def run_file(filename):
    try:
        with open(filename, "r") as f:
            for i, line in enumerate(f, start=1):
                success = run_line(line.strip(), i)
                if success is False:
                    break  # 🔥 STOP on first error
    except FileNotFoundError:
        print("File not found:", filename)


def repl():
    print("NaveenLang REPL 🔥 (type 'exit' to quit)")
    line_no = 1

    while True:
        try:
            line = input(">>> ")

            if line.lower() == "exit":
                break

            success = run_line(line, line_no)

            # 🔥 optional: stop REPL on error
            if success is False:
                continue  # or break if you want hard stop

            line_no += 1

        except Exception as e:
            print(f"Line {line_no}: Error -> {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()