import sys
from core.praser import parse
from core.interpreter import execute


def run_line(line):
    if not line.strip():
        return
    ast = parse(line)
    execute(ast)


def run_file(filename):
    try:
        with open(filename, "r") as f:
            for line in f:
                run_line(line.strip())
    except FileNotFoundError:
        print("File not found:", filename)


def repl():
    print("NaveenLang REPL 🔥 (type 'exit' to quit)")
    while True:
        try:
            line = input(">>> ")
            if line.lower() == "exit":
                break
            run_line(line)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # file mode
        run_file(sys.argv[1])
    else:
        # interactive mode
        repl()