import sys
from core.compiler import compile_model

def main():
    if len(sys.argv) < 2:
        print("Usage: dslc <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file) as f:
        content = f.read()

    compile_model(content)

if __name__ == "__main__":
    main()
